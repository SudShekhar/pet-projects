# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wali', '0003_auto_20150606_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('end_date', models.DateTimeField()),
                ('discounted_cost', models.FloatField(verbose_name=b'Discounted Cost')),
                ('min_customers', models.IntegerField(verbose_name=b'Minimum Number of customers')),
                ('product_id', models.OneToOneField(to='wali.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
