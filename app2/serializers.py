from rest_framework import serializers
from rest_framework.serializers import *

from .models import *
from .tasks import *


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["pk", "video", "img_1", "img_2", "img_3", "img_4", "img_5", "img_6", "img_7", "img_8", "img_9", "img_10",
                  "title", "description"]
        extera_kwargs = {"pk": {"read_only": True}}


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment", "post"]

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return create_comment.apply_async(kwargs=validated_data).get()


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = ["post", "user"]
        extra_kwargs = {'user': {'read_only': True}, 'post': {'read_only': True}}

    def create(self, validated_data):
        return post_like.apply_async(kwargs=validated_data).get()
