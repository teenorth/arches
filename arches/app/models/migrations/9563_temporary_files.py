# Generated by Django 3.2.15 on 2023-05-25 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "9055_add_branch_publication_to_node"),
    ]

    operations = [
        migrations.CreateModel(
            name="TempFile",
            fields=[
                ("fileid", models.UUIDField(primary_key=True, serialize=False)),
                ("path", models.FileField(upload_to="archestemp")),
            ],
            options={
                "db_table": "files_temporary",
                "managed": True,
            },
        ),
    ]
