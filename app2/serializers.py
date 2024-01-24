from more_itertools import ilen
from rest_framework.serializers import ModelSerializer

from .models import *


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["video", "img_1", "img_2", "img_3", "img_4", "img_5", "img_6", "img_7", "img_8", "img_9", "img_10",
                  "title", "description"]


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["comment", "post"]
