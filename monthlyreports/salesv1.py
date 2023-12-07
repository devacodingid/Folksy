import pandas as pd

file = 'P:\\Official\\Folksy\\2023-24\\08_Nov23\\Sales\\FA_SALES_NOV23.csv'

def fill_sign(x):
    return 'Return' if int(x) <= 0 else 'Sales'

# Read the CSV file as data frame
df = pd.read_csv(file, skiprows=5)  # Read the CSV without header

selected_columns = df[['StoreName', 'BillDate', 'BillNumber', 'Quantity', 'TaxDescription','BaseValue','Tax','Amount','HSNCode',]]
selected_columns = selected_columns.copy()
selected_columns['Tran Type'] = selected_columns['Quantity'].apply(lambda x: fill_sign(x))

df = selected_columns
df = df.reset_index(drop=True)

new_order = ['StoreName', 'Tran Type', 'BillDate', 'BillNumber', 'Quantity', 'TaxDescription', 'BaseValue', 'Tax', 'Amount', 'HSNCode']
df = df[new_order]
df['Tax %'] = df['TaxDescription'].str.replace('GST 5%', '5').str.replace('GST 12%', '12')

# Convert the BillDate column to a datetime object
df['BillDate'] = pd.to_datetime(df['BillDate'], format='%d/%m/%Y')

sales_data = df
#-------------------------------------------------------------------------
# Define functions to retrieve first 'WS' and 'LS' bill numbers
def first_WS(x):
    mask = x.str.startswith('WS')
    return x[mask].iloc[0] if mask.any() else None

def last_WS(x):
    mask = x.str.startswith('WS')
    return x[mask].iloc[-1] if mask.any() else None

def first_LS(x):
    mask = x.str.startswith('LS')
    return x[mask].iloc[0] if mask.any() else None

def last_LS(x):
    mask = x.str.startswith('LS')
    return x[mask].iloc[-1] if mask.any() else None

# Group by 'BillDate' and perform necessary aggregations based on conditions
groupedbill = df.groupby('BillDate').agg({
    'BillNumber': [
        ('First WS', first_WS),  # First WS
        ('Last WS', last_WS),  # Last WS
        ('First LS', first_LS),  # First LS
        ('Last LS', last_LS),  # Last LS
    ]
})
groupedbill.columns = ['_'.join(col).strip() for col in groupedbill.columns.values]

# Group the data by BillDate
grouped = df.groupby(['BillDate'])

# Calculate the sum of BaseValue, Tax, and Amount for each group
summed = grouped.agg({'BaseValue': 'sum', 'Tax': 'sum', 'Amount': 'sum'})

# Pivot the data to create columns for CGST and SGST
pivoted = df.pivot_table(index=['BillDate'], columns='TaxDescription', values=['BaseValue', 'Tax', 'Amount'],aggfunc='sum')

# Flatten the column names
pivoted.columns = ['_'.join(col).strip() for col in pivoted.columns.values]

# Merge the two data frames on BillDate
merged = pd.merge(summed, pivoted, on=['BillDate'])

# Calculate CGST and SGST for 5% and 12% taxes
merged['CGST 2.5%'] = merged['Tax_GST 5%'] / 2
merged['SGST 2.5%'] = merged['Tax_GST 5%'] / 2
merged['CGST 6%'] = merged['Tax_GST 12%'] / 2
merged['SGST 6%'] = merged['Tax_GST 12%'] / 2

merged = merged.reset_index()
# Select the columns you're interested in
result = merged[['BillDate', 'Amount', 'BaseValue_GST 5%', 'CGST 2.5%', 'SGST 2.5%', 'BaseValue_GST 12%', 'CGST 6%', 'SGST 6%']]

# Rename the columns to match your desired output
result.columns = ['BillDate', 'Retail_Customer', 'Sales @ 5% GST', 'CGST 2.5%', 'SGST 2.5%', 'Sales @ 12% GST', 'CGST 6%', 'SGST 6%']

merged2 = pd.merge(result, groupedbill, on=['BillDate'])
merged2.replace('None','na')
merged2.columns = ['BillDate', 'Retail_Customer', 'Sales @ 5% GST', 'CGST 2.5%', 'SGST 2.5%', 'Sales @ 12% GST', 'CGST 6%', 'SGST 6%','Sales_Inv_From', 'Sales_Inv_to', 'SaleReturn_From', 'SaleReturn_to']
desired_order = ['BillDate', 'Sales_Inv_From', 'Sales_Inv_to', 'SaleReturn_From', 'SaleReturn_to','Retail_Customer', 'Sales @ 5% GST', 'CGST 2.5%', 'SGST 2.5%', 'Sales @ 12% GST', 'CGST 6%', 'SGST 6%']

sales_summary = merged2.reindex(columns=desired_order)
sales_summary.round(decimals=2) 
print(sales_summary.head())
print(sales_data.head())