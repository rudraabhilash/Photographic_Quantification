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
print('loss_df = \n', loss_df)
metadata = pd.DataFrame({
    "Obligor": obligors,
    "Region": ["US", "US", "EU", "EU", "APAC", "APAC"],
    "Industry": ["Tech", "Energy", "Tech", "Energy", "Tech", "Energy"],
    "Desk": ["DL", "DL", "IB", "IB", "AMC", "AMC"]
})

loss_long = (
    loss_df
    .reset_index()
    .melt(id_vars="index", var_name="Obligor", value_name="Loss")
    .rename(columns={"index": "Scenario"})
)
print('loss_long = \n', loss_long)
loss_long = loss_long.merge(metadata, on="Obligor")
print('loss_long = \n', loss_long)
firm_losses = loss_long.groupby("Scenario")["Loss"].sum()
print('firm_losses = \n', firm_losses)

# Example 2: Region-level loss distributions
region_losses = pd.pivot_table(
    loss_long,
    index="Scenario",
    columns="Region",
    values="Loss",
    aggfunc="sum"
)
print('region_losses = \n', region_losses)

# Example 3: Region × Industry aggregation
region_industry_losses = pd.pivot_table(
    loss_long,
    index="Scenario",
    columns=["Region", "Industry"],
    values="Loss",
    aggfunc="sum"
)
print('region_industry_losses = \n', region_industry_losses)
# Example 4: Desk-level loss distributions
desk_losses = pd.pivot_table(
    loss_long,
    index="Scenario",
    columns="Desk",
    values="Loss",
    aggfunc="sum"
)
print('desk_losses = \n', desk_losses)
