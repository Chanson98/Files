import pandas as pd
# Load sales data into a pandas dataframe
sales_data = pd.read_csv('sales.csv')

# Load SD mapping data into a pandas dataframe
sd_mapping = pd.read_csv('sd_mapping.csv')

# Merge the sales data and SD mapping data on PARENT_ACCOUNT_ID
merged_data = pd.merge(sales_data, sd_mapping, left_on='PARENT_ACCOUNT_ID', right_on='PARENT_ID', how='left')

# Replace NaN values in SD_NAME column with 'NO_CONTRACT_SD'
merged_data['SD_NAME'] =  merged_data['SD_NAME'].replace("-", "NO_CONTRACT_SD")

# Convert the DATE column to datetime
merged_data['DATE'] = pd.to_datetime(merged_data['DATE'])

# Extract quarter information from DATE column
merged_data['QUARTER'] = merged_data['DATE'].dt.quarter

# Filter only records of year 2021
merged_data = merged_data[merged_data['DATE'].dt.year == 2021]

# Group the data by SD_NAME and QUARTER and sum up the TOTAL_TRX
result = merged_data.groupby(['SD_NAME', 'QUARTER'])['TOTAL_TRX'].sum().reset_index()

# Pivot the result data to create the desired output
result_pivot = result.pivot(index='SD_NAME', columns='QUARTER', values='TOTAL_TRX').reset_index()

# Rename the quarter columns from 1, 2, 3, 4 to 2021Q1, 2021Q2, 2021Q3, 2021Q4
result_pivot.rename(columns={1: '2021Q1', 2: '2021Q2', 3: '2021Q3', 4: '2021Q4'}, inplace=True)

# Save the result to a csv file
result_pivot.to_csv('question2result.csv', index=False)
