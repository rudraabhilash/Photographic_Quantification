import pandas as pd
import numpy as np

data_rows = [
    [0.23, 20.0, 1.32],
    [0.54, 54.5, 1.23],
    [0.87, 53.43, 1.87],
    [0.98, 87.34, 1.98],
]

loss_df = pd.DataFrame(data_rows, columns=["comp1", "comp2", "comp3"])

print(loss_df)

