from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['code']


class EmployeeProject(models.Model):
    """Superuser assigns which projects each employee can log hours on."""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_projects')
    project  = models.ForeignKey(Project,  on_delete=models.CASCADE, related_name='assigned_employees')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['employee', 'project']
        ordering = ['employee__name', 'project__code']

    def __str__(self):
        return f"{self.employee.name} → {self.project.code}"


class TimesheetEntry(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('holiday', 'Holiday'),
        ('leave', 'Leave'),
    ]

    date = models.DateField()
    year = models.IntegerField()
    week_number = models.IntegerField()
    month_number = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='entries')
    task_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    total_hours = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.employee.name}"

    class Meta:
        ordering = ['-date', 'employee']
        unique_together = ['date', 'employee']


class ProjectHours(models.Model):
    entry = models.ForeignKey(TimesheetEntry, on_delete=models.CASCADE, related_name='project_hours')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='hours')
    hours = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    def __str__(self):
        return f"{self.entry} - {self.project.code}: {self.hours}h"

    class Meta:
        unique_together = ['entry', 'project']