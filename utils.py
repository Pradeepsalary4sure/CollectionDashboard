import pandas as pd
import streamlit as st

# ---------------------------------
# LOAD DATA
# ---------------------------------

@st.cache_data(ttl=300)
def load_data(csv_url):

    df = pd.read_csv(csv_url)

    # Rename Columns
    cols = list(df.columns)

    rename_map = {
        cols[4]: "Loan Amount",          # E
        cols[5]: "Loan Repay Amount",    # F
        cols[7]: "Repay Date",           # H
        cols[9]: "Repay Month",          # J
        cols[11]: "Current Status",      # L
        cols[13]: "Total Received",      # N
        cols[20]: "Executive Name"       # U
    }

    df = df.rename(columns=rename_map)

    # -----------------------------
    # Numeric Columns
    # -----------------------------

    numeric_cols = [
        "Loan Amount",
        "Loan Repay Amount",
        "Total Received"
    ]

    for col in numeric_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    # -----------------------------
    # Date Column
    # -----------------------------

    df["Repay Date"] = pd.to_datetime(
        df["Repay Date"],
        dayfirst=True,
        errors="coerce"
    )

    # Remove time portion
    df["Repay Date"] = df["Repay Date"].dt.normalize()

    # -----------------------------
    # Text Cleanup
    # -----------------------------

    df["Repay Month"] = (
        df["Repay Month"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["Executive Name"] = (
        df["Executive Name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["Current Status"] = (
        df["Current Status"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # -----------------------------
    # Calculated Columns
    # -----------------------------

    df["Pending Amount"] = (
        df["Loan Repay Amount"]
        - df["Total Received"]
    )

    df["Collection %"] = (
        (
            df["Total Received"]
            / df["Loan Repay Amount"]
        )
        .replace([float("inf")], 0)
        .fillna(0)
        * 100
    ).round(2)

    return df


# ---------------------------------
# FILTER DATA
# ---------------------------------

def filter_dataframe(
    df,
    month,
    executive,
    status,
    from_date,
    to_date
):

    temp = df.copy()

    # Convert both sides to date only
    temp["Repay Date"] = pd.to_datetime(temp["Repay Date"]).dt.date

    from_date = pd.to_datetime(from_date).date()
    to_date = pd.to_datetime(to_date).date()

    # Month
    if month != "All":
        temp = temp[temp["Repay Month"].str.strip() == month]

    # Executive
    if executive != "All":
        temp = temp[temp["Executive Name"] == executive]

    # Status
    if status != "All":
        temp = temp[temp["Current Status"] == status]

    # Date
    temp = temp[
        (temp["Repay Date"] >= from_date) &
        (temp["Repay Date"] <= to_date)
    ]

    return temp.reset_index(drop=True)      