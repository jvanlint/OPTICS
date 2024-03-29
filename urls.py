from django.contrib.auth import views as auth_views
from django.urls import path, include

from airops import views

urlpatterns = [
    path('', views.campaigns_all, name='index'),

    path('campaign/<int:link_id>/', views.campaign_detail, name='campaign'),
    path('campaign', views.campaign, name='campaign'),
    path('campaign_detail/<int:link_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/add', views.campaign_create, name='campaign_add'),
    path('campaign/update/<int:link_id>', views.campaign_update, name='campaign_update'),
    path('campaign/delete/<int:link_id>', views.campaign_delete, name='campaign_delete'),
    path('campaign/filter', views.campaigns_filter, name='campaigns_filter'),

    path('mission/<int:link_id>/', views.mission, name='mission'),
    path('mission/add/<int:link_id>', views.mission_create, name='mission_add'),
    path('mission/update/<int:link_id>', views.mission_update, name='mission_update'),
    path('mission/delete/<int:link_id>', views.mission_delete, name='mission_delete'),
    path('mission/copy/<int:link_id>', views.mission_copy, name='mission_copy'),
    path('mission/signup/<int:link_id>', views.mission_signup, name='mission_signup'),
    path('mission/signup/update/<int:link_id>/<int:seat_id>', views.mission_signup_update, name='mission_signup_update'),
    path('mission/signup/remove/<int:link_id>/<int:seat_id>', views.mission_signup_remove, name='mission_signup_remove'),

    path('package/<int:link_id>/', views.package, name='package'),
    path('package/add/<int:link_id>', views.package_create, name='package_add'),
    path('package/update/<int:link_id>', views.package_update, name='package_update'),
    path('package/delete/<int:link_id>', views.package_delete, name='package_delete'),
    path('package/copy/<int:link_id>', views.package_copy, name='package_copy'),

    path('threat/add/<int:link_id>', views.threat_create, name='threat_add'),
    path('threat/update/<int:link_id>', views.threat_update, name='threat_update'),
    path('threat/delete/<int:link_id>', views.threat_delete, name='threat_delete'),
    path('threat/copy/<int:link_id>', views.threat_copy, name='threat_copy'),

    path('flight/<int:link_id>/', views.flight, name='flight'),
    path('flight/add/<int:link_id>', views.flight_create, name='flight_add'),
    path('flight/update/<int:link_id>', views.flight_update, name='flight_update'),
    path('flight/delete/<int:link_id>', views.flight_delete, name='flight_delete'),
    path('flight/copy/<int:link_id>', views.flight_copy, name='flight_copy'),

    path('aircraft/<int:link_id>/', views.aircraft, name='aircraft'),
    path('aircraft/add/<int:link_id>', views.aircraft_create, name='aircraft_add'),
    path('aircraft/update/<int:link_id>', views.aircraft_update, name='aircraft_update'),
    path('aircraft/delete/<int:link_id>', views.aircraft_delete, name='aircraft_delete'),
    path('aircraft/copy/<int:link_id>', views.aircraft_copy, name='aircraft_copy'),

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
    path('waypoint/copy/<int:link_id>', views.waypoint_copy, name='waypoint_copy'),

    path('mission_imagery/add/<int:link_id>', views.mission_imagery_create, name='mission_imagery_add'),
    path('mission_imagery/update/<int:link_id>', views.mission_imagery_update, name='mission_imagery_update'),
    path('mission_imagery/delete/<int:link_id>', views.mission_imagery_delete, name='mission_imagery_delete'),
    
    path('package_imagery/add/<int:link_id>', views.package_imagery_create, name='package_imagery_add'),
    path('package_imagery/update/<int:link_id>', views.package_imagery_update, name='package_imagery_update'),
    path('package_imagery/delete/<int:link_id>', views.package_imagery_delete, name='package_imagery_delete'),
    
    path('flight_imagery/add/<int:link_id>', views.flight_imagery_create, name='flight_imagery_add'),
    path('flight_imagery/update/<int:link_id>', views.flight_imagery_update, name='flight_imagery_update'),
    path('flight_imagery/delete/<int:link_id>', views.flight_imagery_delete, name='flight_imagery_delete'),

    path('pdf_view/mission/<int:mission_id>/flight/<int:flight_id>', views.view_mission_card, name='pdf_view'),
    path('pdf_download/mission/<int:mission_id>/flight/<int:flight_id>', views.download_mission_card, name='pdf_download'),
]

# Dashboard URL Patterns - V2

urlpatterns += [
    path('dashboard/', views.mission_dashboard, name='mission_dashboard'),
]

# About URL Patterns - V2

urlpatterns += [
    path('about/', views.about, name='about'),
]


# Campaign URL Patterns - V2
urlpatterns += [
    path('v2/', views.campaigns_all, name='home'),
    path('v2/campaign/', views.campaign_redirect),
    path('v2/campaigns/', views.campaigns_all, name='campaigns'),
    path('v2/campaign/<int:link_id>/', views.campaign_detail_v2, name='campaign_detail_v2'),
    path("v2/campaign/add", views.campaign_add_v2, name="campaign_add_v2"),
    path('v2/campaign/update/<int:link_id>', views.campaign_update_v2, name='campaign_update_v2'),
    path('v2/campaign/<int:link_id>/', views.campaign_detail_v2, name='campaign_detail_v2'),
    path("v2/campaign/delete/<int:link_id>", views.campaign_delete_v2, name="campaign_delete_v2"),
    
    # Comments
    path('v2/campaign/comment/add', views.campaign_add_comment, name='campaign_add_comment'),
    path("v2/campaign/comment/delete/<int:link_id>", views.campaign_delete_comment,
      name="campaign_delete_comment"),
    path("v2/campaign/comment/edit/<int:link_id>", views.campaign_edit_comment,
        name="campaign_edit_comment"),
    path('v2/campaign/comment/show', views.campaign_show_comments, name='campaign_show_comments'),
    path('v2/campaign/comment/update/<int:link_id>', views.campaign_update_comment, name='campaign_update_comment'),
]

# Mission URL Patterns - V2
urlpatterns += [
    path('v2/mission/<int:link_id>', views.mission_v2, name='mission_v2'),
    path('v2/mission/add/<int:link_id>', views.mission_add_v2, name='mission_add_v2'),
    path('v2/mission/update/<int:link_id>', views.mission_update_v2, name='mission_update_v2'),
    path("v2/mission/delete/<int:link_id>", views.mission_delete_v2, name="mission_delete_v2"),
    path('v2/mission/copy/<int:link_id>', views.mission_copy_v2, name='mission_copy_v2'),
          
    path('v2/mission/add/file', views.mission_file_add, name='mission_file_add'),
    path("v2/mission/file/delete/<int:link_id>", views.mission_file_delete, name="mission_file_delete"),
         
    path('mission/add/image/<int:link_id>', views.mission_imagery_create_v2, name='mission_imagery_add_v2'),
    path('mission/update/image/<int:link_id>', views.mission_imagery_update_v2, name='mission_imagery_update_v2'),
    path('mission/delete/image/<int:link_id>', views.mission_imagery_delete_v2, name='mission_imagery_delete_v2'),
    
    path('v2/mission/signup/<int:link_id>', views.mission_signup_v2, name='mission_signup_v2'),
    
    # Comments
    path('v2/mission/comment/add', views.mission_add_comment, name='mission_add_comment'),
    path("v2/mission/comment/delete/<int:link_id>", views.mission_delete_comment,
      name="mission_delete_comment"),
    path("v2/mission/comment/edit/<int:link_id>", views.mission_edit_comment,
        name="mission_edit_comment"),
    path('v2/mission/comment/show', views.mission_show_comments, name='mission_show_comments'),
    path('v2/mission/comment/update/<int:link_id>', views.mission_update_comment, name='mission_update_comment'),
]

# Package URL Patterns - V2
urlpatterns += [
    path('v2/package/<int:link_id>', views.package_v2, name='package_v2'),
    path('v2/package/add/<int:link_id>', views.package_add_v2, name='package_add_v2'),
    path('v2/package/update/<int:link_id>', views.package_update_v2, name='package_update_v2'),
    path("v2/package/delete/<int:link_id>", views.package_delete_v2, name="package_delete_v2"),
    
    path('package/add/image/<int:link_id>', views.package_imagery_create_v2, name='package_imagery_add_v2'),
    path('package/update/image/<int:link_id>', views.package_imagery_update_v2, name='package_imagery_update_v2'),
    path('package/delete/image/<int:link_id>', views.package_imagery_delete_v2, name='package_imagery_delete_v2'),
    
    # Comments
    path('v2/package/comment/add', views.package_add_comment, name='package_add_comment'),
    path("v2/package/comment/delete/<int:link_id>", views.package_delete_comment,
      name="package_delete_comment"),
    path("v2/package/comment/edit/<int:link_id>", views.package_edit_comment,
        name="package_edit_comment"),
    path('v2/package/comment/show', views.package_show_comments, name='package_show_comments'),
    path('v2/package/comment/update/<int:link_id>', views.package_update_comment, name='package_update_comment'),
]

# Flight URL Patterns - V2
urlpatterns += [
    path('v2/flight/<int:link_id>', views.flight_v2, name='flight_v2'),
    path('v2/flight/add/<int:link_id>', views.flight_add_v2, name='flight_add_v2'),
    path('v2/flight/update/<int:link_id>', views.flight_update_v2, name='flight_update_v2'),
    path("v2/flight/delete/<int:link_id>", views.flight_delete_v2, name="flight_delete_v2"),
    path("v2/flight/copy/<int:link_id>", views.flight_copy_v2, name="flight_copy_v2"),
    
    path('flight/add/image/<int:link_id>', views.flight_imagery_create_v2, name='flight_imagery_add_v2'),
    path('flight/update/image/<int:link_id>', views.flight_imagery_update_v2, name='flight_imagery_update_v2'),
    path('flight/delete/image/<int:link_id>', views.flight_imagery_delete_v2, name='flight_imagery_delete_v2'),
    
    # Comments
    path('v2/flight/comment/add', views.flight_add_comment, name='flight_add_comment'),
    path("v2/flight/comment/delete/<int:link_id>", views.flight_delete_comment,
      name="flight_delete_comment"),
    path("v2/flight/comment/edit/<int:link_id>", views.flight_edit_comment,
        name="flight_edit_comment"),
    path('v2/flight/comment/show', views.flight_show_comments, name='flight_show_comments'),
    path('v2/flight/comment/update/<int:link_id>', views.flight_update_comment, name='flight_update_comment'),
]

# Aircraft URL Patterns - V2
urlpatterns += [
    path('v2/aircraft/add/<int:link_id>', views.aircraft_add_v2, name='aircraft_add_v2'),
    path('v2/aircraft/update/<int:link_id>', views.aircraft_update_v2, name='aircraft_update_v2'),
    path("v2/aircraft/delete/<int:link_id>", views.aircraft_delete_v2, name="aircraft_delete_v2"),
    path('v2/aircraft/copy/<int:link_id>', views.aircraft_copy_v2, name='aircraft_copy_v2'),
]

# Waypoint URL Patterns - V2
urlpatterns += [
    path('v2/waypoint/add/<int:link_id>', views.waypoint_add_v2, name='waypoint_add_v2'),
    path('v2/waypoint/update/<int:link_id>', views.waypoint_update_v2, name='waypoint_update_v2'),
    path("v2/waypoint/delete/<int:link_id>", views.waypoint_delete_v2, name="waypoint_delete_v2"),
    path('v2/waypoint/copy/<int:link_id>', views.waypoint_copy_v2, name='waypoint_copy_v2'),
]

# Target URL Patterns - V2
urlpatterns += [
    path('v2/target/add/<int:link_id>', views.target_add_v2, name='target_add_v2'),
    path('v2/target/update/<int:link_id>', views.target_update_v2, name='target_update_v2'),
    path("v2/target/delete/<int:link_id>", views.target_delete_v2, name="target_delete_v2"),
]

# Threat URL Patterns - V2
urlpatterns += [
    path('v2/threat/add/<int:link_id>', views.threat_add_v2, name='threat_add_v2'),
    path('v2/threat/update/<int:link_id>', views.threat_update_v2, name='threat_update_v2'),
    path("v2/threat/delete/<int:link_id>", views.threat_delete_v2, name="threat_delete_v2"),
]

# Support URL Patterns - V2
urlpatterns += [
    path('v2/support/add/<int:link_id>', views.support_add_v2, name='support_add_v2'),
    path('v2/support/update/<int:link_id>', views.support_update_v2, name='support_update_v2'),
    path("v2/support/delete/<int:link_id>", views.support_delete_v2, name="support_delete_v2"),
]

# Reference URL Patterns - V2
urlpatterns += [
    path('reference/', views.reference_tables, name='reference_tables'),
    path('referenceobject/add/<str:table>', views.reference_object_add, name='reference_object_add'),
    path('referenceobject/update/<int:link_id>/<str:table>', views.reference_object_update, name='reference_object_update'),
    path('referenceobject/delete/<int:link_id>/<str:table>', views.reference_object_delete, name='reference_object_delete'),
    path('reference/waypoint_type_page', views.waypoint_type_page_manager, name='waypoint_type_page_manager'),
    path('reference/airframe_page', views.airframe_page_manager, name='airframe_page_manager'),
    path('reference/flight_task_page', views.flight_task_page_manager, name='flight_task_page_manager'),
    path('reference/campaign_status_page', views.campaign_status_page_manager, name='campaign_status_page_manager'),
    path('reference/terrain_page', views.terrain_page_manager, name='terrain_page_manager'),
    path('reference/support_type_page', views.support_type_page_manager, name='support_type_page_manager'),
    path('reference/threat_type_page', views.threat_type_page_manager, name='threat_type_page_manager'),
]

# Profile URL Patterns - V2
urlpatterns += [
    path("v2/profile/", views.own_profile_view, name="own_profile"),
    path("v2/profile/<int:link_id>", views.user_profile_view, name="user_profile"),
    path("v2/avatar_select", views.select_avatar, name="select_avatar"),
    path("v2/avatar_change", views.change_avatar, name="avatar_change"),
]

# User Password and Access Management URL Patterns

urlpatterns += [
    
    path("change_password/", auth_views.PasswordChangeView.as_view(
        template_name="authentication/change_password.html"), name="change_password_v2"),
]





