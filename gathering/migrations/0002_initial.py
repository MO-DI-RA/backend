# Generated by Django 4.0 on 2023-11-23 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("gathering", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gatheringpost",
            name="author_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.user"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="author_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.user"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="post_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="gathering.gatheringpost",
                verbose_name="gatherings",
            ),
        ),
    ]
