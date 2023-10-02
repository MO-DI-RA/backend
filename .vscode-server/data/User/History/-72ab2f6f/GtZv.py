from rest_framework import serializers
from .models import Movie, Actor, Review

class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'name', 'reviews', 'opening_date', 'running_time', 'overview']
        
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'reviews', 'opening_date', 'running_time', 'overview']
        read_only_fields = ['reviews']

class ReviewSerializer(serializers.ModelSerializer):
    # ReviewSerializer 선언 전에 MovieSerializer가 선언되어야함.
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'movie', 'username', 'star', 'comment', 'created']