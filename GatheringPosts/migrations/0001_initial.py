# Generated by Django 4.2.6 on 2023-10-07 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(blank=True, max_length=300)),
                ('user_id', models.IntegerField(unique=True)),
                ('status', models.CharField(max_length=30)),
                ('post_created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('comment_created_at', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GatheringPosts.post')),
            ],
        ),
    ]