from django.db import models
import re
from datetime import datetime, timedelta
from login.models import User
from django.utils import timezone

class PostManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['post_text']) <= 0:
            errors['post'] = "Post must have content!"
        return errors
        
class Post(models.Model):
    post_text = models.TextField()
    user = models.ForeignKey(User, related_name = "posts", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PostManager()

    def deletable(self):
        if self.created_at >= (timezone.now() - timedelta(minutes=30)):
            return True
        else:
            return False

class CommentManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['comment_text']) <= 0:
            errors['comment'] = "Comment must have content!"
        return errors
    
class Comment(models.Model):
    comment_text = models.TextField()
    post = models.ForeignKey(Post, related_name = "comments", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = "comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()