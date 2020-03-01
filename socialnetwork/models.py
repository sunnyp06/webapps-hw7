from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    profile_user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio_input_text = models.CharField(blank=True, max_length=200)
    profile_picture = models.FileField(blank=True)
    image_type = models.CharField(max_length=50)
    following = models.ManyToManyField("self", symmetrical=False)

class Post(models.Model):
    post_input_text = models.CharField(max_length=200)
    post_date_time = models.DateTimeField()
    post_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.post_input_text + '"'

class Comment(models.Model):
    comment_input_text = models.CharField(max_length=200)
    comment_date_time = models.DateTimeField()
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)