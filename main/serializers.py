from rest_framework import serializers

from main.models import Course, Instructor, Review, Comment


class CommentRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return [CommentSerializer(item).data for item in value.get_queryset()]
    
class ContentObjectRelatedField(serializers.Field):
    CLASS_NAMES = {
        "course": Course,
        "instructor": Instructor,
        "review": Review,
        "comment": Comment
    }
    
    def get_attribute(self, obj):
        return obj
    
    def to_representation(self, obj):
        value = obj.content_object
        return type(value).__name__.lower() + ":" + str(value.pk)
    
    def to_internal_value(self, data):
        try:
            params = data.split(":")
            name = params[0]
            obj_id = params[1]
        except Exception:
            raise serializers.ValidationError("Invalid format: must be 'object:id'")
        try:
            query_obj = self.CLASS_NAMES[name]
        except KeyError:
            raise serializers.ValidationError("Object name must be: " + ", ".join([x[0] for x in CLASS_NAMES.items()]))
        try:
            if name == "instructor":
                return self.CLASS_NAMES[name].objects.get(sunet=obj_id)
            else:
                return self.CLASS_NAMES[name].objects.get(id=int(obj_id))
        except Exception as e:
            raise serializers.ValidationError(str(e))
            
class VotesField(serializers.Field):
    def to_representation(self, value):
        return value.all().count()
            
        
class CourseSerializer(serializers.ModelSerializer):
    comments = CommentRelatedField(read_only=True)
    
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'description', 'general_requirements',
            'repeatable', 'grading', 'min_units', 'max_units', 'department',
            'sections', 'reviews', 'comments', 'codes', 'average_rating',
            'grade_distribution',
        )
        read_only_fields = (
            'comments', 'average_rating', 'grade_distribution', 'id'
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
    helpful_votes = VotesField(read_only=True)
    unhelpful_votes = VotesField(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'course', 'rating', 'grade', 'text',
            'helpful_votes', 'unhelpful_votes', 'created_at', 'updated_at',
            'comments', 'author'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'helpful_votes', 'unhelpful_votes',
            'comments', 'author'
        )
        
        
class CommentSerializer(serializers.ModelSerializer):
    comments = CommentRelatedField(read_only=True)
    content_object = ContentObjectRelatedField()
    likes = VotesField(read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'content_object', 'text', 'likes', 'created_at',
            'updated_at', 'comments'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'likes', 'comments', 'author'
        )