import pandas as pd

# Load the DataFrame from the CSV file
df = pd.read_csv('dataframe.csv')

# Replace values in Column2 where the value is greater than 10
df['Column2'] = df['Column2'].replace({x: 'High' for x in df['Column2'] if x > 10})

print("DataFrame after replacing values in Column2:")
print(df)