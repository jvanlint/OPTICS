import pytest
from pytest_django.asserts import assertTemplateUsed, assertContains, assertRedirects
from django.urls import reverse
from django.conf import settings
from airops.forms import NewUserForm

"""
test_redirects_to_correct_page_on_successful_registration
test_email_is_generated_for_account_creation

test_error_shown_with_duplicated_call-sign
test_error_shown_with_duplicated_username
test_error_shown_with_duplicated_email
test_error_shown_with_invalid_timezone
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
            "username": "GOAT",
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

    @pytest.mark.skip
    def test_error_shown_with_invalid_username(self, client, django_user_model):
        username = ""
        password = "jyuiy1y181761jkg1ut119"
        # user = django_user_model.objects.create_user(
        #     username=username, password=password
        # )
        response = client.post(
            url,
            date={"username": username, "password1": password, "password2": password},
        )
        form = NewUserForm()

        assertRedirects(response, reverse("index"))

    # < option
    # value = "Australia/Melbourne"
    # selected = "" > Australia / Melbourne < / option >
    # 0['Australia/Melbourne']

    @pytest.mark.skip
    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            (None, None, 400),
            (None, "strong_pass", 400),
            ("user@example.com", None, 400),
            ("user@example.com", "invalid_pass", 400),
            ("user@example.com", "strong_pass", 201),
        ],
    )
    def test_login_data_validation(self, email, password, status_code, client):
        data = {"email": email, "password": password}
        response = client.post(url, data=data)
        assert response.status_code == status_code
