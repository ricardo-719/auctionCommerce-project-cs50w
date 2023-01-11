# Generated by Django 4.1.4 on 2023-01-11 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bids',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='category',
            field=models.CharField(choices=[('OTH', 'Other'), ('HOM', 'Home'), ('FAS', 'Fashion'), ('TOY', 'Toys'), ('ELE', 'Electronics'), ('BAB', 'Baby'), ('AUT', 'Automotive')], default='OTH', max_length=15),
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='itemDescription',
            field=models.CharField(default='Item Description', max_length=450),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='itemTitle',
            field=models.CharField(default='Item Title', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auctionlistings',
            name='listingImg',
            field=models.ImageField(default='Listing Img URL', max_length=250, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='initialBid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
