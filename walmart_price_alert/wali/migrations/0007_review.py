# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wali', '0006_discount_waiting_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('reviewer', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('up_votes', models.IntegerField()),
                ('down_votes', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('review_time', models.DateTimeField()),
                ('product_id', models.ForeignKey(to='wali.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
