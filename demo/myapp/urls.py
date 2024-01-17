from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home/", views.home, name="home"),
    path("create_wo/", views.create_wo, name="create_wo"),
    path("overview/", views.overview, name='overview'),
    path("finished_wo/", views.finished_wo, name='finished_wo'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # CREATE WO
    path('create_wo/mp_emr_traditional_internal/<str:pricing_type>/<str:company_type>/<str:project_type>', views.mp_emr_traditional_internal , name ='mp_emr_traditional_internal'),
    path('create_wo/mp_ln_traditional_internal_odn/<str:pricing_type>/<str:company_type>/<str:project_type>', views.mp_ln_traditional_internal_odn , name ='mp_ln_traditional_internal_odn'),
    path('create_wo/material_emr/<str:company_type>/<str:project_type>', views.material_emr , name ='material_emr'),
    path('create_wo/material_ln/<str:company_type>/<str:project_type>', views.material_ln , name ='material_ln'),
    path('create_wo/oc_emr/<str:company_type>/<str:project_type>', views.oc_emr , name ='oc_emr'),
    path('create_wo/oc_ln/<str:company_type>/<str:project_type>', views.oc_ln , name ='oc_ln'),
    path('create_wo/donation_emr/<str:company_type>/<str:project_type>', views.donation_emr , name ='donation_emr'),
    path('create_wo/donation_ln/<str:company_type>/<str:project_type>', views.donation_ln , name ='donation_ln'),

    # VIEW WO
    path('view_wo/<int:id>/<str:category>/<str:company>/<str:project>', views.view_wo, name='view_wo'),
    # REQUEST FORM
    path('request_form/<int:id>/<str:category>/<str:company>/<str:project>', views.request_form, name='request_form'),

    # EDIT WO
    path('edit_wo/<int:id>/<str:category>/<str:project>', views.edit_wo, name='edit_wo'),

    path('wo_submitted/', views.wo_submitted , name ="wo_submitted"),
    path('delete_attachment/<int:id>/', views.delete_attachment, name='delete_attachment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)