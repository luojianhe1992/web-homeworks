from django.db import models
from django.utils import timezone
# import the User from Django authentication system
from django.contrib.auth.models import User

# Create your models here.



# Message object is to store the messages posted by users
class Message(models.Model):

    # design foreignKey
    user = models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    date_time = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.text

class Profile(models.Model):

    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.IntegerField(default=0, blank=True)
    short_bio = models.TextField(max_length=2000, blank=True)
    # new field picture
    picture = models.ImageField(upload_to="users_photos", null=True, blank=True)

    def __unicode__(self):
        return "%s %s %s %s %s"%(self.user.username, self.first_name, self.last_name, self.age, self.short_bio)

    # use __unicode()__ to define __str()__function
    def __str__(self):
        return self.__unicode__()

    # define a static method for getting the profile information
    @staticmethod
    def get_profile(user):
        return Profile.objects.all().filter(user = user)


class Friendship(models.Model):

    user = models.CharField(max_length=100)
    friends = models.ManyToManyField(User)

    def __unicode__(self):

        return self.user

