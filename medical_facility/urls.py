"""medical_facility URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from website import views as website


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', website.MainPageView.as_view(), name='main'),
    path('login/', website.LoginToWebsiteView.as_view(), name='login'),
    path('logout/', website.LogoutFromWebsiteView.as_view(), name='logout'),
    path('registration/', website.RegistrationView.as_view(), name='registration'),
    path('account/profile/', website.PatientAccountPanelView.as_view(), name='patient-panel'),
    path('account/book/', website.PatientChooseServiceView.as_view(), name='patient-choose'),
    path('account/book/<str:date_visit>/<str:time>/<int:doctor_pk>/<int:service_pk>/',
         website.PatientAppointmentCreateView.as_view(), name='patient-create-appointment'),
    path('account/book/<int:pk>/', website.PatientCancelAppointment.as_view(), name='patient-cancel'),
    path('account/opinion/', website.PatientAddOpinion.as_view(), name='patient-opinion'),

    path('account/profile/doctor/', website.DoctorAccountPanelView.as_view(), name='doctor-panel'),
    path('account/work/', website.DoctorAccountWorkView.as_view(), name='doctor-work'),
    path('account/patients/', website.DoctorPatientsView.as_view(), name='doctor-patients'),


    path('account/profile/administrator', website.AdministratorAccountPanelView.as_view(), name='admin-panel'),
    path('account/update/<int:pk>/', website.PatientAccountUpdateView.as_view(), name='patient-update'),
    path('about-us/privacy-policy-and-regulation/', website.PrivacyAndRegulationView.as_view(), name='policy-regulation'),
]

