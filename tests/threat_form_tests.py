import pytest
from ..forms import ThreatForm


@pytest.mark.parametrize(
    "values",
    [
        "---------",  # Note, this is the ModelChoiceField.empty_label default value
        "AAA",
        "SAM",
        "AIR",
        "NAVAL",
        "GROUND",
    ],
)
def test_support_type_has_correct_values(values):
    form = ThreatForm()
    assert [tup for tup in form.fields["threat_type"].choices if tup[1] == values]
