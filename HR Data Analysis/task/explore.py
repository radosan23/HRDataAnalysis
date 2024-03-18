import pandas as pd
import requests
import os


def get_data():
    if not os.path.exists('../Data'):
        os.mkdir('../Data')
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)


def main():
    get_data()
    a_office = pd.read_xml('../Data/A_office_data.xml')
    b_office = pd.read_xml('../Data/B_office_data.xml')
    hr_data = pd.read_xml('../Data/hr_data.xml')

    a_office.index = 'A' + a_office['employee_office_id'].astype(str).values
    b_office.index = 'B' + b_office['employee_office_id'].astype(str).values
    hr_data = hr_data.set_index('employee_id', drop=False)
    print(a_office.index.tolist(), b_office.index.tolist(), hr_data.index.tolist(), sep='\n')


if __name__ == '__main__':
    main()
