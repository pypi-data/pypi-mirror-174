# flake8_iw

## Supported lint checks

### Use of @patch

```python
from unittest.mock import patch_alias

class ShiftGroupUpdatedTests(TestCase):
    def test_created(self, mock_task):
        self.mock_call = patch_alias("apps.openshifts.signals.task_update_shiftgroup_stats.delay")
        ...
```

```python
from unittest.mock import patch

@patch("apps.openshifts.signals.task_update_shiftgroup_stats.delay")
def my_function(my_argument):
    ...
```

Lint check to prevent the use of `@patch` and `patch` directly.
Recommendation: Use `PatchingTestCase` / `PatchingTransactionTestCase` instead
