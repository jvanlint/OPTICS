import django.contrib.auth.models
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
import factory
from airops.forms import UserForm, ProfileForm
from airops.models import UserProfile

from django.db.models.signals import post_save


url = reverse("profile")


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    callsign = "FactoryBoy"
    # We pass in profile=None to prevent UserFactory from creating another profile
    # (this disables the RelatedFactory)
    user = factory.SubFactory("app.factories.UserFactory", profile=None)


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = django.contrib.auth.models.User

    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.Sequence(lambda n: "email_%d@spam.com" % n)

    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name="user")


@pytest.mark.django_db
class TestRegistration:
    @pytest.fixture
    def auto_login_user(self, client):
        def make_auto_login(user=None):
            if user is None:
                user = UserFactory()
            client.force_login(user)
            return client, user

        return make_auto_login

    def test_correct_template_shown(self, auto_login_user):
        client = auto_login_user()[0]
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "profiles/profile.html")

    def test_correct_forms_shown(self, auto_login_user):
        client = auto_login_user()[0]
        response = client.get(url)
        form = response.context["form"]
        assert isinstance(form, UserForm)
        assertContains(response, "div_id_callsign")
        # the form is loaded as a NewUserForm, so we can't check
        # directly for the profileForm, so look for a profile
        # form control.

    def test_csrf_is_present(self, auto_login_user):
        client = auto_login_user()[0]
        assertContains(client.get(url), "csrfmiddlewaretoken")

    def test_redirects_to_correct_page_on_successful_change(self, auto_login_user):
        client = auto_login_user()[0]
        valid_user = {
            "username": "Yeager",
            "first_name": "Chuck",
            "last_name": "Yeager",
            "email": "Chuck@NACA.gov.us",
            "callsign": "Chuck",
            "timezone": "US/Arizona",
        }
        response = client.post(url, data=valid_user)
        assertRedirects(response, reverse("campaign"))

    def test_error_shown_with_invalid_username(self, auto_login_user):
        client = auto_login_user()[0]
        response = client.post(
            url,
            data={
                "username": "",
            },
        )
        assert response.status_code == 200
        assertFormError(response, "user_form", "username", "This field is required.")

    def test_error_shown_with_invalid_email(self, auto_login_user):
        client = auto_login_user()[0]
        email = "invalid@email"
        response = client.post(
            url,
            data={
                "email": email,
            },
        )
        assert response.status_code == 200
        assertFormError(response, "user_form", "email", "Enter a valid email address.")

    def test_error_shown_with_duplicated_username(
        self, auto_login_user, django_user_model
    ):
        client = auto_login_user()[0]
        existing_user_ = django_user_model.objects.create_user(
            username="user1", password="bar"
        )
        response = client.post(
            url,
            data={
                "username": "user1",
            },
        )
        assert response.status_code == 200
        assertFormError(
            response,
            "user_form",
            "username",
            "A user with that username already exists.",
        )

    def test_error_shown_with_duplicated_email(
        self, auto_login_user, django_user_model
    ):
        client = auto_login_user()[0]
        username = "thisisvalid "
        password = "password"
        email = "valid@email.com"
        user_ = django_user_model.objects.create_user(
            username=username, password=password, email=email
        )
        response = client.post(
            url,
            data={
                "email": email,
            },
        )
        assert response.status_code == 200
        assertFormError(
            response,
            "user_form",
            "email",
            "User with this Email address already exists.",
        )

    def test_error_shown_with_duplicated_callsign(self, auto_login_user, django_user_model):
        client = auto_login_user()[0]
        username = "thisisvalid "
        password = "password"
        email = "valid@email.com"
        callsign = "Maverick"
        user_ = django_user_model.objects.create_user(
            username=username, password=password, email=email
        )
        # make a profile object, populate and save
        profile = UserProfile()
        profile.user = user_
        profile.callsign = callsign
        profile.save()

        response = client.post(
            url,
            data={
                "callsign": callsign,
            },
        )
        assert response.status_code == 200
        assertFormError(
            response,
            "profile_form",
            "callsign",
            "User profile with this Callsign already exists.",
        )

