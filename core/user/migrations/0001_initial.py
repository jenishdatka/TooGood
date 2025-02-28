# Generated by Django 5.1.6 on 2025-02-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=123, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=123, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='media/user_avatar', verbose_name='Аватарка')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'Обычный пользователь'), (2, 'Модератор'), (3, 'Бухгалтер')], default=1, verbose_name='Роль')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
