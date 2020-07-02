from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, User, Follow, Group



class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True
        )
    following = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        queryset=User.objects.all()
        )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        following = data['following']
        data['user'] = self.context['request'].user
        follow = Follow.objects.filter(following=following, user=data['user']).exists()

        if data['user'] == following:
            raise ValidationError('Cant subscribe to yourself')
        if follow:
            raise ValidationError('You have already signed up')
        return data


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title')
        model = Group
