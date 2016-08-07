from rest_framework import serializers

from main.models import Course, Instructor


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'title', 'description', 'general_requirements', 'repeatable',
            'grading', 'min_units', 'max_units', 'department', 'sections'
        )
        depth = 1
        
        
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = (
            'sunet', 'name', 'phone_number', 'bio'
        )