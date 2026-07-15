import pandas as pd
import streamlit as st

# -------------------------------
# LOAD DATA
# -------------------------------

@st.cache_data(ttl=300)
def load_data(csv_url):

    df = pd.read_csv(csv_url)

    # Rename columns by index
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

    # Numeric conversion
    for col in [
        "Loan Amount",
        "Loan Repay Amount",
        "Total Received"
    ]:
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

    # Date conversion
    df["Repay Date"] = pd.to_datetime(
        df["Repay Date"],
        errors="coerce"
    )

    # Text cleanup
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

    # Pending Amount
    df["Pending Amount"] = (
        df["Loan Repay Amount"] -
        df["Total Received"]
    )

    # Collection %
    df["Collection %"] = (
        (
            df["Total Received"] /
            df["Loan Repay Amount"]
        )
        .replace([float("inf")], 0)
        .fillna(0)
        * 100
    ).round(2)

    return df


# -------------------------------
# FILTER DATA
# -------------------------------

def filter_dataframe(
    df,
    month,
    executive,
    status,
    from_date,
    to_date
):

    temp = df.copy()

    if month != "All":
        temp = temp[
            temp["Repay Month"] == month
        ]

    if executive != "All":
        temp = temp[
            temp["Executive Name"] == executive
        ]

    if status != "All":
        temp = temp[
            temp["Current Status"] == status
        ]

    temp = temp[
        (temp["Repay Date"] >= pd.to_datetime(from_date)) &
        (temp["Repay Date"] <= pd.to_datetime(to_date))
    ]

    return temp.reset_index(drop=True)