from rest_framework import serializers
from blogging.models import Blog
from django.contrib.auth.models import User
import datetime


class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=True, max_length=100)
    createdAt = serializers.CharField(required=False)
    content = serializers.CharField(required=True, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance



class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Blog.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'blog']