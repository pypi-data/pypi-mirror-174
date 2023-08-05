import sys
import inspect
from pathlib import Path
from typing import Optional


def get_importer_path() -> Optional[Path]:
    """Returns the path (including filename) of the file that called `import fiximport`"""
    for frame in inspect.stack()[1:]:
        is_internal_library = len(frame.filename) != 0 and frame.filename[0] == "<"
        is_package_init = (
            frame.code_context is not None
            and len(frame.code_context) != 0
            and (
                frame.code_context[0] == "from .fiximport import *\n"
                or "importer_path = get_importer_path()\n" in frame.code_context[0]
            )
        )
        if not is_internal_library and not is_package_init:
            return Path(frame.filename)


def find_project_root(file_path: Path) -> Path:
    """Returns the project root of the given `file_path`"""

    def is_likely_project_root(candidate: Path) -> bool:
        typical_root_items = [
            ".git",
            ".gitignore",
            "LICENSE",
            "requirements.txt",
            "pyproject.toml",
        ]
        for item in candidate.iterdir():
            if item.name in typical_root_items:
                return True
        return False

    if not file_path.is_absolute():
        file_path = file_path.resolve()

    # For example, 'c:/foo/bar/setup.py' has 3 parents, 'c:/foo/bar', 'c:/foo', and 'c:/'
    parents = file_path.parents
    for parent in parents:
        if is_likely_project_root(parent):
            return parent

    # If none of the parents appeared to be the project root, default to the first parent.
    return file_path.parent


def add_python_dirs_to_syspath(root: Path) -> None:
    assert root.is_dir() and root.is_absolute()

    visited_set = set()
    sys_path_set = set(sys.path)  # Set for fast lookups.

    # Explicitly add the project root's parent.
    # This allows imports such as `import coolproject.helper` vs `import helper`.
    parent_str = str(root.parent)
    if parent_str not in sys_path_set:
        sys.path.insert(0, parent_str)
        sys_path_set.add(parent_str)

    # Explicitly add the project root.
    # On some installations of the python interpreter, this has been necessary.
    root_str = str(root)
    if root_str not in sys_path_set:
        sys.path.insert(0, root_str)
        sys_path_set.add(root_str)

    add_python_dir_to_syspath(root, sys_path_set, visited_set)


def add_python_dir_to_syspath(root: Path, sys_path_set: set, visited_set: set) -> bool:
    """
    Returns whether the given `root` is likely a python module.
    It is added to the sys.path if it is.
    """
    assert root.is_dir() and root.is_absolute()

    root_str = str(root)
    visited_set.add(root_str)
    typical_python_extensions = [".py", ".pyc", ".pyo", ".pyd"]

    is_python_module = False

    for item in root.iterdir():
        if item.is_dir() and str(item) not in visited_set:
            is_child_python_module = add_python_dir_to_syspath(
                item, sys_path_set, visited_set
            )

            # If any child directories are python modules, consider self as a python module too.
            if is_child_python_module and root_str not in sys_path_set:
                sys.path.insert(0, root_str)
                sys_path_set.add(root_str)
                is_python_module = True

        # Likely a module if the current directory contains python files. Add current directory to sys.path.
        if (
            item.is_file()
            and item.suffix in typical_python_extensions
            and root_str not in sys_path_set
        ):
            sys.path.insert(0, root_str)
            sys_path_set.add(root_str)
            is_python_module = True

    return is_python_module


try:
    importer_path = get_importer_path()
    if importer_path is not None:
        project_root = find_project_root(importer_path)
        add_python_dirs_to_syspath(project_root)
except:
    # Do nothing if a miscellaneous edge case occurred.
    # Eg a directory or file deleted at runtime, a security access exception, etc.
    pass
