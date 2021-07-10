from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.campaign, name='index'),

    path('campaign/<int:link_id>/', views.campaign_detail, name='campaign'),
    path('campaign', views.campaign, name='campaign'), path('campaign_detail/<int:link_id>/',
                                                            views.campaign_detail, name='campaign_detail'),
    path('campaign/add', views.campaign_create, name='campaign_add'),
    path('campaign/update/<int:link_id>', views.campaign_update, name='campaign_update'),
    path('campaign/delete/<int:link_id>', views.campaign_delete, name='campaign_delete'),

    path('mission/<int:link_id>/', views.mission, name='mission'),
    path('mission/add/<int:link_id>', views.mission_create, name='mission_add'),
    path('mission/update/<int:link_id>', views.mission_update, name='mission_update'),
    path('mission/delete/<int:link_id>', views.mission_delete, name='mission_delete'),
    path('mission/signup/<int:link_id>', views.mission_signup, name='mission_signup'),
    path('mission/signup/update/<int:link_id>/<int:seat_id>', views.mission_signup_update, name='mission_signup_update'),
    path('mission/signup/remove/<int:link_id>/<int:seat_id>', views.mission_signup_remove, name='mission_signup_remove'),

    path('package/<int:link_id>/', views.package, name='package'),
    path('package/add/<int:link_id>', views.package_create, name='package_add'),
    path('package/update/<int:link_id>', views.package_update, name='package_update'),
    path('package/delete/<int:link_id>', views.package_delete, name='package_delete'),

    path('threat/add/<int:link_id>', views.threat_create, name='threat_add'),
    path('threat/update/<int:link_id>', views.threat_update, name='threat_update'),
    path('threat/delete/<int:link_id>', views.threat_delete, name='threat_delete'),
    path('threat/copy/<int:link_id>', views.threat_copy, name='threat_copy'),

    path('flight/<int:link_id>/', views.flight, name='flight'),
    path('flight/add/<int:link_id>', views.flight_create, name='flight_add'),
    path('flight/update/<int:link_id>', views.flight_update, name='flight_update'),
    path('flight/delete/<int:link_id>', views.flight_delete, name='flight_delete'),

    path('aircraft/<int:link_id>/', views.aircraft, name='aircraft'),
    path('aircraft/add/<int:link_id>', views.aircraft_create, name='aircraft_add'),
    path('aircraft/update/<int:link_id>', views.aircraft_update, name='aircraft_update'),
    path('aircraft/delete/<int:link_id>', views.aircraft_delete, name='aircraft_delete'),

    path('target/add/<int:link_id>', views.target_create, name='target_add'),
    path('target/update/<int:link_id>', views.target_update, name='target_update'),
    path('target/delete/<int:link_id>', views.target_delete, name='target_delete'),
    path('target/copy/<int:link_id>', views.target_copy, name='target_copy'),

    path('support/add/<int:link_id>', views.support_create, name='support_add'),
    path('support/update/<int:link_id>', views.support_update, name='support_update'),
    path('support/delete/<int:link_id>', views.support_delete, name='support_delete'),
    path('support/copy/<int:link_id>', views.support_copy, name='support_copy'),

    path('waypoint/add/<int:link_id>', views.waypoint_create, name='waypoint_add'),
    path('waypoint/update/<int:link_id>', views.waypoint_update, name='waypoint_update'),
    path('waypoint/delete/<int:link_id>', views.waypoint_delete, name='waypoint_delete'),

    path('mission_imagery/add/<int:link_id>', views.mission_imagery_create, name='mission_imagery_add'),
    path('mission_imagery/update/<int:link_id>', views.mission_imagery_update, name='mission_imagery_update'),
    path('mission_imagery/delete/<int:link_id>', views.mission_imagery_delete, name='mission_imagery_delete'),

    path('dashboard', views.dashboard),

    path("register", views.register_request, name="register"),

    path("login", views.login_request, name="login"),

    path("logout", views.logout_request, name="logout"),

    path("changepassword", views.change_password, name="changepassword"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_done.html'),
         name='password_reset_complete'),

    path('pdf_view/mission/<int:mission_id>/flight/<int:flight_id>', views.view_mission_card, name="pdf_view"),
    path('pdf_download/mission/<int:mission_id>/flight/<int:flight_id>', views.download_mission_card,
         name="pdf_download"),

]
