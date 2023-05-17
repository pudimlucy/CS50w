from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "date_joined": self.date_joined,
            "nfollowing": len(self.follows()),
            "nfollowers": len(self.followers()),
        }
    def follows(self):
        return UserFollowing.objects.filter(follower=self)
    def followers(self):
        return UserFollowing.objects.filter(following=self)
    pass


class Post(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.content
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "date": self.date,
        }

class UserFollowing(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
