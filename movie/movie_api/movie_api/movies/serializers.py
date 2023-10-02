from rest_framework import serializers
from .models import Movie, Review, Actor


class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'name', 'reviews', 'actors', 'opening_date', 'running_time', 'overview']
        read_only_fields = ['reviews']

class ActorSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    
    class Meta:
        model = Actor
        fields = ['id', 'name', 'gender', 'birth_date', 'movies']


class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'movie', 'username', 'star', 'comment', 'created']