# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wali', '0007_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='comparing_users',
            field=models.ManyToManyField(related_name=b'compare', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='users',
            field=models.ManyToManyField(related_name=b'users', to=settings.AUTH_USER_MODEL),
        ),
    ]
