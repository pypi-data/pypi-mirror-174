# Golden Ratio in Statistics

To determine skewness, mean and deviation with a new approach on continuous data

### Installation
```
pip install golden-ratio-in-statistics
```

### Get started
How to get GRiS result for dataset with this lib:

```Python
# Library import
from golden_ratio_stats.golden_ratio_approch import GoldenRatio

# This line of code will allow shorter imports
from golden_ratio_stats import GoldenRatio

# Instantiate a GoldenRatio object
"""Firstly, import the excel file, then run the library
P.S. Excel file must include name of each column. Like that;

name1	name2	name3	name4 ...
73,36	72,64	68,45	66,52 ...
78,97	67,04	60,85	70,96 ...
...     ...     ...     ...   ...

"""

import os
import pandas as pd

path = r'C:\data'
os.chdir(path)
df = pd.read_excel("my_dataset.xlsx")
# GRiS output
print(GoldenRatio(df))

```