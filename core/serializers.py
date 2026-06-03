from rest_framework import serializers
from .models import Employee, Project, TimesheetEntry, ProjectHours, EmployeeProject
import datetime

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class EmployeeProjectSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source='project.code', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = EmployeeProject
        fields = ['id', 'project', 'project_code', 'project_name', 'assigned_at']


class EmployeeSerializer(serializers.ModelSerializer):
    assigned_projects = EmployeeProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'is_active', 'assigned_projects']


class ProjectHoursSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source='project.code', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectHours
        fields = ['id', 'project', 'project_code', 'project_name', 'hours']


class TimesheetEntrySerializer(serializers.ModelSerializer):
    project_hours = ProjectHoursSerializer(many=True, required=False)
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = TimesheetEntry
        fields = [
            'id', 'date', 'year', 'week_number', 'month_number',
            'employee', 'employee_name', 'task_description',
            'status', 'total_hours', 'project_hours', 'created_at', 'updated_at'
        ]
        read_only_fields = ['year', 'week_number', 'month_number']

    def validate_date(self, value):
        return value

    def create(self, validated_data):
        project_hours_data = validated_data.pop('project_hours', [])
        date = validated_data['date']
        validated_data['year'] = date.year
        validated_data['week_number'] = date.isocalendar()[1]
        validated_data['month_number'] = date.month
        entry = TimesheetEntry.objects.create(**validated_data)
        total = 0
        for ph in project_hours_data:
            ph_obj = ProjectHours.objects.create(entry=entry, **ph)
            total += ph_obj.hours
        entry.total_hours = total
        entry.save()
        return entry

    def update(self, instance, validated_data):
        project_hours_data = validated_data.pop('project_hours', None)
        date = validated_data.get('date', instance.date)
        validated_data['year'] = date.year
        validated_data['week_number'] = date.isocalendar()[1]
        validated_data['month_number'] = date.month
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if project_hours_data is not None:
            instance.project_hours.all().delete()
            total = 0
            for ph in project_hours_data:
                ph_obj = ProjectHours.objects.create(entry=instance, **ph)
                total += ph_obj.hours
            instance.total_hours = total
        instance.save()
        return instance