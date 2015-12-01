# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wali', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='number_of_wishlists',
            field=models.IntegerField(default=0),
        ),
    ]
