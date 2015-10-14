# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_auto_20151007_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_photo',
            name='owner',
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'users_photos'),
        ),
        migrations.DeleteModel(
            name='User_Photo',
        ),
    ]
