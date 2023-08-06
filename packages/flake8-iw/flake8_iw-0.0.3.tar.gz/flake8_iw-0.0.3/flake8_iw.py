import ast
import sys
from dataclasses import dataclass
from typing import Optional, Union

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

_IW_PATCH_CALL_ERROR_MSG = "IW01 unsafe @patch/patch call"


def _get_function_call_attribute(node: Union[ast.Attribute, ast.Name]):
    if isinstance(node, ast.Name):
        return node.id, node
    elif isinstance(node.value, ast.Attribute) or isinstance(node.value, ast.Name):
        res, name_node = _get_function_call_attribute(node.value)
        return f"{res}.{node.attr}", name_node
    else:
        return "-", None


@dataclass
class ImportName:
    """Dataclass for representing an import"""

    _module: str
    _name: str
    _alias: Optional[str]

    @property
    def name(self) -> str:
        """
        Returns the name of the import.
        The name is
            import pandas
                     ^-- this
            from pandas import DataFrame
                                  ^--this
            from pandas import DataFrame as df
                                            ^-- or this
        depending on the type of import.
        """
        return self._alias or self._name

    @property
    def full_name(self) -> str:
        """
        Returns the full name of the import.
        The full name is
            import pandas --> 'pandas'
            from pandas import DataFrame --> 'pandas.DataFrame'
            from pandas import DataFrame as df --> 'pandas.DataFrame'
        """
        return f"{self._module}{self._name}"


class Visitor(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imports: dict[str, ImportName] = {}
        self.issues = []
        self.safe_patch_nodes = []

    def visit_Import(self, node: ast.Import) -> None:
        self.add_import(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.add_import(node)

    def visit_With(self, node: ast.With) -> None:
        for withitem in node.items:
            ctx_withitem_node = withitem.context_expr
            if not isinstance(ctx_withitem_node, ast.Call):
                continue

            if (
                isinstance(ctx_withitem_node.func, ast.Name)
                and ctx_withitem_node.func.id in self.imports
                and self.imports[ctx_withitem_node.func.id].full_name == "unittest.mock.patch"
            ):
                call_node: ast.Name = withitem.context_expr.func
                self.safe_patch_nodes.append(f"{call_node.lineno}:{call_node.col_offset}")

            if (
                isinstance(ctx_withitem_node.func, ast.Attribute)
                and isinstance(ctx_withitem_node.func.value, ast.Attribute)
                and ctx_withitem_node.func.attr == "patch"
            ):
                # Extract module path and original ast.Name node
                module_path_attr, name_node = _get_function_call_attribute(ctx_withitem_node.func.value)
                if name_node and module_path_attr == "unittest.mock":
                    self.safe_patch_nodes.append(f"{name_node.lineno}:{name_node.col_offset}")

    def add_import(self, node: Union[ast.Import, ast.ImportFrom]) -> None:
        """Add relevant ast imports to import lists."""
        for name_node in node.names:
            if name_node.name:
                imp = ImportName(
                    _module=(f"{node.module}." if isinstance(node, ast.ImportFrom) else ""),
                    _alias=name_node.asname,
                    _name=name_node.name,
                )

                self.imports[imp.name] = imp


class ForbiddenPatchCallFinder(ast.NodeVisitor):
    def __init__(self, imports, excludes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.issues = []
        self.imports: dict[str, ImportName] = imports if imports else {}
        self.excludes: [str] = excludes if excludes else []

    def find_patch_call_issues(self, node):
        # Check direct patch function calls and alias function calls. e.g. patch() or mock_patch()
        if (
            node.func
            and isinstance(node.func, ast.Name)
            and node.func.id in self.imports
            and self.imports[node.func.id].full_name == "unittest.mock.patch"
        ):
            node_loc = f"{node.lineno}:{node.col_offset}"
            if node_loc not in self.excludes:
                self.issues.append((node.lineno, node.col_offset, _IW_PATCH_CALL_ERROR_MSG))

        # Check patch calls made using full function reference. e.g. unittest.mock.patch()
        if node.func and isinstance(node.func, ast.Attribute) and node.func.attr == "patch":
            # Extract module path and original ast.Name node
            module_path_attr, name_node = _get_function_call_attribute(node.func.value)
            node_loc = f"{node.lineno}:{node.col_offset}"
            if name_node and module_path_attr == "unittest.mock" and node_loc not in self.excludes:
                self.issues.append((node.lineno, node.col_offset, _IW_PATCH_CALL_ERROR_MSG))

    def find_patch_decorator_issues(self, node):
        func_decorator_list: list[ast.Name] = [
            decorator_node.func
            for decorator_node in node.decorator_list
            if isinstance(decorator_node, ast.Call) and isinstance(decorator_node.func, ast.Name)
        ]

        func_noargs_decorator_list: list[ast.Name] = [
            decorator_node for decorator_node in node.decorator_list if isinstance(decorator_node, ast.Name)
        ]

        for decorator_name in func_decorator_list + func_noargs_decorator_list:
            if decorator_name.id == "patch":
                self.issues.append(
                    (
                        decorator_name.lineno,
                        decorator_name.col_offset,
                        _IW_PATCH_CALL_ERROR_MSG,
                    )
                )

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        self.find_patch_decorator_issues(node)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.find_patch_decorator_issues(node)
        self.generic_visit(node)
        return node

    def visit_Call(self, node: ast.Call) -> ast.Call:
        self.find_patch_call_issues(node)
        self.generic_visit(node)
        return node


class Plugin(object):
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        parser = Visitor()
        parser.visit(self.tree)

        for lineno, column, msg in parser.issues:
            yield (lineno, column, msg, Plugin)

        parser = ForbiddenPatchCallFinder(imports=parser.imports, excludes=parser.safe_patch_nodes)
        parser.visit(self.tree)

        for lineno, column, msg in parser.issues:
            yield (lineno, column, msg, Plugin)
