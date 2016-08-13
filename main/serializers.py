from rest_framework import serializers

from main.models import Course, Instructor, Review, Comment


class CommentRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return [CommentSerializer(item).data for item in value.get_queryset()]
    
class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return type(value).__name__.lower() + ":" + str(value.pk)


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
    comments = CommentRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'reply_to', 'rating', 'grade', 'text',
            'helpful_votes', 'unhelpful_votes', 'created_at', 'updated_at', 'comments'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'helpful_votes', 'unhelpful_votes', 'comments'
        )
        
        
class CommentSerializer(serializers.ModelSerializer):
    comments = CommentRelatedField(read_only=True)
    content_object = ContentObjectRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'content_object', 'text', 'likes', 'created_at',
            'updated_at', 'comments'
        )
        read_only_fields = (
            'content_object', 'created_at', 'updated_at', 'likes', 'comments'
        )