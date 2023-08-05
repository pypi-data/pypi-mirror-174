"""
Functions for working with miscellaneous
"""
import os
import sys
import typing as t

__all__ = [
    "maincli",
    "get_package_about",
    "get_package_requirements",
]


def maincli(fn: t.Callable, *args, **kwargs) -> None:
    """
    TODO
    """
    try:
        return fn(*args, **kwargs)
    except KeyboardInterrupt:
        # exit code could be success or error, it all depends on if it's the
        # normal way of quitting the app.
        pass
    except SystemExit as err:
        if isinstance(err.code, int):
            return err.code
        print(err, file=sys.stderr)
        return 1
    except Exception as err:  # pylint: disable=broad-except
        print(f"error: {err}", file=sys.stderr)
    return 1


def get_package_requirements() -> t.List:
    """
    TODO
    """
    with open("requirements.txt", encoding="UTF-8") as fd:
        requirements = fd.read().splitlines()
        requirements = [x for x in requirements if x and not x.startswith("--")]
        return requirements


def get_package_about(path=".") -> t.List:
    """
    TODO
    """
    about = {}

    for file in os.listdir(path):
        file = path + "/" + file
        if not os.path.isdir(file):
            continue
        if not os.path.exists(file + "/__about__.py"):
            continue
        with open(file + "/__about__.py", encoding="UTF-8") as fd:
            exec(fd.read(), None, about)  # pylint: disable=exec-used
        break

    about = {k: v for k, v in about.items() if k.startswith("__")}
    return about
