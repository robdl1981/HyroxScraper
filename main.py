import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

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

print(f"{len(results)-1} results")

# Create empty list to store structured data from each row
df_list = []

# Loop through each row in results and select specific values from parsed HTML using CSS selectors
for row in tqdm(results[1:]):
    rank = row.select_one('.place-primary').text.strip()
    rank_ag = row.select_one('.place-secondary').text.strip()
    name = row.select_one('.type-fullname a').text.strip()
    link = row.select_one('.type-fullname a').get('href').strip()
    try:
        nat = row.select_one('.type-nation_flag img').get('title').strip()
    except:
        nat = ''
    bib = row.select_one('.type-field').text.replace('Bib Number', '').strip()
    age = row.select_one('.type-age_class').text.replace('Age Group', '').strip()
    workout = row.select_one('.type-eval').text.replace('Workout', '').strip()
    total = row.select_one('.type-time').text.replace('Total', '').strip()

    response_link = requests.get(f"https://results.hyrox.com/season-7/" + link)

    # Use Beautiful soup again to parse the HTML from the response of the link get request
    bs_link = BeautifulSoup(response_link.text, 'html.parser')

    race = bs_link.select_one('td.f-__meeting').text.strip()
    division = bs_link.select_one('td.f-__event').text.strip()

    running1_time = bs_link.select_one('tr.f-time_01 td.f-time_01').text.strip()    
    running1_place = bs_link.select_one('tr.f-time_01 td.last').text.strip()
    
    ski_erg_1000_time = bs_link.select_one('tr.f-time_11 td.f-time_11').text.strip()    
    ski_erg_1000_place = bs_link.select_one('tr.f-time_11 td.last').text.strip()
    
    running2_time = bs_link.select_one('tr.f-time_02 td.f-time_02').text.strip()    
    running2_place = bs_link.select_one('tr.f-time_02 td.last').text.strip()
    
    sled_push_50_time = bs_link.select_one('tr.f-time_12 td.f-time_12').text.strip()    
    sled_push_50_place = bs_link.select_one('tr.f-time_12 td.last').text.strip()
    
    running3_time = bs_link.select_one('tr.f-time_03 td.f-time_03').text.strip()    
    running3_place = bs_link.select_one('tr.f-time_03 td.last').text.strip()
    
    sled_pull_50_time = bs_link.select_one('tr.f-time_13 td.f-time_13').text.strip()    
    sled_pull_50_place = bs_link.select_one('tr.f-time_13 td.last').text.strip()

    running4_time = bs_link.select_one('tr.f-time_04 td.f-time_04').text.strip()    
    running4_place = bs_link.select_one('tr.f-time_04 td.last').text.strip()
    
    burpee_80_time = bs_link.select_one('tr.f-time_14 td.f-time_14').text.strip()    
    burpee_80_place = bs_link.select_one('tr.f-time_14 td.last').text.strip()

    running5_time = bs_link.select_one('tr.f-time_05 td.f-time_05').text.strip()    
    running5_place = bs_link.select_one('tr.f-time_05 td.last').text.strip()
    
    row_1000_time = bs_link.select_one('tr.f-time_15 td.f-time_15').text.strip()    
    row_1000_place = bs_link.select_one('tr.f-time_15 td.last').text.strip()

    running6_time = bs_link.select_one('tr.f-time_06 td.f-time_06').text.strip()    
    running6_place = bs_link.select_one('tr.f-time_06 td.last').text.strip()
    
    farmers_200_time = bs_link.select_one('tr.f-time_16 td.f-time_16').text.strip()    
    farmers_200_place = bs_link.select_one('tr.f-time_16 td.last').text.strip()

    running7_time = bs_link.select_one('tr.f-time_07 td.f-time_07').text.strip()    
    running7_place = bs_link.select_one('tr.f-time_07 td.last').text.strip()
    
    sandbag_100_time = bs_link.select_one('tr.f-time_17 td.f-time_17').text.strip()    
    sandbag_100_place = bs_link.select_one('tr.f-time_17 td.last').text.strip()

    running8_time = bs_link.select_one('tr.f-time_08 td.f-time_08').text.strip()    
    running8_place = bs_link.select_one('tr.f-time_08 td.last').text.strip()
    
    roxzone_time = bs_link.select_one('tr.f-time_60 td.f-time_60').text.strip()    
    roxzone_place = bs_link.select_one('tr.f-time_60 td.last').text.strip()

    run_total = bs_link.select_one('tr.f-time_49 td.f-time_49').text.strip()    
    roxzone_place = bs_link.select_one('tr.f-time_49 td.last').text.strip()

    best_lap_time = bs_link.select_one('tr.f-time_50 td.f-time_50').text.strip()    
    best_lap_place = bs_link.select_one('tr.f-time_50 td.last').text.strip()

    bonus = bs_link.select_one('tr.f-gimmick_03 td').text.strip()    
    penalty = bs_link.select_one('tr.f-gimmick_01 td').text.strip()    
    disqual = bs_link.select_one('tr.f-disqual_reason td').text.strip()    
    info = bs_link.select_one('tr.f-gimmick_09 td').text.strip()    
    
    # rank2 = bs_link.select_one('tr.f-gimmick_09 td').text.strip()
    
    rox_in_tod = bs_link.select_one('tr.f-time_84 td.time_day').text.strip()
    rox_in_time = bs_link.select_one('tr.f-time_84 td.time').text.strip()
    rox_in_diff = bs_link.select_one('tr.f-time_84 td.diff').text.strip()

    ski_erg_1000_in_tod = bs_link.select_one('tr.f-time_85 td.time_day').text.strip()
    ski_erg_1000_in_time = bs_link.select_one('tr.f-time_85 td.time').text.strip()
    ski_erg_1000_in_diff = bs_link.select_one('tr.f-time_85 td.diff').text.strip()

    ski_erg_1000_out_tod = bs_link.select_one('tr.f-time_51 td.time_day').text.strip()
    ski_erg_1000_out_time = bs_link.select_one('tr.f-time_51 td.time').text.strip()
    ski_erg_1000_out_diff = bs_link.select_one('tr.f-time_51 td.diff').text.strip()

    rox_out_tod = bs_link.select_one('tr.f-time_86 td.time_day').text.strip()
    rox_out_time = bs_link.select_one('tr.f-time_86 td.time').text.strip()
    rox_out_diff = bs_link.select_one('tr.f-time_86 td.diff').text.strip()
    
    rox_in2_tod = bs_link.select_one('tr.f-time_87 td.time_day').text.strip()
    rox_in2_time = bs_link.select_one('tr.f-time_87 td.time').text.strip()
    rox_in2_diff = bs_link.select_one('tr.f-time_87 td.diff').text.strip()

    sled_push_50_in_tod = bs_link.select_one('tr.f-time_88 td.time_day').text.strip()
    sled_push_50_in_time = bs_link.select_one('tr.f-time_88 td.time').text.strip()
    sled_push_50_in_diff = bs_link.select_one('tr.f-time_88 td.diff').text.strip()

    sled_push_50_out_tod = bs_link.select_one('tr.f-time_52 td.time_day').text.strip()
    sled_push_50_out_time = bs_link.select_one('tr.f-time_52 td.time').text.strip()
    sled_push_50_out_diff = bs_link.select_one('tr.f-time_52 td.diff').text.strip()

    rox_out2_tod = bs_link.select_one('tr.f-time_89 td.time_day').text.strip()
    rox_out2_time = bs_link.select_one('tr.f-time_89 td.time').text.strip()
    rox_out2_diff = bs_link.select_one('tr.f-time_89 td.diff').text.strip()

    rox_in3_tod = bs_link.select_one('tr.f-time_90 td.time_day').text.strip()
    rox_in3_time = bs_link.select_one('tr.f-time_90 td.time').text.strip()
    rox_in3_diff = bs_link.select_one('tr.f-time_90 td.diff').text.strip()

    sled_pull_50_in_tod = bs_link.select_one('tr.f-time_91 td.time_day').text.strip()
    sled_pull_50_in_time = bs_link.select_one('tr.f-time_91 td.time').text.strip()
    sled_pull_50_in_diff = bs_link.select_one('tr.f-time_91 td.diff').text.strip()

    sled_pull_50_out_tod = bs_link.select_one('tr.f-time_53 td.time_day').text.strip()
    sled_pull_50_out_time = bs_link.select_one('tr.f-time_53 td.time').text.strip()
    sled_pull_50_out_diff = bs_link.select_one('tr.f-time_53 td.diff').text.strip()

    rox_out3_tod = bs_link.select_one('tr.f-time_92 td.time_day').text.strip()
    rox_out3_time = bs_link.select_one('tr.f-time_92 td.time').text.strip()
    rox_out3_diff = bs_link.select_one('tr.f-time_92 td.diff').text.strip()

    rox_in4_tod = bs_link.select_one('tr.f-time_93 td.time_day').text.strip()
    rox_in4_time = bs_link.select_one('tr.f-time_93 td.time').text.strip()
    rox_in4_diff = bs_link.select_one('tr.f-time_93 td.diff').text.strip()

    burpee_80_in_tod = bs_link.select_one('tr.f-time_94 td.time_day').text.strip()
    burpee_80_in_time = bs_link.select_one('tr.f-time_94 td.time').text.strip()
    burpee_80_in_diff = bs_link.select_one('tr.f-time_94 td.diff').text.strip()

    burpee_80_out_tod = bs_link.select_one('tr.f-time_54 td.time_day').text.strip()
    burpee_80_out_time = bs_link.select_one('tr.f-time_54 td.time').text.strip()
    burpee_80_out_diff = bs_link.select_one('tr.f-time_54 td.diff').text.strip()

    rox_out4_tod = bs_link.select_one('tr.f-time_95 td.time_day').text.strip()
    rox_out4_time = bs_link.select_one('tr.f-time_95 td.time').text.strip()
    rox_out4_diff = bs_link.select_one('tr.f-time_95 td.diff').text.strip()

    rox_in5_tod = bs_link.select_one('tr.f-time_96 td.time_day').text.strip()
    rox_in5_time = bs_link.select_one('tr.f-time_96 td.time').text.strip()
    rox_in5_diff = bs_link.select_one('tr.f-time_96 td.diff').text.strip()

    row_1000_in_tod = bs_link.select_one('tr.f-time_97 td.time_day').text.strip()
    row_1000_in_time = bs_link.select_one('tr.f-time_97 td.time').text.strip()
    row_1000_in_diff = bs_link.select_one('tr.f-time_97 td.diff').text.strip()

    row_1000_out_tod = bs_link.select_one('tr.f-time_55 td.time_day').text.strip()
    row_1000_out_time = bs_link.select_one('tr.f-time_55 td.time').text.strip()
    row_1000_out_diff = bs_link.select_one('tr.f-time_55 td.diff').text.strip()

    rox_out5_tod = bs_link.select_one('tr.f-time_98 td.time_day').text.strip()
    rox_out5_time = bs_link.select_one('tr.f-time_98 td.time').text.strip()
    rox_out5_diff = bs_link.select_one('tr.f-time_98 td.diff').text.strip()

    rox_in6_tod = bs_link.select_one('tr.f-time_99 td.time_day').text.strip()
    rox_in6_time = bs_link.select_one('tr.f-time_99 td.time').text.strip()
    rox_in6_diff = bs_link.select_one('tr.f-time_99 td.diff').text.strip()

    farmers_200_in_tod = bs_link.select_one('tr.f-time_100 td.time_day').text.strip()
    farmers_200_in_time = bs_link.select_one('tr.f-time_100 td.time').text.strip()
    farmers_200_in_diff = bs_link.select_one('tr.f-time_100 td.diff').text.strip()

    farmers_200_out_tod = bs_link.select_one('tr.f-time_56 td.time_day').text.strip()
    farmers_200_out_time = bs_link.select_one('tr.f-time_56 td.time').text.strip()
    farmers_200_out_diff = bs_link.select_one('tr.f-time_56 td.diff').text.strip()

    rox_out6_tod = bs_link.select_one('tr.f-time_101 td.time_day').text.strip()
    rox_out6_time = bs_link.select_one('tr.f-time_101 td.time').text.strip()
    rox_out6_diff = bs_link.select_one('tr.f-time_101 td.diff').text.strip()

    rox_in7_tod = bs_link.select_one('tr.f-time_102 td.time_day').text.strip()
    rox_in7_time = bs_link.select_one('tr.f-time_102 td.time').text.strip()
    rox_in7_diff = bs_link.select_one('tr.f-time_102 td.diff').text.strip()

    sandbag_100_in_tod = bs_link.select_one('tr.f-time_103 td.time_day').text.strip()
    sandbag_100_in_time = bs_link.select_one('tr.f-time_103 td.time').text.strip()
    sandbag_100_in_diff = bs_link.select_one('tr.f-time_103 td.diff').text.strip()

    sandbag_100_out_tod = bs_link.select_one('tr.f-time_57 td.time_day').text.strip()
    sandbag_100_out_time = bs_link.select_one('tr.f-time_57 td.time').text.strip()
    sandbag_100_out_diff = bs_link.select_one('tr.f-time_57 td.diff').text.strip()

    rox_out7_tod = bs_link.select_one('tr.f-time_104 td.time_day').text.strip()
    rox_out7_time = bs_link.select_one('tr.f-time_104 td.time').text.strip()
    rox_out7_diff = bs_link.select_one('tr.f-time_104 td.diff').text.strip()

    wheel_balls_in_tod = bs_link.select_one('tr.f-time_105 td.time_day').text.strip()
    wheel_balls_in_time = bs_link.select_one('tr.f-time_105 td.time').text.strip()
    wheel_balls_in_diff = bs_link.select_one('tr.f-time_105 td.diff').text.strip()
    
    total_tod = bs_link.select_one('tr.f-time_finish_netto td.time_day').text.strip()
    total_time = bs_link.select_one('tr.f-time_finish_netto td.time').text.strip()
    total_diff = bs_link.select_one('tr.f-time_finish_netto td.diff').text.strip()
    
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
        'bonus': bonus,    
        'penalty': penalty,    
        'disqual': disqual,   
        'info': info,
        # 'rank2': rank,
        'rox_in_tod': rox_in_tod,
        'rox_in_time': rox_in_time,
        'rox_in_diff': rox_in_diff,
        'ski_erg_1000_in_tod': ski_erg_1000_in_tod,
        'ski_erg_1000_in_time': ski_erg_1000_in_time,
        'ski_erg_1000_in_diff': ski_erg_1000_in_diff,
        'ski_erg_1000_out_tod': ski_erg_1000_out_tod,
        'ski_erg_1000_out_time': ski_erg_1000_out_time,
        'ski_erg_1000_out_diff': ski_erg_1000_out_diff,
        'rox_out_tod': rox_out_tod,
        'rox_out_time': rox_out_time,
        'rox_out_diff': rox_out_diff,
        'rox_in2_tod': rox_in2_tod,
        'rox_in2_time': rox_in2_time,
        'rox_in2_diff': rox_in2_diff,
        'sled_push_50_in_tod': sled_push_50_in_tod,
        'sled_push_50_in_time': sled_push_50_in_time,
        'sled_push_50_in_diff': sled_push_50_in_diff,
        'sled_push_50_out_tod': sled_push_50_out_tod,
        'sled_push_50_out_time': sled_push_50_out_time,
        'sled_push_50_out_diff': sled_push_50_out_diff,
        'rox_out2_tod': rox_out2_tod,
        'rox_out2_time': rox_out2_time,
        'rox_out2_diff': rox_out2_diff,
        'rox_in3_tod': rox_in3_tod,
        'rox_in3_time': rox_in3_time,
        'rox_in3_diff': rox_in3_diff,
        'sled_pull_50_in_tod': sled_pull_50_in_tod,
        'sled_pull_50_in_time': sled_pull_50_in_time,
        'sled_pull_50_in_diff': sled_pull_50_in_diff,
        'sled_pull_50_out_tod': sled_pull_50_out_tod,
        'sled_pull_50_out_time': sled_pull_50_out_time,
        'sled_pull_50_out_diff': sled_pull_50_out_diff,
        'rox_out3_tod': rox_out3_tod,
        'rox_out3_time': rox_out3_time,
        'rox_out3_diff': rox_out3_diff,
        'rox_in4_tod': rox_out3_diff,
        'rox_in4_time': rox_in4_time,
        'rox_in4_diff': rox_in4_diff,
        'burpee_80_in_tod': burpee_80_in_tod,
        'burpee_80_in_time': burpee_80_in_time,
        'burpee_80_in_diff': burpee_80_in_diff,
        'burpee_80_out_tod': burpee_80_out_tod,
        'burpee_80_out_time': burpee_80_out_time,
        'burpee_80_out_diff': burpee_80_out_diff,
        'rox_out4_tod': rox_out4_tod,
        'rox_out4_time': rox_out4_time,
        'rox_out4_diff': rox_out4_diff,
        'rox_in5_tod': rox_in5_tod,
        'rox_in5_time': rox_in5_time,
        'rox_in5_diff': rox_in5_diff,
        'row_1000_in_tod': row_1000_in_tod,
        'row_1000_in_time': row_1000_in_time,
        'row_1000_in_diff': row_1000_in_diff,
        'row_1000_out_tod': row_1000_out_tod,
        'row_1000_out_time': row_1000_out_time,
        'row_1000_out_diff': row_1000_out_diff,
        'rox_out5_tod': rox_out5_tod,
        'rox_out5_time': rox_out5_time,
        'rox_out5_diff': rox_out5_diff,
        'rox_in6_tod': rox_in6_tod,
        'rox_in6_time': rox_in6_time,
        'rox_in6_diff': rox_in6_diff,
        'farmers_200_in_tod': farmers_200_in_tod,
        'farmers_200_in_time': farmers_200_in_time,
        'farmers_200_in_diff': farmers_200_in_diff,
        'farmers_200_out_tod': farmers_200_out_tod,
        'farmers_200_out_time': farmers_200_out_time,
        'farmers_200_out_diff': farmers_200_out_diff,
        'rox_out6_tod': rox_out6_tod,
        'rox_out6_time': rox_out6_time,
        'rox_out6_diff': rox_out6_diff,
        'rox_in7_tod': rox_in7_tod,
        'rox_in7_time': rox_in7_time,
        'rox_in7_diff': rox_in7_diff,
        'sandbag_100_in_tod': sandbag_100_in_tod,
        'sandbag_100_in_time': sandbag_100_in_time,
        'sandbag_100_in_diff': sandbag_100_in_diff,
        'sandbag_100_out_tod': sandbag_100_out_tod,
        'sandbag_100_out_time': sandbag_100_out_time,
        'sandbag_100_out_diff': sandbag_100_out_diff,
        'rox_out7_tod': rox_out7_tod,
        'rox_out7_time': rox_out7_time,
        'rox_out7_diff': rox_out7_diff,
        'wheel_balls_in_tod': wheel_balls_in_tod,
        'wheel_balls_in_time': wheel_balls_in_time,
        'wheel_balls_in_diff': wheel_balls_in_diff,
        'total_tod': total_tod,
        'total_time': total_time,
        'total_diff': total_diff
    })

# Create data frame from list using Pandas
df = pd.DataFrame(df_list)

# Output dataframe to csv file
df.to_csv('hyrox 1.csv', index=False)

