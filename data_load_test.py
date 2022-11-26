import sys
sys.path.append("/home/patrick/pydicer")

from pathlib import Path

from pydicer.utils import read_converted_data

df = read_converted_data(Path("/home/patrick/tcia_pancreas"))

print(df)
print(df.columns)
