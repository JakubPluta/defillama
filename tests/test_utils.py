import datetime
import pytest
from defillama.utils import convert_to_timestamp


@pytest.mark.parametrize(
    "input, expected",
    [
        (datetime.date(2022, 1, 1), int(datetime.datetime(2022, 1, 1).timestamp())),
        (
            datetime.datetime(2022, 1, 1, 12, 0, 0),
            int(datetime.datetime(2022, 1, 1, 12, 0, 0).timestamp()),
        ),
        ("2022-01-01", int(datetime.datetime(2022, 1, 1).timestamp())),
        ("01-01-2022", 1640991600),
        (1641024000, 1641024000),
        (True, TypeError),
    ],
)
def test_convert_to_timestamp(input, expected):
    if expected in (TypeError, ValueError, Exception):
        with pytest.raises(expected):
            convert_to_timestamp(input)
    else:
        assert convert_to_timestamp(input) == expected
