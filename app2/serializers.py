from more_itertools import ilen
from rest_framework.serializers import ModelSerializer

from .models import *
from .tasks import *


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["video", "img_1", "img_2", "img_3", "img_4", "img_5", "img_6", "img_7", "img_8", "img_9", "img_10",
                  "title", "description"]

    def create(self, validated_data):
        return create_post.apply_async(kwargs=validated_data).get()


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment", "post"]

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return create_comment.apply_async(kwargs=validated_data).get()


