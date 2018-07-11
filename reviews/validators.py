import csv
import re
import os
import requests
from urllib.parse import urlsplit

from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Company


class ProfanitiesFilter():
    """
    Custom validator to filter out swear words.
    First file has words that are matched inside other words.
    Second file has words that are matched only as full words.
    """
    # makeing those class variables ensures this code is called only once - after
    # starting server
    words = ''
    with open(os.path.join(settings.BASE_DIR, 'reviews/profanities_filter/prof_fil_broad.txt'), encoding='utf-8') as f:
        i = csv.reader(f, delimiter='\n')
        for item in i:
            words += item[0]
            words += '|'

    more_words = ''
    with open(os.path.join(settings.BASE_DIR, 'reviews/profanities_filter/prof_fil.txt'), encoding='utf-8') as f:
        i = csv.reader(f, delimiter='\n')
        for item in i:
            text_item = '\\b{}\\b|'.format(item[0])
            more_words += text_item

    words += more_words
    pattern = re.compile(words, re.IGNORECASE)

    def __call__(self, value):
        matches = self.pattern.findall(value)
        matches = [match for match in matches if match != '']
        full_words = value.split(' ')
        full_matched_words = []
        for word in full_words:
            for match in matches:
                if match in word:
                    full_matched_words.append(word.lower().rstrip(',!?:;.'))
        matches = set(full_matched_words)
        # if partial words matched, get the full words, of which they are part
        if matches:
            if len(matches) == 1:
                value = ''.join(matches)
            else:
                value = ', '.join(matches)
            raise forms.ValidationError('Niedopuszczalne wyrażenia: {}'.format(value),
                                        params={'value': value},
                                        )


class TextLengthValidator():
    """
    Verify whether user input meets the minimum length requirement. To be used on forms
    rather than models to give moderators option of removing parts of text without
    breaking the minimum length requirement.
    """

    def __init__(self, requirement=20):
        # real constraint is requirement-2 to allow inputs that miss target by 1 or 2 words
        self.req = requirement - 2

    def __call__(self, text):
        words = text.split(' ')
        length = len(words)
        if length < self.req:
            miss = self.req - length
            raise forms.ValidationError(
                'Za krótki wpis, wymagane {req} słow (brakuje {miss})'.format(
                    miss=miss, req=self.req), code='invalid')


class WWWValidator:
    """
    Used for validating new Company urls input by users.
    Check if website with given url exists. Don't allow:
    a). non-exising url (or url which doesn't work for some reason)
    b). url, which redirects to a url for which a Company already exists
    """

    def __call__(self, www):
        try:
            r = requests.get(www)
            if r.history:
                url = urlsplit(r.url)
                url_domain = 'http://{}'.format(url.netloc)
                try:
                    existing = Company.objects.get(website=url_domain)
                except:
                    existing = None
                if existing:
                    raise ValidationError(
                        'Ten www zarejestrowano dla: {}. Adresy www nie mogą się powtarzać'.format(
                            existing.name),
                        code='redirected',  params={'existing': existing, 'url': url_domain})
        except requests.exceptions.RequestException as e:
            raise ValidationError(
                'Podany adres www nie odpowiada. Popraw adres www',
                code='bounced')


class ContactValidator:
    """
    Reject form with included links.
    """

    def __call__(self, text):
        if '<a ' in text or '</a>' in text:
            raise ValidationError('Niedozwolona treść')
