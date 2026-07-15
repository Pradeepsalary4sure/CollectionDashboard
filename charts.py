import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ------------------------------------------
# Executive Performance Chart
# ------------------------------------------

def executive_chart(df):

    chart = (
        df.groupby("Executive Name", as_index=False)
        .agg({
            "Total Received": "sum",
            "Loan Repay Amount": "sum"
        })
    )

    chart["Collection %"] = (
        chart["Total Received"] /
        chart["Loan Repay Amount"]
    ).fillna(0) * 100

    chart = chart.sort_values(
        "Collection %",
        ascending=False
    )

    fig = px.bar(
        chart,
        x="Executive Name",
        y="Collection %",
        text="Collection %",
        color="Collection %",
        color_continuous_scale="Blues",
        title="Executive Wise Collection %"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        template="plotly_white",
        xaxis_title="Executive",
        yaxis_title="Collection %",
        coloraxis_showscale=False
    )

    return fig


# ------------------------------------------
# Monthly Collection Trend
# ------------------------------------------

def monthly_chart(df):

    chart = (
        df.groupby("Repay Month", as_index=False)
        .agg({
            "Total Received": "sum"
        })
    )

    fig = px.line(
        chart,
        x="Repay Month",
        y="Total Received",
        markers=True,
        title="Monthly Collection Trend"
    )

    fig.update_layout(
        height=420,
        template="plotly_white"
    )

    return fig


# ------------------------------------------
# Status Distribution
# ------------------------------------------

def status_chart(df):

    chart = (
        df.groupby("Current Status")
        .size()
        .reset_index(name="Count")
    )

    fig = px.pie(
        chart,
        names="Current Status",
        values="Count",
        hole=0.45,
        title="Status Distribution"
    )

    fig.update_layout(
        height=420
    )

    return fig


# ------------------------------------------
# Leaderboard
# ------------------------------------------

def leaderboard_chart(df):

    board = (
        df.groupby("Executive Name", as_index=False)
        .agg({
            "Loan Repay Amount": "sum",
            "Total Received": "sum"
        })
    )

    board["Collection %"] = (
        board["Total Received"] /
        board["Loan Repay Amount"]
    ).fillna(0) * 100

    board = board.sort_values(
        "Collection %",
        ascending=False
    ).head(10)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=board["Collection %"],
            y=board["Executive Name"],
            orientation="h",
            text=board["Collection %"].round(2).astype(str) + "%",
            textposition="outside"
        )
    )

    fig.update_layout(
        title="🏆 Top 10 Collection Executives",
        height=450,
        template="plotly_white",
        yaxis=dict(autorange="reversed"),
        xaxis_title="Collection %",
        yaxis_title=""
    )

    return fig