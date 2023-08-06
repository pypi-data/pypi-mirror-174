# Empirical Normality Test 

A normality test based on empirical rule for big data

### Installation
```
pip install big-data-normality
```

### Get started
How to get normality test for dataset with this lib:

```Python
# Library import
from big_data_normality.empirical_normality_test import EmpiricalNormalityTest

# This line of code will allow shorter imports
from big_data_normality import EmpiricalNormalityTest

# Instantiate a EmpiricalNormalityTest object
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
print(EmpiricalNormalityTest(df))
```