import pandas as pd

# Create a DataFrame of size 10x3 from a list of values
data = {
    'Column1': range(10),
    'Column2': [x * 2 for x in range(10)],
    'Column3': [x ** 2 for x in range(10)]
}

df = pd.DataFrame(data)
# Save DataFrame to a CSV file for later use
df.to_csv('dataframe.csv', index=False)
print("DataFrame created and saved as dataframe.csv")
