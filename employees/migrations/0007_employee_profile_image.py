from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_employee_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='employees/'),
        ),
    ]
