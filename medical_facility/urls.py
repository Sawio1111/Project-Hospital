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


    path('reset_password/', website.ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_sent/', website.ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', website.ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),


    path('account/profile/', website.PatientAccountPanelView.as_view(), name='patient-panel'),
    path('account/book/', website.PatientChooseServiceView.as_view(), name='patient-choose'),
    path('account/book/<str:date_visit>/<str:time>/<int:doctor_pk>/<int:service_pk>/',
         website.PatientAppointmentCreateView.as_view(), name='patient-create-appointment'),
    path('account/book/<int:pk>/', website.PatientCancelAppointment.as_view(), name='patient-cancel'),
    path('account/opinion/', website.PatientAddOpinion.as_view(), name='patient-opinion'),
    path('account/timeline/<int:patient_pk>/', website.PatientListAppointmentView.as_view(), name='patient-timeline'),
    path('account/update/<int:pk>/', website.PatientAccountUpdateView.as_view(), name='patient-update'),


    path('account/profile/doctor/', website.DoctorAccountPanelView.as_view(), name='doctor-panel'),
    path('account/work/', website.DoctorAccountWorkView.as_view(), name='doctor-work'),
    path('account/patients/', website.DoctorPatientsView.as_view(), name='doctor-patients'),
    path('account/appointment/<int:appointment_pk>/',
         website.DoctorStartAppointmentView.as_view(), name='doctor-start-appointment'),
    path('account/appointment/cancel/<int:appointment_pk>/',
         website.DoctorEndAppointmentView.as_view(), name='doctor-end-appointment'),


    path('account/profile/administrator', website.AdministratorAccountPanelView.as_view(), name='admin-panel'),
    path('account/service/create', website.AdministratorCreateServiceView.as_view(), name='admin-create-service'),
    path('account/service/delete/<int:pk>',
         website.AdministratorDeleteServiceView.as_view(), name='admin-delete-service'),
    path('account/opinion/list/', website.AdministratorListOpinionsView.as_view(), name='admin-list-opinions'),
    path('account/opinion/<int:opinion_pk>/',
         website.AdministratorOpinionStatusView.as_view(), name='admin-status-opinion'),
    path('account/doctors/', website.AdministratorListDoctorView.as_view(), name='admin-list-doctors'),
    path('account/doctors/create/', website.AdministratorCreateDoctorView.as_view(), name='admin-create-doctor'),
    path('account/doctors/update/<int:pk>/', website.AdministratorDoctorUpdateView.as_view(), name='admin-update-doctor'),
    path('account/qualification/update/<int:pk>/',
         website.AdministratorQualificationUpdateView.as_view(), name='admin-quali-doctor'),
    path('account/patients/update/<int:pk>/', website.AdministratorUpdatePatientView.as_view(),name='admin-update-patient'),
    path('account/patients/list/', website.AdministratorListPatientView.as_view(),name='admin-search-patient'),
    path('account/work/<int:date_pk>/', website.AdministratorDoctorWorkView.as_view(),name='admin-work-doctor'),

    path('about-us/privacy-policy-and-regulation/', website.PrivacyAndRegulationView.as_view(), name='policy-regulation'),
]

