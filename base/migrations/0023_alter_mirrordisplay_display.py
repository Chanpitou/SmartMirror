# Generated by Django 5.0 on 2024-02-21 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_alter_mirrordisplay_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mirrordisplay',
            name='display',
            field=models.CharField(choices=[('default', 'Default'), ('display2', 'Display 2'), ('display3', 'Display 3'), ('display4', 'Display 4'), ('display5', 'Display 5'), ('display6', 'Display 6')], default='display1', max_length=50),
        ),
    ]
