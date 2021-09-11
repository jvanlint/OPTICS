import pytest
from allauth.account.forms import SignupForm
from allauth.utils import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.urls import reverse
from factoryman import create_populated_modelfactory

# https://medium.com/insightfulsolutions/elegant-and-dry-test-data-creation-for-django-be68373c69d4
from pytest_django.asserts import (
    assertTemplateUsed,
    assertContains,
    assertRedirects,
    assertFormError,
)

from airops.models import UserProfile, Campaign

from model_bakery import baker


# https://model-bakery.readthedocs.io/en/latest/index.html


@pytest.fixture
def make_user_record():
    def _make_user_record():
        return baker.prepare(UserProfile).user

    return _make_user_record


@pytest.fixture
def make_campaign():
    def _make_campaign(user):
        return baker.prepare("airops.campaign", creator=user)

    return _make_campaign


def test_users_can_create_campaigns(make_user_record, make_campaign):
    user1 = make_user_record()
    user2 = make_user_record()
    campaign1 = make_campaign(user1)
    campaign2 = make_campaign(user2)
    assert user1 != user2
    assert campaign1.creator != campaign2.creator


def test_creator_can_edit_their_campaign(make_user_record, make_campaign):
    creator = make_user_record()
    campaign = make_campaign(creator)
    assert campaign.creator == creator


'''
campaign model will have a editors many-many field to users for allowed editors
campaign model will have a editor-requests many-many field for users requesting editing permission.
campaign creator will get a UI element on campaign screen when there are users in the editor-requests field
    listing them and allowing assigning or declining editor permission.
        When allowed, the user is moved to the editors field.
        When declined, user is removed from the editor-requests field
Campaign main page will have a list of editors 
Campaign main page will have a button or control to request editor permission.
When viewing Campaigns and their children, only creators and editors will see edit controls.
When POSTing changes to campiagns and children request.user will be checked against the creator and editor fields
    for permission.
    
'''




# url = reverse("account_signup")

#
# def test_correct_template_shown(client):
#     response = client.get(url)
#     assert response.status_code == 200
#     assertTemplateUsed(response, "account/signup.html")
#
#
# def test_correct_form_fields_shown():
#     form = SignupForm()
#     assert "username" in form.fields
#     assert "email" in form.fields
#     assert "password1" in form.fields
#     assert "password2" in form.fields
#     assert "squadron" in form.fields
#     assert "timezone" in form.fields
#
#
# def test_correct_default_timezone_shown(db, client):
#     correct_selection = "selected>" + settings.TIME_ZONE
#     response = client.get(url)
#     assert str(response.content).find(correct_selection)

# # pytest import
# import pytest
#
# # Third-party app imports
# from model_bakery import baker
#
# from shop.models import Customer
#

#
# @pytest.fixture
# def make_customer_record():
#     def _make_customer_record(name):
#         return {"name": name, "orders": []}
#
#     return _make_customer_record
#
#
# def test_customer_records(make_customer_record):
#     customer_1 = make_customer_record("Lisa")
#     customer_2 = make_customer_record("Mike")
#     customer_3 = make_customer_record("Meredith")
# #
