from django.urls import path
from . import views

urlpatterns = [
    path('', views.campaign, name='index'),

    path('campaign/<int:link_id>/', views.campaign_detail, name='campaign'),
    path('campaign', views.campaign, name='campaign'),
    path('campaign_detail/<int:link_id>/',
         views.campaign_detail, name='campaign_detail'),
    path('campaign/add', views.campaign_create, name='campaign_add'),
    path('campaign/update/<int:link_id>',
         views.campaign_update, name='campaign_update'),
    path('campaign/delete/<int:link_id>',
         views.campaign_delete, name='campaign_delete'),

    path('mission/<int:link_id>/', views.mission, name='mission'),
    path('mission/add/<int:link_id>', views.mission_create, name='mission_add'),
    path('mission/update/<int:link_id>',
         views.mission_update, name='mission_update'),
    path('mission/delete/<int:link_id>',
         views.mission_delete, name='mission_delete'),

    path('package/<int:link_id>/', views.package, name='package'),
    path('package/add/<int:link_id>', views.package_create, name='package_add'),
    path('package/update/<int:link_id>',
         views.package_update, name='package_update'),
    path('package/delete/<int:link_id>',
         views.package_delete, name='package_delete'),

    path('dashboard', views.dashboard),

    path("register", views.register_request, name="register"),

    path("login", views.login_request, name="login"),

    path("logout", views.logout_request, name="logout"),
]
