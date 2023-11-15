import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv('D:\\Developments\\vscprojects\\Folksy\\dailycash\\sales.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Streamlit app
st.title('Amounts by Store Over Time')

# Group data by Store
grouped_data = df.groupby('Store')

# Plot using matplotlib
plt.figure(figsize=(10, 6))
for store, data in grouped_data:
    plt.plot(data['Date'], data['Amount'], marker='o', label=f'Store {store}')

plt.xlabel('Date')
plt.ylabel('Amount')
plt.title('Amount Over Time for All Stores')
plt.legend()
plt.xticks(rotation=45)

# Display line chart using st.pyplot
st.pyplot(plt)