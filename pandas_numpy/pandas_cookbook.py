import pandas as pd
import numpy as np
import datetime as dt

### create a simple array for dataframe

data = np.random.randn(5,3)

df = pd.DataFrame(data, index=['one','two','three','four','five'],
                  columns=['A','B','C'])

print(df)