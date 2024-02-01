from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    video = models.FileField(upload_to='video/post/', blank=True, null=True)
    img_1 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_2 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_3 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_4 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_5 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_6 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_7 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_8 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_9 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    img_10 = models.ImageField(upload_to='image/post/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
