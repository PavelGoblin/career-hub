from secforge.utils import format_table, detect_os


def test_format_table():
    rows = [["a", "b"], ["c", "d"]]
    result = format_table(rows, header=["X", "Y"])
    assert "+" in result
    assert "X" in result
    assert "Y" in result
    assert "a" in result
    assert "b" in result


def test_format_table_empty():
    assert format_table([]) == ""


def test_detect_os():
    os_val = detect_os()
    assert os_val in ("linux", "macos", "windows", "unknown")
