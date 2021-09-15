import pytest
from ..forms import SupportForm


@pytest.mark.parametrize(
    "values",
    [
        "---------",  # Note, this is the ModelChoiceField.empty_label default value
        "AWACS",
        "TANKER",
        "JTAC",
        "CARRIER",
        "LHA",
        "ABM",
        "AIRFIELD",
    ],
)
def test_support_type_has_correct_values(values):
    form = SupportForm()
    assert [tup for tup in form.fields["support_type"].choices if tup[1] == values]
