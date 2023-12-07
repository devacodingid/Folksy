import os
import pandas as pd
import requests
from sales_processing import SalesProcessor
from tallyposter import generate_xml_from_dataframe as gen

folder_path = 'D:\\Developments\\vscprojects\\Folksy\\monthlyreports\\sales\\'  # Path to the folder containing files
counter = 0
url = 'http:\\localhost:9000'

def first_bill(x, prefix):
    mask = x.str.startswith(prefix)
    return x[mask].iloc[0] if mask.any() else None

def last_bill(x, prefix):
    mask = x.str.startswith(prefix)
    return x[mask].iloc[-1] if mask.any() else None

if __name__ == "__main__":
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

    for file_path in file_paths:
        counter += 1
        processor = SalesProcessor(file_path)
        sales_data = processor.process_sales_data()
        # print(sales_data)
        company = sales_data['StoreName'].iloc[0] 
        outputfile = company + '.xlsx'
        grouped_bills = sales_data.groupby('BillDate').agg({
            'BillNumber': [
                ('Sales_Inv_From', lambda x: first_bill(x, 'WS')),
                ('Sales_Inv_to', lambda x: last_bill(x, 'WS')),
                ('SaleReturn_From', lambda x: first_bill(x, 'LS')),
                ('SaleReturn_to', lambda x: last_bill(x, 'LS'))
            ]
        })
        grouped_bills.columns = ['_'.join(col).strip() for col in grouped_bills.columns.values]

        # Group the data by BillDate
        grouped = sales_data.groupby(['BillDate'])

        # Calculate the sum of BaseValue, Tax, and Amount for each group
        summed = grouped.agg({'BaseValue': 'sum', 'Tax': 'sum', 'Amount': 'sum'})

        # Pivot the data to create columns for CGST and SGST
        pivoted = sales_data.pivot_table(index=['BillDate'], columns='TaxDescription', values=['BaseValue', 'Tax', 'Amount'],aggfunc='sum')

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

        merged2 = pd.merge(result, grouped_bills, on=['BillDate'])
        merged2.replace('None','na')
        merged2.columns = ['BillDate', 'Retail_Customer', 'Sales @ 5% GST', 'CGST 2.5%', 'SGST 2.5%', 'Sales @ 12% GST', 'CGST 6%', 'SGST 6%','Sales_Inv_From', 'Sales_Inv_to', 'SaleReturn_From', 'SaleReturn_to']
        desired_order = ['BillDate', 'Sales_Inv_From', 'Sales_Inv_to', 'SaleReturn_From', 'SaleReturn_to','Retail_Customer', 'Sales @ 5% GST', 'CGST 2.5%', 'SGST 2.5%', 'Sales @ 12% GST', 'CGST 6%', 'SGST 6%']
        
        sales_summary = merged2.reindex(columns=desired_order)
        sales_summary = sales_summary.fillna(0)
        sales_summary = sales_summary.round(decimals=2)
        columns_to_convert = ['Retail_Customer', 'Sales @ 5% GST', 'CGST 2.5%', 'SGST 2.5%', 'Sales @ 12% GST', 'CGST 6%', 'SGST 6%']
        sales_summary[columns_to_convert] = sales_summary[columns_to_convert].apply(pd.to_numeric, errors='coerce')
        # Perform the calculation for 'Round off'
        sales_summary['Round off'] = (
            sales_summary['Retail_Customer'] - 
            sales_summary['Sales @ 5% GST'] - 
            sales_summary['CGST 2.5%'] - 
            sales_summary['SGST 2.5%'] - 
            sales_summary['Sales @ 12% GST'] - 
            sales_summary['CGST 6%'] - 
            sales_summary['SGST 6%']
        )

        sales_summary = sales_summary.round(decimals=2)
        with pd.ExcelWriter(outputfile) as writer: 
            sales_summary.to_excel(writer, sheet_name='sales_summary', index=False)
            sales_data.to_excel(writer, sheet_name='sales_data', index=False)

        a = gen(sales_summary, company)
        xmlname = 'output' + str(counter) + '.xml'
        with open(xmlname, 'w') as text_file:
            text_file.write(a)

        posting = requests.post("http://localhost:9000",a)
        print(posting.text)