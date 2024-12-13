"""
Remove from database all entries that have invalid www (www not working).
"""

# Configuration to allow for access to project models
import os
import sys

import requests

proj_path = "/home/tomek/pracor/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pracor.settings")
sys.path.append(proj_path)
from reviews.models import Company

COUNTER = 0
TIMEOUTS = []


def test_www(company):
    www = company.website
    try:
        r = requests.get(www, timeout=30)
        print(r.status_code)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error http: ", e.args)
        return False
    except requests.exceptions.ConnectionError as e:
        print("Wrong www: ", e.args)
        return False
    except requests.exceptions.TooManyRedirects as e:
        print("Too many redirects: ", e.args, "still adding ", www, "to database")
        return True
    except requests.exceptions.ReadTimeout as e:
        print("Timeout ", e.args, company.website)
        TIMEOUTS.append(company)
        return True
    return True


if __name__ == "__main__":
    companies = Company.objects.all()
    for company in companies:
        # print('*', end='')
        print("Testing {} {}".format(company.name, company.website))
        if not test_www(company):
            print("Deleting {} {}".format(company.name, company.website))
            company.delete()
            COUNTER += 1

    print("Companies deleted: ", COUNTER)
    print("Timeouts:")
    for i in TIMEOUTS:
        print(i.name, i.website)
