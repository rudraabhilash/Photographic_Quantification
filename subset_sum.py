# A private credit fund is constructing a loan pool from a universe of illiquid corporate loans.
# Each loan is indivisible (either included or excluded).

# Construct a subset of loans such that:
# Total portfolio exposure is exactly equal to a target notional T.

# 🧠 Why This is NP-Hard - 
# Loans are illiquid → no fractional selection
# Exact funding is required → equality constraint
# Combinatorial explosion: 2^N possible portfolios
# Accept approximation
# Accept randomization
# Accept exponential in N


# Solution - 
# classic DP fails once N*Sum >> 10^9
# Case 1 -> N<= 40-50, sum is HUGE:
# Split set in two halves - 
# S1 = 2^(N/2)
# S2 = 2^(N/2)
# Sort one list, binary search other list for T - s1

# Case 2 -> sum <= 10^7, N is HUGE:
# 2️⃣ Core Algorithm (High Level)
# Repeat K times:
# Randomly choose a subset S
# Compute its sum
# Measure error ∣sum−T∣
# Keep the best solution found so far
# This is Monte Carlo search.

# 3️⃣ Why Random Subsets Even Work
# Important statistical fact:
# For large N, subset sums concentrate around the mean.
# Then random subsets tend to cluster near μ
# So if T is near μ, random sampling works shockingly well.

import random

def monte_carlo_subset_sum(a, T, K=10_000): # Time: O(N*K), Memory: O(N)
    n = len(a)

    best_error = float("inf")
    best_subset = None
    best_sum = None

    for _ in range(K):
        current_subset = []
        current_sum = 0

        # Randomly choose subset
        for i in range(n):
            if random.random() < 0.5:   # include with 50% probability
                current_subset.append(a[i])
                current_sum += a[i]

        # Measure error
        error = abs(current_sum - T)

        # Keep best solution
        if error < best_error:
            best_error = error
            best_subset = current_subset
            best_sum = current_sum

            # Early exit if perfect match found
            if best_error == 0:
                break

    return best_subset, best_sum, best_error
a = [3, 7, 12, 19, 25]
T = 40

subset, subset_sum, error = monte_carlo_subset_sum(a, T, K=100_000)

print("Subset:", subset)
print("Sum:", subset_sum)
print("Error:", error)

# Important Notes
# This does not guarantee optimal solution
# Increasing K improves quality
# Works best when:
# Many combinations exist
# Target is not extreme
# Exact equality not mandatory