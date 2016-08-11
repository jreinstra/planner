from rest_framework import serializers

from main.models import Course, Instructor, Review, Comment


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
        
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id', 'reply_to', 'rating', 'grade', 'text',
            'helpful_votes', 'unhelpful_votes', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'helpful_votes', 'unhelpful_votes'
        )
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'author','reply_to', 'text', 'likes', 'created_at',
            'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'likes')