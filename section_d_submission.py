"""
SECTION D - AI-Augmented Learning
Single file containing all submission items.

Run:  python section_d_submission.py
Needs: pip install pandas openpyxl numpy
"""

import numpy as np
import pandas as pd

# =====================================================================
# EXACT PROMPT GIVEN TO THE AI TOOL
# =====================================================================
PROMPT = """
Write a Python script using pandas that:
1. Reads a food delivery orders CSV file and produces a summary table showing
   Total Revenue, Average DeliveryTime, and Order Count grouped by Cuisine.
2. Adds a new column named PerformanceFlag that labels any row with
   DeliveryTime > 60 as 'Delayed' and all others as 'On Time'.
3. Saves the cleaned and enriched output as a new file named
   food_delivery_summary.xlsx using pandas ExcelWriter.
4. Runs without raising an error on a dataset where some Revenue cells are
   blank and at least one DeliveryTime value is negative (a data entry error).
"""


def original_ai_script(csv_path="food_delivery_orders.csv",
                       out_path="food_delivery_summary_ORIGINAL.xlsx"):
    df = pd.read_csv(csv_path)

    summary = df.groupby("Cuisine").agg(
        Total_Revenue=("Revenue", "sum"),
        Avg_DeliveryTime=("DeliveryTime", "mean"),
        Order_Count=("OrderID", "count"),
    ).reset_index()

    df["PerformanceFlag"] = np.where(df["DeliveryTime"] > 60, "Delayed", "On Time")

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    return df, summary

# =====================================================================
# TEST DATASET (>= 3 blank Revenue cells, one DeliveryTime of -5,
# plus a fully empty row)
# =====================================================================
def make_test_csv(path="food_delivery_orders.csv"):
    data = {
        "OrderID":      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Cuisine":      ["Italian", "Indian", "Italian", "Chinese", "Indian",
                         "Chinese", "Italian", "Indian", "Chinese", np.nan],
        "Revenue":      [250, np.nan, 300, np.nan, 180, 220, np.nan, 400, 150, np.nan],
        "DeliveryTime": [30, 75, -5, 45, 90, 62, 20, 55, 40, np.nan],
    }
    pd.DataFrame(data).to_csv(path, index=False)
    return path

# =====================================================================
# SUBMIT ITEM 2B - YOUR CORRECTED VERSION 
# =====================================================================
# Steps:
#  1. Run this file, open food_delivery_summary_ORIGINAL.xlsx.
#  2. Compare the Summary and Cleaned_Data sheets against the CSV by hand.
#     Ask yourself for each cuisine: does the average look right? Is the
#     -5 row flagged sensibly? What happened to the blank rows/cells?
#  3. Copy original_ai_script below, rename it corrected_script, and fix
#     what you find.
def corrected_script(csv_path="food_delivery_orders.csv",
                     out_path="food_delivery_summary.xlsx"):
    df = pd.read_csv(csv_path)

    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
    df["DeliveryTime"] = pd.to_numeric(df["DeliveryTime"], errors="coerce")

    df.loc[df["DeliveryTime"] < 0, "DeliveryTime"] = np.nan

    df = df.dropna(subset=["OrderID", "Cuisine"])

    df["PerformanceFlag"] = np.where(
        df["DeliveryTime"].isna(),
        "Invalid/Missing",
        np.where(df["DeliveryTime"] > 60, "Delayed", "On Time")
    )

    summary = df.groupby("Cuisine").agg(
        Total_Revenue=("Revenue", "sum"),
        Avg_DeliveryTime=("DeliveryTime", "mean"),
        Order_Count=("OrderID", "count"),
    ).reset_index()

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    return df, summary


# =====================================================================
# SUBMIT ITEM 3 - WRITTEN NOTE (3-4 lines, YOUR words)
# =====================================================================
# Cover: (a) what you changed, (b) which specific input exposed the bug,
# (c) why the AI's original version failed on that input.
NOTE = """
I changed the script to safely handle blank Revenue cells and invalid DeliveryTime values.
The DeliveryTime value of -5 exposed the problem because the original AI script treated it as On Time.
I changed negative DeliveryTime values to missing values and added an Invalid/Missing flag.
This prevents incorrect delivery-time results while allowing the script to run without errors.
"""

if __name__ == "__main__":

    csv = make_test_csv()

    df_original, summary_original = original_ai_script(csv)

    print("ORIGINAL SUMMARY:")
    print(summary_original)

    print("\nORIGINAL DATA:")
    print(df_original)

    df_corrected, summary_corrected = corrected_script(csv)

    print("\nCORRECTED SUMMARY:")
    print(summary_corrected)

    print("\nCORRECTED DATA:")
    print(df_corrected)

    print("\nCorrected Excel file created: food_delivery_summary.xlsx")