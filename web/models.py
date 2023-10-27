from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User , related_name='blog_posts' , on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User , related_name='post_likes',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_comment')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='question_comment')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.question.title , self.user.username)
    

class Replies(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_reply')
    comment = models.ForeignKey(Comment , on_delete=models.CASCADE,related_name='comment_reply')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='question_reply')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.question.title,self.user.username)