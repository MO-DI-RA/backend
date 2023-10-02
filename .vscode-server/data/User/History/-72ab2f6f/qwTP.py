from rest_framework import serializers
from .models import Movie, Actor, Review

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'review_set', 'opening_date', 'running_time', 'overview']
        read_only_fields = ['reviews']
        
class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'gender', 'birth_date']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'movie', 'username', 'star', 'comment', 'created']
        extra_kwargs = {
            'movie': {'read_only': True},
        }