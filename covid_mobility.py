import pandas as pd
import matplotlib.pyplot as plt

# Load Google Mobility data from URL
mobility_url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"
mobility = pd.read_csv(mobility_url)

# Load covid confirmed cases data from URL
covid_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
confirmed = pd.read_csv(covid_url)

# Filter and process covid data for India
india_confirmed = confirmed[confirmed['Country/Region'] == 'India'].drop(['Province/State', 'Lat', 'Long'], axis=1)
india_confirmed = india_confirmed.groupby('Country/Region').sum().T
india_confirmed.index = pd.to_datetime(india_confirmed.index)
india_confirmed.columns = ['Confirmed']
india_confirmed['new_cases'] = india_confirmed['Confirmed'].diff().fillna(0)
india_confirmed['new_cases_smoothed'] = india_confirmed['new_cases'].rolling(window=7).mean()

# Process Google Mobility data for India
india_mobility = mobility[(mobility['country_region'] == 'India') & (mobility['sub_region_1'].isna())].copy()
india_mobility['date'] = pd.to_datetime(india_mobility['date'])
india_mobility['workplace_mobility'] = india_mobility['workplaces_percent_change_from_baseline']
india_mobility = india_mobility[['date', 'workplace_mobility']]

# Merge both datasets on date
combined = pd.merge(india_mobility, india_confirmed, left_on='date', right_index=True, how='inner')

# Plotting
fig, ax1 = plt.subplots(figsize=(14, 7))

# Mobility plot (left Y-axis)
ax1.set_xlabel('Date')
ax1.set_ylabel('Workplace Mobility (% from baseline)', color='tab:green')
ax1.plot(combined['date'], combined['workplace_mobility'].rolling(7).mean(), color='tab:green', label='Mobility')
ax1.tick_params(axis='y', labelcolor='tab:green')

# COVID cases plot (right Y-axis)
ax2 = ax1.twinx()
ax2.set_ylabel('New COVID Cases (7-day avg)', color='tab:red')
ax2.plot(combined['date'], combined['new_cases_smoothed'], color='tab:red', label='New Cases')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Final touches
plt.title('India: Workplace Mobility vs COVID-19 Cases (Live Data)')
fig.tight_layout()
plt.grid(True)
plt.show()
