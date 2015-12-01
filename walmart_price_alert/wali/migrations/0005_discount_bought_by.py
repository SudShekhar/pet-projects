# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wali', '0004_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='bought_by',
            field=models.IntegerField(default=0, verbose_name=b'Already brought by'),
            preserve_default=True,
        ),
    ]
