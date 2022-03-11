import uuid

import pytest
from allauth.account.forms import SignupForm
from django.conf import settings
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


url = reverse("own_profile")


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        user = django_user_model.objects.create_user(**kwargs)
        return user

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(
            username=user.username,
            password=test_password,
            backend=settings.AUTHENTICATION_BACKENDS[0],
        )
        return client, user
    return make_auto_login


@pytest.mark.django_db
def test_correct_template_shown(auto_login_user):
    client, user = auto_login_user()
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "v2/profile/profile.html")


@pytest.mark.skip
def test_correct_forms_shown(client):
    response = client.get(url)
    form = response.context["form"]
    assert isinstance(form, SignupForm)
    # assertContains(response, "div_id_callsign")
    # the form is loaded as a NewUserForm, so we can't check
    # directly for the profileForm, so look for a profile
    # form control.
