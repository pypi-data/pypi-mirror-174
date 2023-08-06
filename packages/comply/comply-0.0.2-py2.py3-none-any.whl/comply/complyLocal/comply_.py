import platform
import sys
import typing as t

default_min_msg = lambda v, min_vers, max_vers: print(
    f"Your python version is {v}. This program may break because it is currently only compatible with versions between {min_vers} and {max_vers}")

default_max_msg = lambda v, min_vers, max_vers: print(
    f"Your python version is {v}. This program may break because it is currently only compatible with versions between {min_vers} and {max_vers}")

default_compat_msg = lambda v: print(
    f"Your python version is {v} This program was tested with this version and runs properly. However, "
    f"if you notice a bug or if your version breaks at runtime please feel free to open a PR on github.")


def check(
        min_version: str,
        max_version: str,
        min_msg: t.Union[str, t.Callable] = default_min_msg,
        max_msg: t.Union[str, t.Callable] = default_max_msg,
        compatible_msg: t.Union[str, t.Callable] = default_compat_msg,
        verbose: bool = True,
        mock_sys_version: t.Union[str, bool] = False,

):
    def convert_int(coming_tuple_str) -> t.Tuple[int]:
        return tuple(map(lambda x: int(x), coming_tuple_str))

    def convert_str_to_version(version_as_str: str) -> t.Tuple[int]:
        return convert_int(tuple(version_as_str.split(".")))

    if mock_sys_version:
        v_ = convert_str_to_version(mock_sys_version)
        v = mock_sys_version
    else:
        v_ = platform.python_version_tuple()
        v = sys.version
    v_tuple: t.Tuple[int] = convert_int(v_)

    min_version_tuple: t.Tuple[int] = convert_str_to_version(min_version)
    max_version_tuple: t.Tuple[int] = convert_str_to_version(max_version)
    # callback: t.Callable = lambda: True

    assert isinstance(min_version_tuple, tuple)
    assert isinstance(max_version_tuple, tuple)

    if max_version_tuple < v_tuple:
        if verbose:
            if callable(max_msg):
                max_msg(v, min_version_tuple, max_version_tuple)
            else:
                print(f"Your python version is {v}", max_msg)

        return False
    elif min_version_tuple > v_tuple:
        if verbose:
            if callable(min_msg):
                min_msg(v, min_version_tuple, max_version_tuple)
            else:
                print(f"Your python version is {v}", min_msg)
        return False
    else:
        if verbose:
            if callable(compatible_msg):
                compatible_msg(v)
            else:
                print(f"Your python version is {v}", compatible_msg)
        return True
