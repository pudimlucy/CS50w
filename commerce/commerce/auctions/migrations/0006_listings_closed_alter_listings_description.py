# Generated by Django 4.1.2 on 2022-10-31 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_alter_comments_comment_alter_listings_category_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="closed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="listings",
            name="description",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
