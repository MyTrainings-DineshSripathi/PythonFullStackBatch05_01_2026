from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_job_job_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='apply_source',
            field=models.CharField(choices=[('hire_flow', 'Krowdly'), ('company_site', 'Company Site')], default='hire_flow', max_length=20),
        ),
    ]
