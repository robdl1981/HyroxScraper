import requests
from bs4 import BeautifulSoup
import pandas as pd

# event_main_group possible values:
# 2024 Anaheim
# 2024 Marseille
# 2024 Stockholm
# 2024 Frankfurt
# 2024 Melbourne
# 2024 London
# 2024 Hong Kong
# 2024 Dallas
# 2024 Beijing
# 2024 Chicago Navy Pier
# 2024 Dublin
# 2024 Manchester
# 2024 Ciudad de Mexico
# 2024 Paris
# 2024 Poznan
# 2024 Hamburg
# 2024 Birmingham
# 2024 Madrid
# 2024 Incheon
# 2024 Milan
# 2024 Amsterdam
# 2024 Nice
# 2024 Toronto
# 2024 Stuttgart
# 2024 Perth
# 2024 Cape Town
# 2024 Singapore
# 2024 Brisbane
# 2024 Sydney
# 2024 Singapore National Stadium

# event possible values:
# HPRO_JGDMS4JI93E      ------------------------    HYROX PRO
# H_JGDMS4JI93E         ------------------------    HYROX
# HDP_JGDMS4JI93E       ------------------------    HYROX PRO DOUBLES
# HD_JGDMS4JI93E        ------------------------    HYROX DOUBLES
# HMR_JGDMS4JI93E       ------------------------    HYROX TEAM RELAY
# HA_JGDMS4JI93E        ------------------------    HYROX ADAPTIVE

# search[sex] values:
# M                     ------------------------    Men
# W                     ------------------------    Women

# num_results values:
# 25
# 50
# 100

# Post request to Hyrox url with filter data. See above for possible values
response = requests.post('https://results.hyrox.com/season-7/?pid=list&pidp=ranking_nav', data={
    'page': 1,                              
    'event_main_group': '2024 Anaheim',     
    'event': 'HPRO_JGDMS4JI93E',            
    'search[sex]': 'M',
    'num_results': 100                      
})

# Use Beautiful soup to parse the HTML from the response of post request
bs = BeautifulSoup(response.text, 'html.parser')

# Select all rows of the results table from parsed HTML using CSS selectors
results = bs.select('ul.list-group-multicolumn li.list-group-item')

print(f"{len(results)} results")

# Create empty list to store structured data from each row
df_list = []

# Loop through each row in results and select specific values from parsed HTML using CSS selectors
for row in results[1:]:
    rank = row.select_one('.place-primary').text.strip()
    rank_ag = row.select_one('.place-secondary').text.strip()
    name = row.select_one('.type-fullname').text.strip()
    try:
        nat = row.select_one('.type-nation_flag img').get('title').strip()
    except:
        nat = ''
    bib = row.select_one('.type-field').text.replace('Bib Number', '').strip()
    age = row.select_one('.type-age_class').text.replace('Age Group', '').strip()
    workout = row.select_one('.type-eval').text.replace('Workout', '').strip()
    total = row.select_one('.type-time').text.replace('Total', '').strip()

    # print(rank, rank_ag, name, nat, bib, age, workout, total)
    
    # Add row data to list
    df_list.append({
        'rank': rank,
        'rank_ag': rank_ag,
        'name': name,
        'nat': nat,
        'bib': bib,
        'age': age,
        'workout': workout,
        'total': total,
    })

# Create data frame from list using Pandas
df = pd.DataFrame(df_list)

# Output dataframe to csv file
df.to_csv('hyrox 1.csv', index=False)

