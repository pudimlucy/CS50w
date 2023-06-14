from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "date_joined": self.date_joined,
            "following": len(self.follows()),
            "followers": len(self.followers()),
        }

    def follows(self):
        return UserFollowing.objects.filter(follower=self).all()

    def followers(self):
        return UserFollowing.objects.filter(following=self).all()

    pass


class Post(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False)

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
            "likes": len(self.likes()),
            "dislikes": len(self.dislikes()),
        }

    def likes(self):
        return Interaction.objects.filter(post=self, type=True).all()

    def dislikes(self):
        return Interaction.objects.filter(post=self, type=False).all()


class UserFollowing(models.Model):
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )


class Interaction(models.Model):
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE)
    interacted = models.ForeignKey(
        User, related_name="interacted", on_delete=models.CASCADE
    )

    # True = Like, False = Dislike
    type = models.BooleanField()
