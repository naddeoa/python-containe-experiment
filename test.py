from time import perf_counter
import pandas as pd
import io
from whylogs.core import DatasetProfile
from time import perf_counter


file_name = './data/lending_club.csv'
file = open(file_name, 'rb')
csv = file.read()
print(type(csv))

print("starting")
profile = DatasetProfile()
b = io.BytesIO(csv)
print("about to decode bytes")
df = pd.read_csv(b)
print(df)
start = perf_counter()
profile.track(df)
end = perf_counter()
print(f'done in {end-start}s')
print(profile.view().to_pandas())
