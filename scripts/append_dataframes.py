import pandas as pd
import numpy as np

# Load the original DataFrame from the CSV file
df1 = pd.read_csv('dataframe.csv')

# Create a new DataFrame with random data (size: 10x3)
data2 = {
    'Column1': np.random.randint(0, 10, size=10),
    'Column2': np.random.randint(0, 20, size=10),
    'Column3': np.random.randint(0, 100, size=10)
}

df2 = pd.DataFrame(data2)

# Append df2 to df1
appended_df = pd.concat([df1, df2], ignore_index=True)

print("Original DataFrame:")
print(df1)
print("\nNew DataFrame to append:")
print(df2)
print("\nAppended DataFrame:")
print(appended_df)

# Optionally save the appended DataFrame to a new CSV file
appended_df.to_csv('appended_dataframe.csv', index=False)
