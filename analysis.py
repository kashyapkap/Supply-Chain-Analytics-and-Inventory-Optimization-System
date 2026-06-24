# ============================
# IMPORT LIBRARIES
# ============================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================
# LOAD DATASET
# ============================
df = pd.read_csv("supply_chain_data.csv")

# ============================
# CALCULATED COLUMNS
# ============================

# Inventory Value
df["Inventory Value"] = df["Stock levels"] * df["Price"]

# Stock Status
df["Stock Status"] = df["Stock levels"].apply(
    lambda x: "Low Stock" if x < 20 else "Normal"
)

print(df[["SKU", "Stock levels", "Price", "Inventory Value", "Stock Status"]].head())

# ============================
# KPI ANALYSIS
# ============================

print("\n----- KPI ANALYSIS -----")

print("Total Revenue:",
      round(df["Revenue generated"].sum(),2))

print("Average Stock Level:",
      round(df["Stock levels"].mean(),2))

print("Average Defect Rate:",
      round(df["Defect rates"].mean(),2))

print("Total Inventory Value:",
      round(df["Inventory Value"].sum(),2))


# ============================
# LOW STOCK ANALYSIS
# ============================

low_stock = df[df["Stock levels"] < 20]

print("\n----- LOW STOCK PRODUCTS -----")

print(
    low_stock[
        ["SKU",
         "Product type",
         "Stock levels"]
    ]
)

# ============================
# ABC ANALYSIS
# ============================

abc = df[["SKU", "Revenue generated"]].sort_values(
    by="Revenue generated",
    ascending=False
)

# Calculate cumulative revenue
abc["Cumulative Revenue"] = (
    abc["Revenue generated"].cumsum()
)

# Calculate cumulative percentage
total_revenue = abc["Revenue generated"].sum()

abc["Cumulative Percentage"] = (
    abc["Cumulative Revenue"] / total_revenue
) * 100


# Function to classify products
def classify(x):
    if x <= 70:
        return "A"
    elif x <= 90:
        return "B"
    else:
        return "C"


# Assign classes
abc["Class"] = abc["Cumulative Percentage"].apply(classify)

print("\n----- ABC CLASSIFICATION -----")

print(abc["Class"].value_counts())

# ============================
# ABC VISUALIZATION
# ============================

abc_count = abc["Class"].value_counts()

plt.figure(figsize=(6,6))

plt.pie(
    abc_count.values,
    labels=abc_count.index,
    autopct="%1.1f%%"
)

plt.title("ABC Classification")

# Save the graph
plt.savefig("graphs/abc_analysis.png")

# Display the graph
plt.show()

# ============================
# INVENTORY OPTIMIZATION
# ============================

# Daily Demand
df["Daily Demand"] = df["Number of products sold"] / 30

# Demand standard deviation
df["Demand Std"] = (
    df["Number of products sold"].std() / 30
)

# Z-value for 90% service level
z = 1.28

df["Safety Stock"] = (
    z *
    df["Demand Std"] *
    np.sqrt(df["Lead times"])
)



# Reorder Point
df["Reorder Point"] = (
    df["Daily Demand"] * df["Lead times"]
) + df["Safety Stock"]

# Reorder Alert
df["Reorder Alert"] = df.apply(
    lambda x:
    "Reorder Needed"
    if x["Stock levels"] < x["Reorder Point"]
    else "Sufficient",
    axis=1
)

print("\n----- REORDER STATUS -----")

print(df["Reorder Alert"].value_counts())

# ============================
# EOQ ANALYSIS
# ============================

# Annual Demand
df["Annual Demand"] = df["Number of products sold"] * 12

# Assumptions
ordering_cost = 100
holding_cost = 10

# EOQ
df["EOQ"] = np.sqrt(
    (2 * df["Annual Demand"] * ordering_cost)
    / holding_cost
)

print("\n----- EOQ ANALYSIS -----")

print(
    df[
        ["SKU",
         "Annual Demand",
         "EOQ"]
    ].head(10)
)

# ============================
# EOQ CATEGORY
# ============================

df["EOQ Category"] = pd.cut(
    df["EOQ"],
    bins=3,
    labels=["Low", "Medium", "High"]
)

print("\n----- EOQ CATEGORY -----")
print(df["EOQ Category"].value_counts())

# ============================
# EOQ CATEGORY GRAPH
# ============================

eoq_count = df["EOQ Category"].value_counts()

plt.figure(figsize=(6,5))

plt.bar(
    eoq_count.index,
    eoq_count.values
)

plt.xlabel("EOQ Category")
plt.ylabel("Number of Products")
plt.title("EOQ Category Distribution")

plt.savefig("graphs/eoq_category.png")

plt.show()

# ============================
# SUPPLIER ANALYSIS
# ============================

# Revenue by Supplier
supplier_revenue = df.groupby(
    "Supplier name"
)["Revenue generated"].sum()

print("\n----- REVENUE BY SUPPLIER -----")

print(supplier_revenue)


# Average Defect Rate by Supplier
supplier_defect = df.groupby(
    "Supplier name"
)["Defect rates"].mean()

print("\n----- DEFECT RATE BY SUPPLIER -----")

print(supplier_defect)

print("\n----- BEST SUPPLIER -----")

best_supplier = supplier_revenue.idxmax()

print("Highest Revenue Supplier:", best_supplier)

best_quality_supplier = supplier_defect.idxmin()

print("Lowest Defect Rate Supplier:", best_quality_supplier)

# ============================
# TRANSPORTATION ANALYSIS
# ============================

transport_cost = df.groupby(
    "Transportation modes"
)["Costs"].mean()

print("\n----- TRANSPORTATION COST ANALYSIS -----")

print(transport_cost)

# Cheapest and most expensive mode
cheapest_mode = transport_cost.idxmin()
expensive_mode = transport_cost.idxmax()

print("\nCheapest Transportation Mode:", cheapest_mode)
print("Most Expensive Transportation Mode:", expensive_mode)

# ============================
# REVENUE BY PRODUCT TYPE
# ============================

revenue_product = df.groupby(
    "Product type"
)["Revenue generated"].sum()

plt.figure(figsize=(7,5))

plt.bar(
    revenue_product.index,
    revenue_product.values
)

plt.xlabel("Product Type")
plt.ylabel("Revenue")
plt.title("Revenue by Product Type")

plt.savefig("graphs/revenue_product_type.png")

plt.show()

# ============================
# SUPPLIER REVENUE GRAPH
# ============================

plt.figure(figsize=(7,5))

plt.bar(
    supplier_revenue.index,
    supplier_revenue.values
)

plt.xlabel("Supplier")
plt.ylabel("Revenue")
plt.title("Revenue by Supplier")

plt.savefig("graphs/supplier_revenue.png")

plt.show()

# ============================
# TRANSPORTATION COST GRAPH
# ============================

plt.figure(figsize=(7,5))

plt.bar(
    transport_cost.index,
    transport_cost.values
)

plt.xlabel("Transportation Mode")
plt.ylabel("Average Cost")

plt.title("Transportation Cost Analysis")

plt.savefig("graphs/transport_cost.png")

plt.show()

# ============================
# DEFECT RATE GRAPH
# ============================

plt.figure(figsize=(7,5))

plt.bar(
    supplier_defect.index,
    supplier_defect.values
)

plt.xlabel("Supplier")
plt.ylabel("Average Defect Rate")

plt.title("Supplier Quality Analysis")

plt.savefig("graphs/defect_rate.png")

plt.show()

# ============================
# INVENTORY DISTRIBUTION
# ============================

inventory_distribution = df.groupby(
    "Product type"
)["Inventory Value"].sum()

plt.figure(figsize=(6,6))

plt.pie(
    inventory_distribution.values,
    labels=inventory_distribution.index,
    autopct="%1.1f%%"
)

plt.title("Inventory Value Distribution")

plt.savefig("graphs/inventory_distribution.png")

plt.show()

# ============================
# EXPORT RESULTS
# ============================

df.to_csv(
    "supply_chain_analysis_results.csv",
    index=False
)

print("\nResults exported successfully!")





