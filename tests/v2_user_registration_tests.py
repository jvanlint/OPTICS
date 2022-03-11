import uuid
import pytest
from allauth.account.forms import SignupForm
from allauth.utils import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.urls import reverse
from factoryman import create_populated_modelfactory
from model_bakery import baker
from pytest_django.asserts import (
    assertTemplateUsed,
    assertContains,
    assertRedirects,
    assertFormError,
)

# https://model-bakery.readthedocs.io/en/latest/index.html
# https://medium.com/insightfulsolutions/elegant-and-dry-test-data-creation-for-django-be68373c69d4
# Model-bakery _was_ model-mommy

from apps.airops.models import Squadron
# UserFactory = create_populated_modelfactory(User)
# CampaignFactory = create_populated_modelfactory(Campaign, creator=UserFactory())
url = reverse("account_signup")


@pytest.fixture
def valid_squadron(db):
    return baker.make(Squadron)


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


def test_correct_template_shown(db, client):
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "account/signup.html")


def test_correct_form_fields_shown(db):
    form = SignupForm()
    assert "username" in form.fields
    assert "email" in form.fields
    assert "password1" in form.fields
    assert "password2" in form.fields
    assert "squadron" in form.fields
    assert "timezone" in form.fields


def test_correct_default_timezone_shown(db, client):
    correct_selection = "selected>" + settings.TIME_ZONE
    response = client.get(url)
    assert str(response.content).find(correct_selection)


def test_csrf_is_present(db, client):
    assertContains(client.get(url), "csrfmiddlewaretoken")


def test_redirects_to_correct_page_on_successful_signup(db, client, valid_squadron):
    squadron = valid_squadron
    valid_user = {
        "username": "ChuckYeager",  # Note: Spaces in username is NOT allowed
        "email": "Chuck@NACA.gov.us",
        "password1": "TheRightStuff!",
        "password2": "TheRightStuff!",
        "timezone": "US/Arizona",
        "squadron": squadron.id,
    }
    response = client.post(url, data=valid_user)
    assertRedirects(response, reverse(settings.ACCOUNT_SIGNUP_REDIRECT_URL))
    # note: This test will fail when timezone data is not loaded in the form.


def test_signup_works_with_empty_squadron(db, client):
    valid_user = {
        "username": "ChuckYeager",  # Note: Spaces in username is NOT allowed
        "email": "Chuck@NACA.gov.us",
        "password1": "TheRightStuff!",
        "password2": "TheRightStuff!",
        "timezone": "US/Arizona",
        "squadron": 1,
    }
    response = client.post(url, data=valid_user)
    assertRedirects(response, reverse(settings.ACCOUNT_SIGNUP_REDIRECT_URL))


def test_valid_signup_creates_valid_user(db, client, valid_squadron):
    valid_signup = {
        "username": "Yeager",
        "email": "Chuck@NACA.gov.us",
        "password1": "TheRightStuff!",
        "password2": "TheRightStuff!",
        "timezone": "US/Arizona",
        "squadron": 3,
    }
    response = client.post(url, data=valid_signup)
    assert response.status_code == 302
    user = authenticate(
        username=valid_signup["username"], password=valid_signup["password1"]
    )
    if user is not None:
        assert user.profile.timezone == "US/Arizona"
        assert user.profile.squadron == valid_squadron
    else:
        assert False


def test_authenticated_client_redirected_to_index(db, client, django_user_model):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[1])
    response = client.get(url)
    assertRedirects(response, reverse(settings.ACCOUNT_SIGNUP_REDIRECT_URL))


def test_error_shown_with_invalid_username(db, client):
    username = ""
    password = "jyuiy1y181761jkg1ut119"
    response = client.post(
        url,
        data={"username": username, "password1": password, "password2": password},
    )
    assert response.status_code == 200
    assertFormError(response, "form", "username", "This field is required.")


def test_error_shown_with_non_matching_password(db, client):
    username = "thisisvalid "
    password = "jdu92y7812699132"
    response = client.post(
        url,
        data={
            "username": username,
            "password1": password,
            "password2": password + "2",
        },
    )
    assert response.status_code == 200
    assertFormError(
        response,
        "form",
        "password2",
        "You must type the same password each time.",
    )


def test_error_shown_with_invalid_email(db, client):
    username = "this is valid "
    password = "password"
    email = "invalid@email"
    response = client.post(
        url,
        data={
            "username": username,
            "password1": password,
            "password2": password,
            "email": email,
        },
    )
    assert response.status_code == 200
    assertFormError(response, "form", "email", "Enter a valid email address.")


def test_error_shown_with_duplicated_username(db, django_user_model):
    username = "user1"
    password = "bar"
    user_ = django_user_model.objects.create_user(username=username, password=password)
    user_factory = create_populated_modelfactory(get_user_model())
    with pytest.raises(IntegrityError):
        duplicate_user = user_factory(username="user1")


def test_error_shown_with_duplicated_email(db, client, django_user_model):

    username = "thisisvalid "
    password = "password"
    email = "valid@email.com"
    user_ = django_user_model.objects.create_user(
        username=username, password=password, email=email
    )
    response = client.post(
        url,
        data={
            "username": username,
            "password1": password,
            "password2": password,
            "email": email,
        },
    )
    assert response.status_code == 200
    assertFormError(
        response,
        "form",
        "email",
        "A user is already registered with this e-mail address.",
    )
