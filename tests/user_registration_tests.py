import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.urls import reverse
from factoryman import create_populated_modelfactory
from pytest_django.asserts import (
    assertTemplateUsed,
    assertContains,
    assertRedirects,
    assertFormError,
)

from airops.forms import NewUserForm

"""
test_email_is_generated_for_account_creation
test_error_shown_with_duplicated_call-sign
"""

url = reverse("register")


@pytest.mark.django_db
class TestRegistration:
    def test_correct_template_shown(self, client):
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "dashboard/register.html")

    def test_correct_forms_shown(self, client):
        response = client.get(url)
        form = response.context["form"]
        assert isinstance(form, NewUserForm)
        assertContains(response, "div_id_callsign")
        # the form is loaded as a NewUserForm, so we can't check
        # directly for the profileForm, so look for a profile
        # form control.

    def test_correct_default_timezone_shown(self, client):
        correct_selection = "selected>" + settings.TIME_ZONE
        response = client.get(url)
        assert str(response.content).find(correct_selection)

    def test_csrf_is_present(self, client):
        assertContains(client.get(url), "csrfmiddlewaretoken")

    def test_redirects_to_correct_page_on_successful_registration(self, client):
        valid_user = {
            "username": "Yeager",
            "first_name": "Chuck",
            "last_name": "Yeager",
            "email": "Chuck@NACA.gov.us",
            "password1": "TheRightStuff!",
            "password2": "TheRightStuff!",
            "callsign": "Chuck",
            "timezone": "US/Arizona",
        }
        response = client.post(url, data=valid_user)
        assertRedirects(response, reverse("campaign"))

    def test_authenticated_client_redirected_to_index(self, client, django_user_model):
        username = "user1"
        password = "bar"
        user = django_user_model.objects.create_user(
            username=username, password=password
        )
        client.force_login(user)
        response = client.get(url)
        assertRedirects(response, reverse("index"))

    def test_error_shown_with_invalid_username(self, client):
        username = ""
        password = "jyuiy1y181761jkg1ut119"
        response = client.post(
            url,
            data={"username": username, "password1": password, "password2": password},
        )
        assert response.status_code == 200
        assertFormError(
            response, "register_form", "username", "This field is required."
        )

    def test_error_shown_with_non_matching_password(self, client):
        username = "thisisvalid "
        password = "password"
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
            "register_form",
            "password2",
            "The two password fields didn’t match.",
        )

    def test_error_shown_with_invalid_email(self, client):
        username = "thisisvalid "
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
        assertFormError(
            response, "register_form", "email", "Enter a valid email address."
        )

    def test_error_shown_with_duplicated_username(self, django_user_model):
        username = "user1"
        password = "bar"
        user_ = django_user_model.objects.create_user(
            username=username, password=password
        )
        user_factory = create_populated_modelfactory(get_user_model())
        with pytest.raises(IntegrityError):
            duplicate_user = user_factory(username="user1")

    def test_error_shown_with_duplicated_email(self, client, django_user_model):

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
            "register_form",
            "email",
            "User with this Email address already exists.",
        )

    @pytest.mark.skip
    def test_error_shown_with_duplicated_callsign(self, client, django_user_model):
        username = "thisisvalid "
        password = "password"
        email = "valid@email.com"
        callsign = "Maverick"
        user_ = django_user_model.objects.create_user(
            username=username, password=password, email=email
        )
        user_.profile.callsign = callsign
        response = client.post(
            url,
            data={
                "username": username + "_",
                "password1": password,
                "password2": password,
                "email": email + ".au",
                "callsign": callsign,
            },
        )
        assert response.status_code == 200
        assertFormError(
            response,
            "profile_form",
            "callsign",
            "User with this Email address already exists.",
        )

    @pytest.mark.parametrize(
        "username, firstname, lastname, email, password1, password2, callsign, timezone, status_code",
        [
            (
                "valid_username",
                "first",
                "last",
                "email@email.com",
                "ValidPwd123",
                "ValidPwd123",
                "Callsign",
                "UTC",
                302,
            ),
            (
                "",
                "first",
                "last",
                "email@email.com",
                "ValidPwd123",
                "ValidPwd123",
                "Callsign",
                "UTC",
                200,
            ),
            (
                "valid_username",
                "",
                "last",
                "email@email.com",
                "ValidPwd123",
                "ValidPwd123",
                "Callsign",
                "UTC",
                302,
            ),
            (
                "valid_username",
                "",
                "",
                "email@email.com",
                "ValidPwd123",
                "ValidPwd123",
                "Callsign",
                "UTC",
                302,
            ),
            (
                "valid_username",
                "",
                "",
                "",
                "ValidPwd123",
                "ValidPwd123",
                "Callsign",
                "UTC",
                200,
            ),
            (
                "valid_username",
                "",
                "last",
                "email@email.com",
                "",
                "ValidPwd123",
                "Callsign",
                "UTC",
                200,
            ),
            (
                "valid_username",
                "",
                "last",
                "email@email.com",
                "ValidPwd123",
                "",
                "Callsign",
                "UTC",
                200,
            ),
            (
                "valid_username",
                "",
                "last",
                "email@email.com",
                "ValidPwd123",
                "ValidPwd123",
                "",
                "UTC",
                302,
            ),
            (
                "valid_username",
                "",
                "last",
                "email@email.com",
                "ValidPwd123",
                "ValidPwd123",
                "Callsign",
                "",
                200,
            ),
        ],
    )
    def test_registration_data_validation(
        self,
        username,
        firstname,
        lastname,
        email,
        password1,
        password2,
        callsign,
        timezone,
        status_code,
        client,
    ):
        data = {
            "username": username,  # required
            "first_name": firstname,
            "last_name": lastname,
            "email": email,  # required
            "password1": password1,  # required
            "password2": password2,  # required to match
            "callsign": callsign,
            "timezone": timezone,  # required
        }
        response = client.post(url, data=data)
        assert response.status_code == status_code
