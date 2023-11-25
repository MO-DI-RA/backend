<<<<<<< HEAD
# Generated by Django 4.0 on 2023-11-14 01:56
=======
# Generated by Django 4.0 on 2023-11-23 14:03
>>>>>>> develop

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=300, verbose_name="comment")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GatheringPost",
            fields=[
<<<<<<< HEAD
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('content', models.TextField(max_length=2000, verbose_name='content')),
                ('status', models.BooleanField(default=False, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
=======
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag", models.CharField(max_length=10)),
                ("method", models.CharField(max_length=10)),
                ("max_people", models.IntegerField()),
                ("period", models.CharField(max_length=20)),
                ("title", models.CharField(max_length=64, verbose_name="title")),
                ("content", models.TextField(max_length=2000, verbose_name="content")),
                ("summary", models.CharField(max_length=50, verbose_name="summary")),
                ("status", models.BooleanField(default=False, verbose_name="status")),
                ("deadline", models.DateTimeField(null=True, verbose_name="deadline")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
>>>>>>> develop
            ],
        ),
    ]