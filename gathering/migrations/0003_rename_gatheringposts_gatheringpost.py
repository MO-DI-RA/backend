# Generated by Django 4.0 on 2023-10-08 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('gathering', '0002_comment_gatheringposts_delete_user_comment_post_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GatheringPosts',
            new_name='GatheringPost',
        ),
    ]
