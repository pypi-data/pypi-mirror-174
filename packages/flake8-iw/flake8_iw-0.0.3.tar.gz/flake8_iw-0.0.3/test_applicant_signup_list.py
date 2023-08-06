import http
import json
from unittest.mock import patch

from expects import be_empty, be_none, equal, expect, have_key, have_len
from faker import Factory
from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from backend.models import PushToken, UserProfile, UserReferral, UserWorkPreference
from backend.tests import factories
from backend.tests.matchers import have_status
from lib.expects_mock import have_been_called
from positions.tests import factories as positions_factories

fake = Factory.create("en_US")
fake.add_provider(factories.PhoneNumberProvider)


class ApplicantSignupListTests(APITestCase):
    def setUp(self):
        self.position = positions_factories.PositionFactory()
        self.user = factories.UserProfileFactory()
        self.referral_user = factories.UserProfileFactory()
        self.request_data = json.dumps(
            {
                "data": {
                    "type": "applicant_signup",
                    "attributes": {
                        "phone_number": fake.us_phone_number(),
                        "email": fake.email(),
                        "locale": "en",
                        "geocode": "%s,%s" % (fake.latitude(), fake.longitude()),
                        "positions": [self.position.name],
                        "work_preferences": ["jobs", "gigs"],
                        "os": PushToken.OS_IOS,
                        "token": fake.pystr(),
                        "referral_code": self.referral_user.referral_code(),
                    },
                }
            }
        )

    @parameterized.expand(
        [
            ("no_app_version", None, status.HTTP_201_CREATED),
            ("unsupported_app_version", "2.61.2", status.HTTP_400_BAD_REQUEST),
            ("supported_app_version", "2.61.3", status.HTTP_201_CREATED),
        ]
    )
    def test_create(self, _, version, response_status):
        url = reverse("applicant-signup-list")

        headers = {"HTTP_X_APP_VERSION": version}

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json", **headers)
        expect(response.status_code).to(equal(response_status))

    def test_create_anonymous(self):
        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=None)

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))
        data = json.loads(response.content).get("data")

        expect(data["attributes"]).to(be_empty)
        expect(data["relationships"]).to(have_key("user"))

    def test_create_user(self):
        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=self.user.user)

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))

    def test_create_duplicate(self):
        url = reverse("applicant-signup-list")
        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))
        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_400_BAD_REQUEST))

    def test_create_required(self):
        url = reverse("applicant-signup-list")
        request_data = json.dumps({"data": {"type": "applicant_signup", "attributes": {"locale": "en"}}})
        response = self.client.post(url, data=request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_400_BAD_REQUEST))
        errors = json.loads(response.content)
        expect(errors).to(have_key("errors"))
        expect(errors["errors"]).to(have_len(1))

    def test_cookie_fix(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(user=None)
        url = reverse("applicant-signup-list")
        client.cookies = http.cookies.SimpleCookie({"sessionid": "fake", "csrftoken": "fake", "test": "fake"})
        response = client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))

        # Cookies should be cleared out in response
        expect(response.cookies.get("sessionid").value).to(equal(""))
        expect(response.cookies.get("csrftoken").value).to(equal(""))
        expect(response.cookies.get("test")).to(be_none)

    def test_create_duplicate_cookie_fix(self):
        request_data = {"data": {"type": "applicant_signup", "attributes": {"phone_number": self.user.phonenum}}}
        client = APIClient(enforce_csrf_checks=True)
        client.force_authenticate(user=None)
        url = reverse("applicant-signup-list")
        client.cookies = http.cookies.SimpleCookie({"sessionid": "fake", "csrftoken": "fake", "test": "fake"})
        response = client.post(url, data=request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_400_BAD_REQUEST))

        # Cookies should be cleared out in response
        expect(response.cookies.get("sessionid").value).to(equal(""))
        expect(response.cookies.get("csrftoken").value).to(equal(""))
        expect(response.cookies.get("test")).to(be_none)

    def test_list(self):
        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=self.user.user)
        response = self.client.get(url, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_405_METHOD_NOT_ALLOWED))

    def test_list_anonymous(self):
        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=None)
        response = self.client.get(url, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_405_METHOD_NOT_ALLOWED))

    def test_referral_user_is_attributed_for_signup(self):
        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=None)

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))
        data = json.loads(response.content).get("data")
        user_referral = UserReferral.objects.get(referred_user_id=data["id"])

        expect(user_referral.creator).to(equal(self.referral_user))
        expect(user_referral.incentive).to(equal(UserReferral.INCENTIVE_50_ON_GIG_WORKED))

    def test_no_one_is_attributed_when_referral_code_is_invalid(self):
        self.request_data = json.dumps(
            {
                "data": {
                    "type": "applicant_signup",
                    "attributes": {
                        "phone_number": fake.us_phone_number(),
                        "email": fake.email(),
                        "locale": "en",
                        "geocode": "%s,%s" % (fake.latitude(), fake.longitude()),
                        "positions": [self.position.name],
                        "os": PushToken.OS_IOS,
                        "token": fake.pystr(),
                        "referral_code": "invalid-code",
                    },
                }
            }
        )

        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=None)

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        error = json.loads(response.content).get("errors")[0]
        expect(response).to(have_status(status.HTTP_400_BAD_REQUEST))
        expect(error["detail"]).to(equal("Invalid referral code"))

    def test_no_one_is_attributed_when_referral_user_does_not_exist(self):
        hasher = self.user._referral_code_hasher()
        # generate referral_code for id that doesn't exist
        referral_code = hasher.encode(232323)

        self.request_data = json.dumps(
            {
                "data": {
                    "type": "applicant_signup",
                    "attributes": {
                        "phone_number": fake.us_phone_number(),
                        "email": fake.email(),
                        "locale": "en",
                        "geocode": "%s,%s" % (fake.latitude(), fake.longitude()),
                        "positions": [self.position.name],
                        "os": PushToken.OS_IOS,
                        "token": fake.pystr(),
                        "referral_code": referral_code,
                    },
                }
            }
        )

        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=None)

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        error = json.loads(response.content).get("errors")[0]
        expect(response).to(have_status(status.HTTP_400_BAD_REQUEST))
        expect(error["detail"]).to(equal("Invalid referral code"))

    def test_user_work_preference_is_set_to_gig_if_referral_signup(self):
        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=None)
        request_data = json.dumps(
            {
                "data": {
                    "type": "applicant_signup",
                    "attributes": {
                        "phone_number": fake.us_phone_number(),
                        "email": fake.email(),
                        "locale": "en",
                        "geocode": "%s,%s" % (fake.latitude(), fake.longitude()),
                        "positions": [self.position.name],
                        "work_preferences": [],
                        "os": PushToken.OS_IOS,
                        "token": fake.pystr(),
                        "referral_code": self.referral_user.referral_code(),
                    },
                }
            }
        )

        response = self.client.post(url, data=request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))
        data = json.loads(response.content).get("data")
        user_id = data["id"]

        work_preferences = UserProfile.objects.get(id=user_id).work_preferences.all()
        expect(work_preferences.count()).to(equal(1))
        expect(work_preferences.first().preference).to(equal(UserWorkPreference.WORK_PREFERENCE_GIGS))

    @patch("backend.tasks.task_notify_referral_signup.delay")
    def test_task_notify_referral_signup_not_called(self, mock_notify_referral_signup):
        request_data = json.dumps(
            {
                "data": {
                    "type": "applicant_signup",
                    "attributes": {
                        "phone_number": fake.us_phone_number(),
                        "email": fake.email(),
                        "locale": "en",
                        "geocode": "%s,%s" % (fake.latitude(), fake.longitude()),
                        "positions": [self.position.name],
                        "os": PushToken.OS_IOS,
                        "token": fake.pystr(),
                    },
                }
            }
        )

        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=self.user.user)
        response = self.client.post(url, data=request_data, content_type="application/vnd.api+json")
        expect(response).to(have_status(status.HTTP_201_CREATED))
        expect(mock_notify_referral_signup).to_not(have_been_called)

    def test_heard_from_reason_is_saved(self):
        self.request_data = json.dumps(
            {
                "data": {
                    "type": "applicant_signup",
                    "attributes": {
                        "phone_number": fake.us_phone_number(),
                        "email": fake.email(),
                        "locale": "en",
                        "geocode": "%s,%s" % (fake.latitude(), fake.longitude()),
                        "positions": [self.position.name],
                        "work_preferences": ["jobs", "gigs"],
                        "os": PushToken.OS_IOS,
                        "token": fake.pystr(),
                        "referral_code": self.referral_user.referral_code(),
                        "heard_from": "Friend",
                    },
                }
            }
        )

        url = reverse("applicant-signup-list")
        self.client.force_authenticate(user=self.user.user)

        response = self.client.post(url, data=self.request_data, content_type="application/vnd.api+json")
        data = json.loads(response.content).get("data")
        heard_from = UserProfile.objects.get(id=data.get("id")).heard_from
        expect(response).to(have_status(status.HTTP_201_CREATED))
        expect(heard_from).to(equal("Friend"))
