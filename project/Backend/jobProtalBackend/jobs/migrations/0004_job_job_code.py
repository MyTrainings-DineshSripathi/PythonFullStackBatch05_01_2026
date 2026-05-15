from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
