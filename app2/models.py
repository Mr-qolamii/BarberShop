from django.db import models


class Post(models.Model):
    video = models.FileField(upload_to='video/', blank=True)
    img_1 = models.ImageField(upload_to='image/', blank=True)
    img_2 = models.ImageField(upload_to='image/', blank=True)
    img_3 = models.ImageField(upload_to='image/', blank=True)
    img_4 = models.ImageField(upload_to='image/', blank=True)
    img_5 = models.ImageField(upload_to='image/', blank=True)
    img_6 = models.ImageField(upload_to='image/', blank=True)
    img_7 = models.ImageField(upload_to='image/', blank=True)
    img_8 = models.ImageField(upload_to='image/', blank=True)
    img_9 = models.ImageField(upload_to='image/', blank=True)
    img_10 = models.ImageField(upload_to='image/', blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
