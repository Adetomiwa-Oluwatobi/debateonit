from django.core.management import call_command
from django.db import migrations

def create_superuser(apps, schema_editor):
    call_command('createsuperuser', '--noinput', username='devyneme', email='adetomiwaoluwatobi45.com', password='#Torazy45')

class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(create_superuser),
    ]
