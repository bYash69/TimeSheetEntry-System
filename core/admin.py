from django.contrib import admin
from .models import Employee, Project, TimesheetEntry, ProjectHours, EmployeeProject


class EmployeeProjectInline(admin.TabularInline):
    model = EmployeeProject
    extra = 1
    verbose_name = "Assigned Project"
    verbose_name_plural = "Assigned Projects"
    autocomplete_fields = ['project']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'assigned_project_count']
    list_filter = ['is_active']
    search_fields = ['name']
    inlines = [EmployeeProjectInline]

    def assigned_project_count(self, obj):
        return obj.assigned_projects.count()
    assigned_project_count.short_description = 'Projects Assigned'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(EmployeeProject)
class EmployeeProjectAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project', 'assigned_at']
    list_filter = ['project', 'employee']
    search_fields = ['employee__name', 'project__code']


class ProjectHoursInline(admin.TabularInline):
    model = ProjectHours
    extra = 1


@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'status', 'total_hours', 'week_number']
    list_filter = ['status', 'year', 'month_number', 'employee']
    search_fields = ['employee__name', 'task_description']
    inlines = [ProjectHoursInline]
    date_hierarchy = 'date'