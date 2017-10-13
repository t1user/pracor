"""Creates database entries for reviews.Company from excel files. Excel files must have labels in row 8 and 1000 entries starting from row 9. Columns with names as per line [] must exist.
"""

#Configuration to allow for access to project models
import os, sys
proj_path = "/home/tomek/pracr/"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pracr.settings')
sys.path.append(proj_path)
import pracr.wsgi



import openpyxl, requests
#from openpyxl.worksheet.worksheet.Worksheet import iter_rows, iter_cells, cell
from reviews.models import Company


def get_files():
    #create a list of excel files
    files = []
    for file in os.listdir():
        if file.endswith('.xlsx'):
            files.append(file)
    return files

def get_sheet(file):
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    return sheet

def count_rows():
    for file in files:
        sheet = get_sheet(file)
        n = 0
        for row in sheet.rows:
            n+=1
        print(n)




def get_header(sheet):
    #get content of row 8 and return it as a list
    header = [cell.value for column in sheet.iter_cols(min_row=8, max_row=8) for cell in column]
    return header
            
        
def get_content(header, sheet):
    content = []
    for row in sheet.iter_rows(min_col=1, max_col=len(header), min_row=9, max_row=1008):
        values = {}
        for index, cell in enumerate(row):
            values[header[index]]= cell.value
        content.append(values)
    return content


def create_entry(entry):
    """Creates one database entry from a dictionary passed to it."""
    def get_public(item):
        """Helper function to convert public/private staus into boolean
        value defined in the database"""
        if item == 'Niegiełdowe':
            return False
        else:
            return True

    def get_employment(employees):
        """Helper function to convert employment classes into ranges
        defined in database."""
        if employees < 100:
            return 'A'
        elif employees < 500:
            return 'B'
        elif employees < 1000:
            return 'C'
        elif employees < 5000:
            return 'D'
        elif employees < 10000:
            return 'E'
        else:
            return 'F'


    def clean_name(name):
        new_name = name.strip('[1]').strip()
        if 'Likwidacja' in new_name or 'Zamknięta' in new_name:
            raise ValueError
        return new_name

    #want to have companies without www removed silently (without loggin an error)
    if entry['Strona www'] != 'n/a':
        try:
            item = Company(name = clean_name(entry['Firma']),
                           headquarters_city = entry['Miasto'],
                           region = entry['Kraj/Region'],
                           country = entry['Kraj'],
                           website = entry['Strona www'],
                           public = get_public(entry['Notowane/Nienotowane']),
                           ownership = entry['Właściciele'],
                           employment = get_employment(entry['Liczba zatrudnionych']),
        )
            item.save()
            return 1
        except Exception as e:
            print('ERROR!!!!!!!!   ', entry['Firma'], entry['Strona www'], 'Error: ', e)
            return 0

    return 0

def test_www(entry):
    number = entry['Num']
    name = entry['Firma']
    www = entry['Strona www']
    
    r = requests.get(www)
    if r.status_code != requests.codes.ok:
        print('ERROR!!!!!!! ', number, name, www, r.status_code)

def list_no_www(entry):
    if entry['Strona www'] == 'n/a':
        print(entry['Firma'], entry['Strona www'])
        return 1
    return 0
    
        
        

#returns a list of excel files
files = get_files()
#gets the active sheet from given file
sheet = get_sheet(files[1])
#creates dictionary keys from column labels in row 8, returns a list
header = get_header(sheet)
#returns a list of dictionaries with content from the given sheet
content = get_content(header, sheet)

"""
counter = 0
for entry in content:
    print(entry['Firma'], entry['Strona www'])
    try:
        test_www(entry)
    except:
        counter+=1
print(counter)
"""
    

def do_file(content, function):
    """Performs 'function' for content generated from one file"""
    counter = 0
    for entry in content:
        a = function(entry)
        counter+=a
    return counter

def run_files(function):
    """Performs 'function' for all files."""
    counter = 0
    for file in files:
        print(file)
        sheet = get_sheet(file)
        header = get_header(sheet)
        content = get_content(header, sheet)
        a = do_file(content, function)
        counter += a
    print('Count: ', counter)

run_files(create_entry)
#run_files(list_no_www)
        



"""
#print(content)

for  item in content:
    print(item['Num'], item['Firma'], item['Strona www'])
    


print(files)
print(files[1])
"""
