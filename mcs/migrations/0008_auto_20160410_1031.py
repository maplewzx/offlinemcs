# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-10 10:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcs', '0007_files_groupid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='GroupID',
            new_name='GroupId',
        ),
    ]
