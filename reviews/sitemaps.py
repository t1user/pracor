from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Company


class CompanySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Company.objects.selected().order_by("id")


"""
class ReviewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Review.objects.selected()

class SalarySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Salary.objects.selected()

class InterviewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Salary.objects.selected()
"""


class StaticViewsSitemap(Sitemap):
    priority = 1
    changefreq = "weekly"

    def items(self):
        return [
            "home",
        ]

    def location(self, item):
        return reverse(item)
