import pytest

from stellarphot.io import AAVSOExtendedFileFormat

DEFAULT_OBSCODE = "ABCDE"


def test_no_obscode_raises_error():
    with pytest.raises(TypeError, match="observer_code"):
        aef = AAVSOExtendedFileFormat()


def test_default_values():
    aef = AAVSOExtendedFileFormat(DEFAULT_OBSCODE)
    assert aef.delim == ","
