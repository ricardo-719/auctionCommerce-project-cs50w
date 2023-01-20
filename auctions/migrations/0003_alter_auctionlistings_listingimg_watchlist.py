# Generated by Django 4.1.4 on 2023-01-19 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_delete_bids_delete_comments_auctionlistings_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='listingImg',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemTitle', models.CharField(max_length=80)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]