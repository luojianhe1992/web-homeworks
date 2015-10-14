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