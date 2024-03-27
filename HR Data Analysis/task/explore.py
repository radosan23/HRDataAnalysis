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


def stage_1(df):
    print(df.sort_values('average_monthly_hours', ascending=False)['Department'][:10].tolist())
    print(df.query("Department == 'IT' & salary == 'low'")['number_project'].sum())
    print(df.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist())


def stage_2(df):
    result = df.groupby(['left']).agg({'number_project': ['median', lambda x: (x > 5).sum()],
                                       'time_spend_company': ['mean', 'median'],
                                       'Work_accident': ['mean'],
                                       'last_evaluation': ['mean', 'std']}).round(2)
    print(result.rename(columns={'<lambda_0>': 'count_bigger_5'}).to_dict())


def main():
    get_data()
    a_office = pd.read_xml('../Data/A_office_data.xml')
    b_office = pd.read_xml('../Data/B_office_data.xml')
    hr_data = pd.read_xml('../Data/hr_data.xml')

    a_office.index = 'A' + a_office['employee_office_id'].astype(str).values
    b_office.index = 'B' + b_office['employee_office_id'].astype(str).values
    hr_data = hr_data.set_index('employee_id')

    df = pd.concat([a_office, b_office])
    df = df.merge(hr_data, how='inner', left_index=True, right_index=True, sort=True)
    df.drop('employee_office_id', axis=1, inplace=True)

    stage_2(df)


if __name__ == '__main__':
    main()
