import pandas as pd

# Load the CSV dataset
df = pd.read_csv("Task4_Data.csv")

# Display the first five rows
print(df.head())

# Descriptive statistics
print("\nDescriptive Statistics:")
print(df[["Revenue", "Delivery Time", "Rating"]].describe())

# Calculate Q1 and Q3
Q1 = df["Delivery Time"].quantile(0.25)
Q3 = df["Delivery Time"].quantile(0.75)

# Calculate IQR
IQR = Q3 - Q1

# Calculate lower and upper bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Print IQR analysis
print("\nIQR Analysis:")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)

# Find outliers
outliers = df[
    (df["Delivery Time"] < lower_bound) |
    (df["Delivery Time"] > upper_bound)
]

print("\nOutliers:")
print(outliers[["Delivery Time"]])

# Clean labelled summary
print("\nDELIVERY PERFORMANCE SUMMARY")
print("----------------------------")
print("Mean Delivery Time:", df["Delivery Time"].mean())
print("Median Delivery Time:", df["Delivery Time"].median())
print("Mode Delivery Time:", df["Delivery Time"].mode()[0])
print("Standard Deviation:", df["Delivery Time"].std())
print("Variance:", df["Delivery Time"].var())
print("Minimum Delivery Time:", df["Delivery Time"].min())
print("Maximum Delivery Time:", df["Delivery Time"].max())
print("25th Percentile (Q1):", Q1)
print("75th Percentile (Q3):", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)

# Business interpretation comments:
# A positive correlation means that two variables tend to increase together.
# A negative correlation between DeliveryTime and Rating would suggest that longer delivery times are associated with lower ratings.
# The correlation between Revenue and DeliveryTime can help the business understand whether higher-value orders are associated with longer delivery times.

# Calculate correlation matrix
correlation_matrix = df[["Revenue", "Delivery Time", "Rating"]].corr()

print("\nCORRELATION MATRIX")
print("------------------")
print(correlation_matrix)
