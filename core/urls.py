from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'entries', views.TimesheetEntryViewSet, basename='timesheetentry')
router.register(r'assignments', views.EmployeeProjectViewSet)

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Superuser views
    path('', views.dashboard, name='dashboard'),
    path('timesheet/', views.all_timesheet_view, name='timesheet'),
    path('projects/', views.projects_view, name='projects'),
    path('employees/', views.employees_view, name='employees'),
    path('roles/', views.role_management_view, name='role_management'),
    path('export/', views.export_view, name='export'),
    path('export/excel/', views.export_excel, name='export_excel'),

    # Normal user view
    path('my-timesheet/', views.my_timesheet_view, name='my_timesheet'),

    # DRF API
    path('api/', include(router.urls)),
]