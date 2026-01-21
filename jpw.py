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

# Probability Distributions

# Probability distributions, on the other hand, describe the probabilities associated with the possible outcomes of a 
# random variable. They specify how likely each outcome of the random variable is to occur. In essence, a 
# probability distribution assigns probabilities to each possible value that a random variable can take.

# The probability distribution for the random variable X specifies the probabilities associated with each possible outcome. 
# Since the die is fair, each outcome (1, 2, 3, 4, 5, or 6) has an equal probability of 1/6​. So, the probability distribution 
# might look like this:
# P(X =1) = 1/6 
# ...
# P(X =5) = 1/6
# P(X =6) = 1/6

#  Normal Distribution - 
# The normal distribution, also known as the Gaussian distribution, is a continuous probability distribution that is 
# symmetric about its mean, with the shape of a bell curve.Mathematically, the distribution is defined by its PDF. 
# A random variable X is said to follow a normal distribution if its probability density function is defined as below:
# f(x) = (1 / (σ * sqrt(2π))) * exp(-0.5 * ((x - μ) / σ)^2)
# where:
# f(x) is the value of the PDF at point x.
# μ is the mean of the distribution. The average value of the distribution, which determines the center of the bell curve.
# σ is the standard deviation of the distribution. A measure of the spread or dispersion of the distribution.  
# exp is the exponential function.

# The probability density function (PDF) is a function that describes the likelihood of a continuous random variable 
# taking on a specific value. The PDF provides the relative likelihood of different outcomes, but it does not give the actual 
# probability of a specific outcome occurring. Instead, the probability of observing a value within a certain range is 
# obtained by integrating the PDF over that range.
# Empirical Rule: In many cases, the distribution of data follows a normal distribution. According to the empirical rule:

# Approximately 68% of the data falls within one standard deviation of the mean.
# Approximately 95% of the data falls within two standard deviations of the mean.
# Approximately 99.7% of the data falls within three standard deviations of the mean.


# Cumulative Distribution Function (CDF)
# The Cumulative Distribution Function (CDF) of a probability distribution provides the probability that a random variable 
# is less than or equal to a specified point.
# When utilising the CDF, it’s essential to note that by default, it calculates the probability of a range 
# less than or equal to the specified value. In the context of using the cumulative distribution in libraries like Pandas, 
# the value provided is inclusive. However, if you want the probability of a value exceeding the specified threshold, 
# you can readily obtain it by subtracting the CDF value from 1.


# Percentage Point Function (PPF)
# The Percentage Point Function (PPF), also known as the inverse cumulative distribution function (CDF), is the 
# mathematical function that provides the value for which a given percentage of observations fall below. 
# In simpler terms, it gives the cutoff value for a specified percentile or probability.

# For example, if you have a normal distribution and you want to find the value below which 95% of the data falls, 
# you would use the PPF to obtain this value.

# The PPF is the inverse of the CDF. While the CDF gives the probability that a random variable is less than or 
# equal to a specified point, the PPF gives the point for which a certain probability is less than or equal to.

# PDF (Probability Density Function): Use pdf() function.

# CDF (Cumulative Distribution Function): Use cdf() function.
# PPF (Percentage Point Function, also known as the inverse CDF): Use ppf() function.
# sample python code for pdf, cdf, ppf using scipy.stats
from scipy.stats import norm
# Parameters for the normal distribution
mu,sigma, x = 0, 1, 1.0  # Mean, Standard deviation, x value
pdf_value = norm.pdf(x, mu, sigma)
cdf_value = norm.cdf(x, mu, sigma)
ppf_value = norm.ppf(0.95, mu, sigma)  #95th percentile
print(f'PDF value at x={x}: {pdf_value}')
print(f'CDF value at x={x}: {cdf_value}')
print(f'PPF value at 95th percentile: {ppf_value}')

# Example output:
# PDF value at x=1.0: 0.24197072451914337
# CDF value at x=1.0: 0.8413447460685429
# PPF value at 95th percentile: 1.644853626951472