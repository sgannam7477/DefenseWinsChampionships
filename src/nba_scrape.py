import pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Gets list of NBA Champions and Runner-Ups

champions_url = 'https://www.basketball-reference.com/playoffs/'
c = requests.get(champions_url)
champions_soup = BeautifulSoup(c.content, 'html.parser')
champions_table = champions_soup.find('table', id = "champions_index")
champions_headers = []

# Ensure all appropriate table headers are acquired

for th in champions_table.find_all('th'):
    if th.get('class') is not None and 'over_header' not in th.get('class') and 'right' not in th.get('class'):
        champions_headers.append(th.text.strip())

# Acquires all data information from the table
champions_rows = []
for tr in champions_table.find_all('tr'):
    cells = []
    year = tr.find('th')
    if (year is not None and 'right' in year.get('class')):
        cells.append(year.text[0:4])
    for td in tr.find_all('td'):
        cells.append(td.text.strip())
    if cells:
        champions_rows.append(cells)

# Outputs all data into a csv file

champions_df = pd.DataFrame(champions_rows, columns=champions_headers)

output_dir = '/Users/shrenick/PycharmProjects/DefenseWinsChampionships'
file_name = 'NBA Champions.csv'
output_file = os.path.join(output_dir, file_name)
champions_df.to_csv(output_file, index=False)



for year in range(1951, 2025):
    # Acquires NBA Regular Season Advanced Data for selected year
    regular_season_url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    r = requests.get(regular_season_url)
    regular_soup = BeautifulSoup(r.content, 'html.parser')
    regular_table = regular_soup.find('table', id = "advanced-team")
    regular_headers = []

    # Get table header information for table of selected url
    for th in regular_table.find_all('th'):
        if (th.get('class') is not None and 'over_header' not in th.get('class') and 'right' not in th.get('class')):
            regular_headers.append(th.text.strip())
    regular_headers.remove('Rk')
    regular_rows = []

    # Get table data information for selected url
    for tr in regular_table.find_all('tr'):
        cells = []
        for td in tr.find_all('td'):
            cells.append(td.text.strip())
        if cells:
            regular_rows.append(cells)

    regular_df = pd.DataFrame(regular_rows, columns=regular_headers)

    # Outputs data from the url into a csv file

    output_dir = '/Users/shrenick/PycharmProjects/DefenseWinsChampionships'
    file_name = str(year - 1) + "-" + str(year) + " NBA Advanced Ratings.csv"
    output_file = os.path.join(output_dir, file_name)
    regular_df.to_csv(output_file, index=False)

    # Repeats process above but for playoff advanced stats
    playoffs_url = 'https://www.basketball-reference.com/playoffs/NBA_' + str(year) + '.html'
    p = requests.get(playoffs_url)
    playoff_soup = BeautifulSoup(p.content, 'html.parser')
    playoff_table = playoff_soup.find('table', id = "advanced-team")
    playoff_headers = []
    for th in playoff_table.find_all('th'):
        if (th.get('class') is not None and 'over_header' not in th.get('class') and 'right' not in th.get('class')):
            playoff_headers.append(th.text.strip())
    playoff_headers.remove('Rk')

    playoff_rows = []
    for tr in playoff_table.find_all('tr'):
        cells = []
        for td in tr.find_all('td'):
            cells.append(td.text.strip())
        if cells:
            playoff_rows.append(cells)

    playoff_df = pd.DataFrame(playoff_rows, columns=playoff_headers)

    output_dir = '/Users/shrenick/PycharmProjects/DefenseWinsChampionships'
    file_name = str(year - 1) + "-" + str(year) + " NBA Playoff Advanced Ratings.csv"
    output_file = os.path.join(output_dir, file_name)
    playoff_df.to_csv(output_file, index=False)



