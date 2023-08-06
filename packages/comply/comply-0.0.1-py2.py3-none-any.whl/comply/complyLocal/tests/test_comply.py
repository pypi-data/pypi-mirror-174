# from comply.complyLocal.comply_ import check
import comply
check = comply.check

# test


def test_check():
    check(
        min_version="3.7",
        max_version="3.11",

    )


def test_check_with_mock():
    assert check(
        min_version="3.7",
        max_version="3.11",
        mock_sys_version="2.7"
    ) is False

    assert check(
        min_version="3.7",
        max_version="3.11",
        mock_sys_version="3.8"
    ) is True


"""

def check_compat(
        min_version: str,
        max_version: str,
        min_msg: t.Union[str, t.Callable] = default_min_msg,
        max_msg: t.Union[str, t.Callable] = default_max_msg,
        compatible_msg: t.Union[str, t.Callable] = default_compat_msg,
        verbose: bool = True,
        mock_sys_version: t.Union[str, bool] = False,

):
"""


def test_check_compat_with_mock_msg(capsys):
    with capsys.disabled():
        assert check(
            min_version="3.7",
            max_version="3.11",
            mock_sys_version="2.7"
        ) is False
    with capsys.disabled():
        assert check(
            min_version="3.7",
            max_version="3.11",
            mock_sys_version="3.8"
        ) is True

    with capsys.disabled():
        assert check(
            min_version="3.7",
            max_version="3.11",
            mock_sys_version="3.4",
            min_msg="Your version is less than minimum.",
            verbose=True,

        ) is False

    with capsys.disabled():
        assert check(
            min_version="3.7",
            max_version="3.10",
            mock_sys_version="3.11",
            min_msg="Your version is greater than maximum that is compatible with ths package.",
            verbose=True,

        ) is False
