from rest_framework import serializers

from django.contrib.auth.models import User
from main.models import *


class CommentRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return [CommentSerializer(item).data for item in value.get_queryset()]
    
    
class ReviewRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        q = value.get_queryset().exclude(
            text="No review written."
        ).exclude(
            text=""
        ).order_by('-created_at')[:5]
        return [ReviewSerializer(item).data for item in q]
    
    
class CodeRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return [CodeSerializer(item).data for item in value.get_queryset()]
    
    
class SectionRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        result = []
        term_sections = []
        for item in value.get_queryset():
            data = InlineSectionSerializer(item).data
            term_section = data["term"] + "_-_" + str(data["section_number"])
            if term_section not in term_sections:
                result.append(data)
                term_sections.append(term_section)
        return result
    
    
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
    
    
class CourseDataField(serializers.Field):
    SEASONS = ["autumn", "winter", "spring", "summer"]
    
    def get_attribute(self, obj):
        return obj
    
    def to_representation(self, obj):
        result = {}
        for season in self.SEASONS:
            result[season] = [CourseSerializer(c).data for c in getattr(obj, season).all()]
            
        return result
            
        
class CourseSerializer(serializers.ModelSerializer):
    comments = CommentRelatedField(read_only=True)
    reviews = ReviewRelatedField(read_only=True)
    codes = CodeRelatedField(read_only=True)
    prerequisites = CodeRelatedField(read_only=True)
    sections = SectionRelatedField(read_only=True)
    
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'description', 'general_requirements',
            'repeatable', 'grading', 'min_units', 'max_units', 'department',
            'sections', 'reviews', 'comments', 'codes', 'average_rating',
            'grade_distribution', 'median_grade', 'instructors', 'prerequisites'
        )
        read_only_fields = (
            'average_rating', 'grade_distribution', 'id', 'sections', 'comments', 'reviews'
        )
        
        
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = (
            'sunet', 'name', 'email', 'phone_number', 'bio', 'sections', 'courses'
        )
        depth = 1
        
        
class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCode
        fields = (
            'code', 'alt_code', 'title', 'course'
        )
        
        
class InlineSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = (
            'id', 'year', 'term', 'section_number', 'num_enrolled',
            'max_enrolled', 'num_waitlist', 'max_waitlist', 'enroll_status',
            'instructor', 'start_date', 'end_date', 'start_time', 'end_time',
            'days', 'component'
        )
        depth = 1
        
        
class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = (
            'id', 'department', 'degree_type', 'name'
        )
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'code', 'name', 'school', 'description_html'
        )
        
        
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'degrees', 'years')
        read_only_fields = ('id', 'years')
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'username')
        
        
class PlanYearSerializer(serializers.ModelSerializer):
    course_data = CourseDataField(read_only=True)
    
    class Meta:
        model = PlanYear
        fields = (
            'id', 'plan', 'year', 'summer', 'autumn', 'winter', 'spring',
            'summer_sections', 'autumn_sections', 'winter_sections',
            'spring_sections', 'course_data'
        )
        read_only_fields = ('id', 'course_data')
        
        
class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentRelatedField(read_only=True)
    upvotes = VotesField(read_only=True)
    downvotes = VotesField(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            'id', 'course', 'rating', 'grade', 'text',
            'upvotes', 'downvotes', 'created_at', 'updated_at', 'comments',
            'author', 'instructor', 'instructor_name'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'upvotes', 'downvotes', 'comments',
            'author', 'instructor_name'
        )
        
        
class CommentSerializer(serializers.ModelSerializer):
    comments = CommentRelatedField(read_only=True)
    content_object = ContentObjectRelatedField()
    upvotes = VotesField(read_only=True)
    downvotes = VotesField(read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'content_object', 'text', 'upvotes', 'downvotes',
            'created_at', 'updated_at', 'comments'
        )
        read_only_fields = (
            'created_at', 'updated_at', 'upvotes', 'downvotes', 'comments',
            'author'
        )