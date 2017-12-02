import os, sys
proj_path = "/home/tomek/pracr/"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pracr.settings')
sys.path.append(proj_path)
import pracr.wsgi

import re


from reviews.models import Company


def clean_name(name):
    endings = ['S.A.',
               'Sp. z o.o.',
               'Sp. z o.o. Sp.k.',
               'Sp. j.',
               'Sp. j. Sp. j.',
               'Sp. k.',
               'Sp. j. Sp. j.',
               'Sp. z o.o. Ska.',
               'Sp. z o.o. Sp. j.',
    ]
    for e in endings:
        if name.endswith(e):
            name = name.replace(e, '')
    return name


companies = Company.objects.all()
pattern = re.compile('\((\d+)\.?\d{0,2}%\)')

counter = 0
for_deletion = []
for company in companies:
    if company.ownership == 'n/a':
        continue
    owners = company.ownership.split(',')
    if len(owners) == 1:
        owner = owners[0].split('(')[0].strip()
        try:
            percentage = pattern.findall(owners[0])[0]
            percentage = float(percentage)
        except IndexError:
            percentage = 100
        if percentage < 60:
            continue
        parent = companies.filter(name=owner)
        if parent.count() > 0:
            name = clean_name(parent[0].name).strip()
            name_s = name.split(' ')
            for i in name_s:
                if i.upper() in company.name.upper():
                    print('Company: ', company, '-->', 'Parent: ', parent)
                    #companies not deleted immediately so that their children can found
                    for_deletion.append(company.pk)
                    counter+= 1
                    break
print(counter)

# this is actual deletion
for item in for_deletion:
    companies.get(pk=item).delete()

a=companies.get(name="Mbank S.A.")
a.name="mBank S.A."
a.save()

            
