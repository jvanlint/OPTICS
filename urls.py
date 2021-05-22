from django.urls import path
from . import views

urlpatterns = [
    path('', views.campaign, name='index'),

    path('campaign/<int:link_id>/', views.campaign_detail, name='campaign'),
    path('campaign', views.campaign, name='campaign'),
    path('campaign_detail/<int:link_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/add', views.campaign_create, name='campaign_add'),
    path('campaign/update/<int:link_id>', views.campaign_update, name='campaign_update'),
    path('campaign/delete/<int:link_id>', views.campaign_delete, name='campaign_delete'),

    path('mission/<int:link_id>/', views.mission, name='mission'),
    path('mission/add/<int:link_id>', views.mission_create, name='mission_add'),
    path('mission/update/<int:link_id>', views.mission_update, name='mission_update'),
    path('mission/delete/<int:link_id>', views.mission_delete, name='mission_delete'),

    path('package/<int:link_id>/', views.package, name='package'),
    path('package/add/<int:link_id>', views.package_create, name='package_add'),
    path('package/update/<int:link_id>', views.package_update, name='package_update'),
    path('package/delete/<int:link_id>', views.package_delete, name='package_delete'),

    path('threat/add/<int:link_id>', views.threat_create, name='threat_add'),
    path('threat/update/<int:link_id>', views.threat_update, name='threat_update'),
    path('threat/delete/<int:link_id>', views.threat_delete, name='threat_delete'),

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

    path('support/add/<int:link_id>', views.support_create, name='support_add'),
    path('support/update/<int:link_id>', views.support_update, name='support_update'),
    path('support/delete/<int:link_id>', views.support_delete, name='support_delete'),

    path('waypoint/add/<int:link_id>', views.waypoint_create, name='waypoint_add'),
    path('waypoint/update/<int:link_id>', views.waypoint_update, name='waypoint_update'),
    path('waypoint/delete/<int:link_id>', views.waypoint_delete, name='waypoint_delete'),

    path('dashboard', views.dashboard),

    path("register", views.register_request, name="register"),

    path("login", views.login_request, name="login"),

    path("logout", views.logout_request, name="logout"),

    path('pdf_view/mission/<int:mission_id>/flight/<int:flight_id>', views.view_mission_card, name="pdf_view"),
    path('pdf_download/mission/<int:mission_id>/flight/<int:flight_id>', views.download_mission_card, name="pdf_download"),

]
