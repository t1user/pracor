# Generated by Django 5.1.3 on 2024-11-16 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("reviews", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="benefit",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="benefit",
            name="reviewer",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Zatwierdzający",
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="reviewer",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Zatwierdzający",
            ),
        ),
        migrations.AddField(
            model_name="interview",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="reviews.company"
            ),
        ),
        migrations.AddField(
            model_name="interview",
            name="reviewer",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Zatwierdzający",
            ),
        ),
        migrations.AddField(
            model_name="interview",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="position",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="reviews.company",
            ),
        ),
        migrations.AddField(
            model_name="position",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="company",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="reviews.company",
                verbose_name="firma",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="position",
            field=models.OneToOneField(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="reviews.position",
                verbose_name="stanowisko",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="reviewer",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Zatwierdzający",
            ),
        ),
        migrations.AddField(
            model_name="salary",
            name="benefits",
            field=models.ManyToManyField(
                blank=True, to="reviews.benefit", verbose_name="benefity"
            ),
        ),
        migrations.AddField(
            model_name="salary",
            name="company",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="reviews.company",
                verbose_name="firma",
            ),
        ),
        migrations.AddField(
            model_name="salary",
            name="position",
            field=models.OneToOneField(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="reviews.position",
                verbose_name="stanowisko",
            ),
        ),
        migrations.AddField(
            model_name="salary",
            name="reviewer",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Zatwierdzający",
            ),
        ),
        migrations.AddIndex(
            model_name="position",
            index=models.Index(
                fields=["position", "company"], name="reviews_pos_positio_35f801_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="position",
            index=models.Index(
                fields=["user", "company"], name="reviews_pos_user_id_20cf89_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="salary",
            index=models.Index(
                fields=["company", "position"], name="reviews_sal_company_c3c707_idx"
            ),
        ),
    ]
