import pandas as pd
import numpy as np

obligors = ["Obligor_A", "Obligor_B", "Obligor_C", "Obligor_D", "Obligor_E", "Obligor_F"]
data_rows = [
    [0.23, 20.0, 1.32, 0.23, 20.0, 1.32],
    [0.54, 54.5, 1.23, 0.54, 54.5, 1.23],
    [0.87, 53.43, 1.87, 0.87, 53.43, 1.87],
    [0.98, 87.34, 1.98, 0.98, 87.34, 1.98],
]

loss_df = pd.DataFrame(data_rows, columns=obligors)

metadata = pd.DataFrame({
    "Obligor": obligors,
    "Region": ["US", "US", "EU", "EU", "APAC", "APAC"],
    "Industry": ["Tech", "Energy", "Tech", "Energy", "Tech", "Energy"],
    "Desk": ["DL", "DL", "IB", "IB", "AMC", "AMC"]
})


