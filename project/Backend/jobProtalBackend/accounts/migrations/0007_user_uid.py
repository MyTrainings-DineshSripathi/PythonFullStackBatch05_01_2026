from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_bio_user_experience_user_job_preferences_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
