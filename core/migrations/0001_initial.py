# Generated by Django 3.2.8 on 2024-03-17 17:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True)),
                ('definition', models.TextField()),
                ('count', models.IntegerField(default=0)),
                ('pos', models.CharField(blank=True, max_length=50, null=True)),
                ('is_popular_now', models.BooleanField(default=False)),
                ('popularity_updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
