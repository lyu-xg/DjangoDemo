# CustomUser Admin
# Apples and Oranges
# Created by Patrick Zhang on 5/9/16
# Copyright © 2016 Patrick Zhang. All rights reserved.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.auth.models
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(verbose_name='username',  max_length=30, unique=True, error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254, unique=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('role', models.CharField(null=True, blank=True, max_length=10)),
                ('is_email_verified', models.BooleanField(verbose_name='email verified', help_text='Designates whether this user has verified email', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('address1', models.CharField(blank=True, null=True, max_length=255)),
                ('address2', models.CharField(blank=True, null=True, max_length=255)),
                ('city', models.CharField(blank=True, null=True, max_length=255)),
                ('state', models.CharField(blank=True, null=True, max_length=5)),
                ('country', models.CharField(blank=True, null=True, max_length=50)),
                ('zip_code', models.CharField(blank=True, null=True, max_length=20)),
                ('groups', models.ManyToManyField(blank=True, verbose_name='AppUsergroups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', related_query_name='user')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', related_query_name='user'),
        ),
    ]
