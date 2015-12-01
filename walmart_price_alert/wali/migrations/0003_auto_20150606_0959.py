# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wali', '0002_auto_20150605_1817'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_url',
            new_name='large_image_url',
        ),
        migrations.AddField(
            model_name='product',
            name='customer_rating_image',
            field=models.URLField(default='http://facebook.com/me.png', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='long_description',
            field=models.TextField(default='hod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='medium_image_url',
            field=models.URLField(default='http://facebook.com/me.png'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='msrp',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
