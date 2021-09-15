import pytest
from ..forms import WaypointForm


@pytest.mark.parametrize(
    "waypoint_type_value",
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
def test_waypoint_type_has_correct_values(waypoint_type_value):
    form = WaypointForm()
    assert [
        tup
        for tup in form.fields["waypoint_type"].choices
        if tup[1] == waypoint_type_value
    ]
