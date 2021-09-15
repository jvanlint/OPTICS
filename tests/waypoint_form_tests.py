import pytest
from ..forms import WaypointForm


@pytest.mark.parametrize(
    "values",
    [
        "---------",  # Note, this is the ModelChoiceField.empty_label default value
        "NAV",
        "IP",
        "CAP",
        "STRIKE",
        "CAS",
        "DEAD",
        "SEAD",
        "BAI",
        "TAKEOFF",
        "LAND",
        "DIVERT",
    ],
)
def test_waypoint_type_has_correct_values(db, values):
    form = WaypointForm()
    assert [tup for tup in form.fields["waypoint_type"].choices if tup[1] == values]
