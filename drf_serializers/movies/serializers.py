from rest_framework import serializers
from .models import Movie, Resource, Comment, ModelA, ModelB, ModelC
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Rating must be between 1 and 10.')
        return value

    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('US gross cannot be greater than worldwide gross.')
        return data


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.liked_by.count()
        return representation

    def to_internal_value(self, data):
        resource_data = data.get('resource', data)
        return super().to_internal_value(resource_data)


class UserSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source='is_active')
    full_name = serializers.CharField(source='get_full_name')
    bio = serializers.CharField(source='userprofile.bio')
    birth_date = serializers.DateField(source='userprofile.birth_date')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'active', 'full_name', 'bio', 'birth_date']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'

class ModelASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelA
        fields = '__all__'
        depth = 1  # Adjust this for different levels of nested serialization