from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('condition', models.CharField(choices=[('NEW', 'Brand New / Sealed'), ('REFURB', 'Refurbished / Tested'), ('USED', 'Used / Working'), ('SCRAP', 'Scrap / For Spare Parts')], default='USED', max_length=10)),
                ('stock_count', models.PositiveIntegerField(default=1)),
                ('item_location', models.CharField(choices=[('GULU', 'Gulu City'), ('LIRA', 'Lira City'), ('KLA', 'Kampala Road / Hub'), ('ARUA', 'Arua City')], default='GULU', max_length=10)),
                ('seller_location_details', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=255, verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='myapp.product')),
            ],
        ),
    ]
