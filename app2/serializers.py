from rest_framework import serializers
from rest_framework.serializers import *

from .models import *
from .tasks import *


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["pk", "video", "img_1", "img_2", "img_3", "img_4", "img_5", "img_6", "img_7", "img_8", "img_9",
                  "img_10",
                  "title", "description"]
        extra_kwargs = {"pk": {"read_only": True}}


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk" ,"comment", "post", "date", "user"]
        extra_kwargs = {"post": {"read_only": True}, "user": {"read_only": True}, "date": {"read_only": True}}

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        validated_data['post_id'] = self.context['request'].parser_context['kwargs']['pk']
        return create_comment.apply_async(kwargs=validated_data).get()


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["post", "user"]
        extra_kwargs = {'user': {'read_only': True}, 'post': {'read_only': True}}

    def create(self, validated_data):
        return post_like.apply_async(kwargs=validated_data).get()
