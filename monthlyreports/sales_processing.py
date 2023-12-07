import pandas as pd

class SalesProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def fill_sign(self, x):
        return 'Return' if int(x) <= 0 else 'Sales'

    def read_sales_data(self):
        sales_data = pd.read_csv(self.file_path, skiprows=5, low_memory=False)
        return sales_data

    def process_sales_data(self):
        sales_data = self.read_sales_data()

        expected_columns = ['StoreName', 'BillDate', 'BillNumber', 'Quantity', 'TaxDescription', 'BaseValue', 'Tax', 'Amount', 'HSNCode']
        if not all(col in sales_data.columns for col in expected_columns):
            raise ValueError("Columns do not match the expected format in file: " + self.file_path)

        selected_columns = sales_data.loc[:, expected_columns].copy()  # Use .copy() to avoid setting values on a slice
        selected_columns['Tran Type'] = selected_columns['Quantity'].apply(lambda x: self.fill_sign(x))
        
        # Define replacements using a dictionary
        replacements = {
            'GST 5%': '5',
            'GST 12%': '12',
            'GST 18%': '18',
            'GST 28%': '28'
        }
        
        # Perform replacements using the dictionary
        selected_columns['Tax %'] = selected_columns['TaxDescription'].replace(replacements, regex=True)
        selected_columns['BillDate'] = pd.to_datetime(selected_columns['BillDate'], format='%d/%m/%Y')
        return selected_columns

    # def process_sales_data(self):
    #     sales_data = self.read_sales_data()

    #     expected_columns = ['StoreName', 'BillDate', 'BillNumber', 'Quantity', 'TaxDescription', 'BaseValue', 'Tax', 'Amount', 'HSNCode']
    #     if not all(col in sales_data.columns for col in expected_columns):
    #         raise ValueError("Columns do not match the expected format in file: " + self.file_path)

    #     selected_columns = sales_data[expected_columns]
    #     selected_columns['Tran Type'] = selected_columns['Quantity'].apply(lambda x: self.fill_sign(x))
    #     selected_columns['Tax %'] = selected_columns['TaxDescription'].str.replace('GST 5%', '5').str.replace('GST 12%', '12').str.replace('GST 18%', '18').str.replace('GST 28%', '28')
    #     selected_columns['BillDate'] = pd.to_datetime(selected_columns['BillDate'], format='%d/%m/%Y')
    #     return selected_columns