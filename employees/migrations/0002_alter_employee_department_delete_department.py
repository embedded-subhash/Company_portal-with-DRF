import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.department'),
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql='DROP TABLE IF EXISTS "employees_department" CASCADE;',
                    reverse_sql='SELECT 1;',
                ),
            ],
            state_operations=[
                migrations.DeleteModel(
                    name='Department',
                ),
            ],
        ),
    ]
