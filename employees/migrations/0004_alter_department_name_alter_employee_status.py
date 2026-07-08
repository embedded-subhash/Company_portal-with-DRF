from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_department_employee_profile_image_and_more'),
    ]

    operations = [
        migrations.RunPython(
            migrations.RunPython.noop,
            migrations.RunPython.noop,
        ),
    ]
