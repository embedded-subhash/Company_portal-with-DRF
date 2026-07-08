from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_alter_employee_department_alter_employee_employee_id_and_more'),
    ]

    operations = [
        migrations.RunPython(
            migrations.RunPython.noop,
            migrations.RunPython.noop,
        ),
    ]
