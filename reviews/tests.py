from django.test import TestCase
from django.utils.text import slugify
from unidecode import unidecode

from .models import Company


class CompanyModelTest(TestCase):
    def test_slug_generation(self):
        company = Company.objects.create(name="Test Company -sp-z-oo")
        self.assertEqual(company.slug, slugify("Test Company"))

    def test_absolute_url(self):
        company = Company.objects.create(name="Example Co")
        self.assertEqual(company.get_absolute_url(), f"/{company.pk}/{company.slug}")


class AnotherCompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company S.A.",
            headquarters_city="Warsaw",
            website="http://testcompany.com",
        )

    def test_slug_creation(self):
        expected_slug = slugify(unidecode("Test Company S.A.")).replace("-sa", "")
        self.assertEqual(self.company.slug, expected_slug)

    def test_get_absolute_url(self):
        url = self.company.get_absolute_url()
        self.assertIn(str(self.company.pk), url)
        self.assertIn(self.company.slug, url)
