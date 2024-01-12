import os
import dotenv
dotenv.load_dotenv()

import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
# Replace 'your_dataset.csv' with the actual filename or path to your dataset
df = pd.read_csv(os.getenv("SOURCE_URL"))

# Ensure 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Sort the DataFrame by date
df = df.sort_values(by=['state', 'date'])

# Calculate daily cases for each state 
df['daily_cases'] = df.groupby('state')['cases'].diff().fillna(df['cases'])

# Aggregate the data to handle duplicates (summing daily cases for the same date and state )
df_agg = df.groupby(['date', 'state'], as_index=False)['daily_cases'].sum().reset_index()

# Pivot the DataFrame to have 'date' as the index and columns for each state 
pivot_df = df_agg.pivot(index='date', columns='state', values='daily_cases')

# Add a new column for the total daily cases across all states
pivot_df['Total'] = pivot_df.sum(axis=1)

# Plot the line chart
ax = pivot_df.plot(kind='line', y=pivot_df.columns, legend='brief', figsize=(12, 8))
# ax = pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8))

# Set x-axis ticks every N days (adjust N as needed)
N = 7
ax.xaxis.set_major_locator(plt.MaxNLocator(N))

plt.title('Daily COVID-19 Cases Over Time by County and Total Daily Cases Across All States')
plt.xlabel('Date')
plt.ylabel('Number of Daily Cases')
plt.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
