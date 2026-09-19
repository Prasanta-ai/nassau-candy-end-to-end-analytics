from pathlib import Path

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import streamlit as st

# 1. Added Page Configaration

st.set_page_config(
    page_title = "Nassau Candy Profitability Dashboard",
    page_icon = "🍬",
    layout = "wide"
)

st.title("🍬 Nassau Candy Distributor")

st.caption( "Product Line Profitability & Margin Performance Dashboard")

# 2. Define Project File Paths

BASE_DIR = Path(__file__).resolve().parent

FILES = {
    # Main cleaned dataset
    "clean":
        BASE_DIR / "data" / "processed" /
        "Cleaned_Nassau_Candy_Distributor_Dataset.csv",

    # Phase 1 and Phase 2 reports
    "phase_1":
        BASE_DIR / "reports" / "phase_1" /
        "Phase_1_Data_Understanding_Report.csv",

    "phase_2":
        BASE_DIR / "reports" / "phase_2" /
        "Phase_2_Data_Quality_Report.csv",

    # Profitability reports
    "profitability_metrics":
        BASE_DIR / "reports" / "profitability" /
        "Phase_3.1_Profitability_Metric_Calculation_Report.csv",

    "product_report":
        BASE_DIR / "reports" / "profitability" /
        "Phase_3.2_Product_Level_Profitability_Analysis.csv",

    "division_report":
        BASE_DIR / "reports" / "profitability" /
        "Phase_3.3_Division_Level_Performance_Analysis.csv",

    # Pareto reports
    "revenue_pareto":
        BASE_DIR / "reports" / "pareto" /
        "Revenue_Pareto_Report.csv",

    "profit_pareto":
        BASE_DIR / "reports" / "pareto" /
        "Profit_Pareto_Report.csv",

    "pareto_summary":
        BASE_DIR / "reports" / "pareto" /
        "Phase_3.4_Pareto_Analysis_Summary_Report.csv",

    # Geographic reports
    "state_report":
        BASE_DIR / "reports" / "geographic" /
        "State_Concentration_Analysis.csv",

    "region_report":
        BASE_DIR / "reports" / "geographic" /
        "Region_Concentration_Analysis.csv",

    "geo_summary":
        BASE_DIR / "reports" / "geographic" /
        "Phase_3.4_State_Concentration_Over_Dependency_Summary.csv",

    # Cost diagnostics reports
    "cost_report":
        BASE_DIR / "reports" / "cost_diagnostics" /
        "Cost_Structure_Diagnostics.csv",

    "cost_summary":
        BASE_DIR / "reports" / "cost_diagnostics" /
        "Cost_Diagnostics_Summary.csv",

    # Margin volatility reports
    "company_margin":
        BASE_DIR / "reports" / "margin_volatility" /
        "Monthly_Company_Margin.csv",

    "division_volatility":
        BASE_DIR / "reports" / "margin_volatility" /
        "Division_Margin_Volatility_Report.csv",

    "product_volatility":
        BASE_DIR / "reports" / "margin_volatility" /
        "Product_Margin_Volatility_Report.csv",

    "margin_summary":
        BASE_DIR / "reports" / "margin_volatility" /
        "Margin_Volatility_Analysis_Summary.csv"
}

# 3. Load CSV Files

@st.cache_data
def load_csv(path):
    path = Path(path)

    if not path.exists():
        return None

    return pd.read_csv(path)


# Load cleaned dataset
df = load_csv(FILES["clean"])

if df is None:
    st.error(
        "Cleaned dataset not found at "
        "data/processed/Cleaned_Nassau_Candy_Distributor_Dataset.csv"
    )
    st.stop()


# Validate required columns
required_columns = [
    "Order ID",
    "Order Date",
    "Division",
    "Region",
    "State/Province",
    "Product ID",
    "Product Name",
    "Sales",
    "Units",
    "Gross Profit",
    "Cost"
]

missing_required_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_required_columns:
    st.error(
        "The cleaned dataset is missing required columns: "
        + ", ".join(missing_required_columns)
    )
    st.stop()


# Clean text columns
text_columns = [
    "Division",
    "Region",
    "State/Province",
    "Product Name",
    "Product ID"
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )


# Convert Order Date to datetime safely
order_date_text = (
    df["Order Date"]
    .astype(str)
    .str.strip()
)

df["Order Date"] = pd.to_datetime(
    order_date_text,
    format="%d-%m-%Y",
    errors="coerce"
)

# Fallback for any rows stored in another parseable date format
failed_date_mask = df["Order Date"].isna()

if failed_date_mask.any():
    df.loc[failed_date_mask, "Order Date"] = pd.to_datetime(
        order_date_text[failed_date_mask],
        dayfirst=True,
        errors="coerce"
    )

if df["Order Date"].notna().sum() == 0:
    st.error(
        "Order Date conversion failed. Please verify the Order Date format "
        "in the cleaned dataset."
    )
    st.stop()


# 4. Load Reports
reports = {
    key: load_csv(path)
    for key, path in FILES.items()
    if key != "clean"
}


# 5. Create live Product Metrics function

def create_product_metrics(data):

    product = (

        data.groupby(
            [
                "Product ID",
                "Product Name",
                "Division"
            ],
            as_index=False
        )

        .agg(

            Total_Sales=("Sales", "sum"),

            Total_Units=("Units", "sum"),

            Total_Cost=("Cost", "sum"),

            Total_Gross_Profit=(
                "Gross Profit",
                "sum"
            )
        )
    )


    product["Gross_Margin(%)"] = np.where(

        product["Total_Sales"] != 0,

        (
            product["Total_Gross_Profit"]
            /
            product["Total_Sales"]
        ) * 100,

        np.nan
    )


    product["Profit_per_Unit"] = np.where(

        product["Total_Units"] != 0,

        product["Total_Gross_Profit"]
        /
        product["Total_Units"],

        np.nan
    )


    product["Cost_Ratio(%)"] = np.where(

        product["Total_Sales"] != 0,

        (
            product["Total_Cost"]
            /
            product["Total_Sales"]
        ) * 100,

        np.nan
    )


    total_sales = product[
        "Total_Sales"
    ].sum()


    total_profit = product[
        "Total_Gross_Profit"
    ].sum()


    product[
        "Revenue_Contribution(%)"
    ] = (

        product["Total_Sales"]
        /
        total_sales
    ) * 100


    product[
        "Profit_Contribution(%)"
    ] = (

        product["Total_Gross_Profit"]
        /
        total_profit
    ) * 100


    return product

# 6. Division calculation function

def create_division_metrics(data):

    division = (

        data.groupby(
            "Division",
            as_index=False
        )

        .agg(

            Total_Sales=("Sales", "sum"),

            Total_Units=("Units", "sum"),

            Total_Cost=("Cost", "sum"),

            Total_Gross_Profit=(
                "Gross Profit",
                "sum"
            )
        )
    )


    division["Gross_Margin(%)"] = (

        division["Total_Gross_Profit"]
        /
        division["Total_Sales"]
    ) * 100


    division[
        "Revenue_Contribution(%)"
    ] = (

        division["Total_Sales"]
        /
        division["Total_Sales"].sum()
    ) * 100


    division[
        "Profit_Contribution(%)"
    ] = (

        division["Total_Gross_Profit"]
        /
        division["Total_Gross_Profit"].sum()
    ) * 100


    return division

# 7. Monthly Margin function

def create_monthly_margin(
    data,
    group=None
):

    temp = data.dropna(
        subset=["Order Date"]
    ).copy()


    temp["Month"] = (

        temp["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )


    if group is None:

        group_columns = ["Month"]

    else:

        group_columns = [
            group,
            "Month"
        ]


    monthly = (

        temp.groupby(
            group_columns,
            as_index=False
        )

        .agg(

            Monthly_Sales=(
                "Sales",
                "sum"
            ),

            Monthly_Gross_Profit=(
                "Gross Profit",
                "sum"
            )
        )
    )


    monthly[
        "Monthly_Gross_Margin(%)"
    ] = (

        monthly[
            "Monthly_Gross_Profit"
        ]

        /

        monthly[
            "Monthly_Sales"
        ]

    ) * 100


    return monthly

# 8. Create Pareto function

def create_pareto(
    product,
    value_column,
    contribution_column,
    cumulative_column
):

    pareto = (

        product[
            [
                "Product ID",
                "Product Name",
                "Division",
                value_column
            ]
        ]

        .sort_values(
            value_column,
            ascending=False
        )

        .reset_index(drop=True)
    )


    total = pareto[
        value_column
    ].sum()


    pareto[
        contribution_column
    ] = (

        pareto[value_column]
        /
        total
    ) * 100


    pareto[
        cumulative_column
    ] = (

        pareto[
            contribution_column
        ].cumsum()
    )


    return pareto

#80% counter:
def count_to_80(
    pareto,
    cumulative_column
):

    if pareto.empty:

        return 0


    count = (

        pareto[
            cumulative_column
        ] < 80

    ).sum() + 1


    return min(
        int(count),
        len(pareto)
    )

# 9.Sidebar filters

valid_dates = (
    df["Order Date"]
    .dropna()
)

min_date = (
    valid_dates.min().date()
)

max_date = (
    valid_dates.max().date()
)


st.sidebar.header(
    "Dashboard Controls"
)

#Date Range:
date_range = st.sidebar.date_input(

    "Date Range",

    value=(
        min_date,
        max_date
    ),

    min_value=min_date,

    max_value=max_date
)

if (
    isinstance(date_range, tuple)
    and len(date_range) == 2
):

    start_date, end_date = (
        date_range
    )

else:

    start_date = min_date
    end_date = max_date

#Division filter:
all_divisions = sorted(

    df["Division"]
    .dropna()
    .unique()
    .tolist()
)


selected_divisions = (
    st.sidebar.multiselect(

        "Division",

        options=all_divisions,

        default=all_divisions
    )
)

#Product Search:
product_search = (
    st.sidebar.text_input(

        "Product Search",

        placeholder="e.g. Kazookles"
    )
)

#Margin Threshold Slider:
full_product = (
    create_product_metrics(df)
)


default_margin = float(

    full_product[
        "Gross_Margin(%)"
    ].quantile(0.25)
)


margin_threshold = (
    st.sidebar.slider(

        "Margin Threshold (%)",

        min_value=0.0,

        max_value=100.0,

        value=round(
            default_margin,
            2
        ),

        step=0.5
    )
)

# 10. Dashboard page selector

page = st.sidebar.radio(

    "Dashboard Module",

    [
        "Executive Overview",

        "Product Profitability",

        "Division Performance",

        "Profit Concentration",

        "Cost & Margin Diagnostics",

        "Margin Volatility",

        "Reports & Downloads"
    ]
)

# 11. Apply filters

filtered_df = df[

    (
        df["Order Date"].dt.date
        >= start_date
    )

    &

    (
        df["Order Date"].dt.date
        <= end_date
    )

].copy()

#Division:
if selected_divisions:

    filtered_df = filtered_df[

        filtered_df[
            "Division"
        ].isin(
            selected_divisions
        )

    ]

else:

    filtered_df = (
        filtered_df.iloc[0:0]
    )

#Product search:
if product_search.strip():

    filtered_df = filtered_df[

        filtered_df[
            "Product Name"
        ].str.contains(

            product_search.strip(),

            case=False,

            na=False
        )
    ]

#Check:
if filtered_df.empty:

    st.warning(
        "No data found for selected filters."
    )

    st.stop()

#Calculate current metrics:
product_metrics = (
    create_product_metrics(
        filtered_df
    )
)


division_metrics = (
    create_division_metrics(
        filtered_df
    )
)

# 12. Executive Overview

if page == "Executive Overview":

    st.subheader(
        "Executive Overview"
    )


    total_sales = (
        filtered_df["Sales"].sum()
    )

    total_profit = (
        filtered_df[
            "Gross Profit"
        ].sum()
    )

    total_cost = (
        filtered_df["Cost"].sum()
    )

    total_units = (
        filtered_df["Units"].sum()
    )

    total_orders = (
        filtered_df[
            "Order ID"
        ].nunique()
    )

    gross_margin = (

        total_profit
        /
        total_sales

    ) * 100

#KPI Cards:
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)


    c1.metric(
        "Revenue",
        f"${total_sales:,.2f}"
    )

    c2.metric(
        "Gross Profit",
        f"${total_profit:,.2f}"
    )

    c3.metric(
        "Gross Margin",
        f"{gross_margin:.2f}%"
    )

    c4.metric(
        "Total Cost",
        f"${total_cost:,.2f}"
    )

    c5.metric(
        "Units",
        f"{total_units:,.0f}"
    )

    c6.metric(
        "Unique Orders",
        f"{total_orders:,}"
    )

#Top Products chart:
    top_products = (

        product_metrics
        .sort_values(
            "Total_Gross_Profit",
            ascending=True
        )
        .tail(10)
    )


    fig = px.bar(

        top_products,

        x="Total_Gross_Profit",

        y="Product Name",

        orientation="h",

        color="Division",

        title=(
            "Top Products by Gross Profit"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# 13. Product Profitability module

elif page == "Product Profitability":

    st.subheader(
        "Product Profitability Overview"
    )


    product_metrics[
        "Margin_Risk"
    ] = np.where(

        product_metrics[
            "Gross_Margin(%)"
        ] < margin_threshold,

        "Below Threshold",

        "At / Above Threshold"
    )

#Margin Leaderboard:
    leaderboard = (

        product_metrics
        .sort_values(
            "Gross_Margin(%)",
            ascending=True
        )
    )


    fig = px.bar(

        leaderboard,

        x="Gross_Margin(%)",

        y="Product Name",

        orientation="h",

        color="Division",

        title=(
            "Product-Level Margin Leaderboard"
        )
    )


    fig.add_vline(

        x=margin_threshold,

        line_dash="dash"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Profit Contribution:
    profit_chart = (

        product_metrics
        .sort_values(
            "Profit_Contribution(%)",
            ascending=True
        )
    )


    fig = px.bar(

        profit_chart,

        x="Profit_Contribution(%)",

        y="Product Name",

        orientation="h",

        color="Division",

        title="Product Profit Contribution"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Table:
    st.dataframe(

        product_metrics.round(2),

        use_container_width=True,

        hide_index=True
    )

# 14. Division Performance Dashboard

elif page == "Division Performance":

    st.subheader(
        "Division Performance Dashboard"
    )

#Revenue vs Profit:
    fig = px.bar(

        division_metrics,

        x="Division",

        y=[
            "Total_Sales",
            "Total_Gross_Profit"
        ],

        barmode="group",

        title=(
            "Revenue vs Gross Profit "
            "by Division"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Margin distribution:
    division_monthly = (
        create_monthly_margin(
            filtered_df,
            group="Division"
        )
    )


    fig = px.box(

        division_monthly,

        x="Division",

        y="Monthly_Gross_Margin(%)",

        points="all",

        title=(
            "Margin Distribution "
            "by Division"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Revenue-Profit gap:
    division_metrics[
        "Revenue-Profit Gap (pp)"
    ] = (

        division_metrics[
            "Profit_Contribution(%)"
        ]

        -

        division_metrics[
            "Revenue_Contribution(%)"
        ]
    )


    st.dataframe(

        division_metrics.round(2),

        use_container_width=True,

        hide_index=True
    )

# 15. Profit Concentration / Pareto

elif page == "Profit Concentration":

    st.subheader(
        "Profit Concentration "
        "(Pareto) Analysis"
    )

#Revenue Pareto:
    revenue_pareto = create_pareto(

        product_metrics,

        "Total_Sales",

        "Revenue_Contribution(%)",

        "Cumulative_Revenue(%)"
    )

#Profit Pareto:
    profit_pareto = create_pareto(

        product_metrics,

        "Total_Gross_Profit",

        "Profit_Contribution(%)",

        "Cumulative_Profit(%)"
    )

#80% products:
    revenue_80 = count_to_80(

        revenue_pareto,

        "Cumulative_Revenue(%)"
    )


    profit_80 = count_to_80(

        profit_pareto,

        "Cumulative_Profit(%)"
    )

#KPI cards:
    c1, c2 = st.columns(2)


    c1.metric(
        "Products Required for 80% Revenue",
        revenue_80
    )


    c2.metric(
        "Products Required for 80% Profit",
        profit_80
    )

#Revenue Pareto chart:
    fig = make_subplots(

        specs=[
            [
                {
                    "secondary_y": True
                }
            ]
        ]
    )


    fig.add_trace(

        go.Bar(

            x=revenue_pareto[
                "Product Name"
            ],

            y=revenue_pareto[
                "Total_Sales"
            ],

            name="Revenue"
        ),

        secondary_y=False
    )


    fig.add_trace(

        go.Scatter(

            x=revenue_pareto[
                "Product Name"
            ],

            y=revenue_pareto[
                "Cumulative_Revenue(%)"
            ],

            mode="lines+markers",

            name="Cumulative Revenue %"
        ),

        secondary_y=True
    )


    fig.add_hline(

        y=80,

        line_dash="dash",

        secondary_y=True
    )


    fig.update_layout(

        title="Product Revenue Pareto",

        xaxis_tickangle=-55
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Create the Profit Pareto chart:
    fig = make_subplots(

        specs=[
            [
                {
                    "secondary_y": True
                }
            ]
        ]
    )


    fig.add_trace(

        go.Bar(

            x=profit_pareto[
                "Product Name"
            ],

            y=profit_pareto[
                "Total_Gross_Profit"
            ],

            name="Gross Profit"
        ),

        secondary_y=False
    )


    fig.add_trace(

        go.Scatter(

            x=profit_pareto[
                "Product Name"
            ],

            y=profit_pareto[
                "Cumulative_Profit(%)"
            ],

            mode="lines+markers",

            name="Cumulative Profit %"
        ),

        secondary_y=True
    )


    fig.add_hline(

        y=80,

        line_dash="dash",

        secondary_y=True
    )


    fig.update_layout(

        title="Product Profit Pareto",

        xaxis_tickangle=-55
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 16. Add Geographic Dependency

    st.subheader(
        "State & Region Dependency"
    )

#State analysis:
    state_analysis = (

        filtered_df.groupby(
            "State/Province",
            as_index=False
        )

        .agg(

            Total_Order=(
                "Order ID",
                "nunique"
            ),

            Total_Units=(
                "Units",
                "sum"
            ),

            Total_Sales=(
                "Sales",
                "sum"
            ),

            Total_Gross_Profit=(
                "Gross Profit",
                "sum"
            )
        )
    )

#Contribution:
    state_analysis[
        "Revenue_Share(%)"
    ] = (

        state_analysis[
            "Total_Sales"
        ]

        /

        state_analysis[
            "Total_Sales"
        ].sum()

    ) * 100


    state_analysis[
        "Profit_Share(%)"
    ] = (

        state_analysis[
            "Total_Gross_Profit"
        ]

        /

        state_analysis[
            "Total_Gross_Profit"
        ].sum()

    ) * 100

#Chart:
    state_analysis = (

        state_analysis
        .sort_values(
            "Total_Sales",
            ascending=False
        )
    )


    fig = px.bar(

        state_analysis.head(15),

        x="State/Province",

        y="Revenue_Share(%)",

        title=(
            "Top States / Provinces "
            "by Revenue Share"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Region analysis:
    region_analysis = (

        filtered_df.groupby(
            "Region",
            as_index=False
        )

        .agg(

            Total_Order=(
                "Order ID",
                "nunique"
            ),

            Total_Units=(
                "Units",
                "sum"
            ),

            Total_Sales=(
                "Sales",
                "sum"
            ),

            Total_Gross_Profit=(
                "Gross Profit",
                "sum"
            )
        )
    )

    region_analysis[
        "Revenue_Share(%)"
    ] = (

        region_analysis[
            "Total_Sales"
        ]

        /

        region_analysis[
            "Total_Sales"
        ].sum()

    ) * 100


    region_analysis[
        "Profit_Share(%)"
    ] = (

        region_analysis[
            "Total_Gross_Profit"
        ]

        /

        region_analysis[
            "Total_Gross_Profit"
        ].sum()

    ) * 100

    fig = px.bar(

        region_analysis,

        x="Region",

        y=[
            "Revenue_Share(%)",
            "Profit_Share(%)"
        ],

        barmode="group",

        title=(
            "Regional Revenue "
            "and Profit Dependency"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 17. Cost & Margin Diagnostics

elif page == "Cost & Margin Diagnostics":

    st.subheader(
        "Cost vs Margin Diagnostics"
    )


    cost_report = (
        reports["cost_report"]
    )


    if cost_report is None:

        st.error(
            "Cost_Structure_Diagnostics.csv "
            "not found."
        )

        st.stop()

#Clean names:
    cost_report = (
        cost_report.copy()
    )


    for column in [
        "Product ID",
        "Product Name",
        "Division"
    ]:

        cost_report[column] = (

            cost_report[column]
            .astype(str)
            .str.strip()
        )

#Calculate your quantile thresholds:
    low_margin_threshold = (

        cost_report[
            "Gross_Margin(%)"
        ].quantile(0.25)
    )


    high_cost_threshold = (

        cost_report[
            "Cost_Ratio(%)"
        ].quantile(0.75)
    )


    low_sales_threshold = (

        cost_report[
            "Total_Sales"
        ].quantile(0.25)
    )


    median_sales_threshold = (

        cost_report[
            "Total_Sales"
        ].quantile(0.50)
    )


    low_profit_threshold = (

        cost_report[
            "Total_Gross_Profit"
        ].quantile(0.25)
    )

#Threshold KPI cards:
    t1, t2, t3 = st.columns(3)
    t4, t5 = st.columns(2)


    t1.metric(
        "Low Margin Q1",
        f"{low_margin_threshold:.2f}%"
    )


    t2.metric(
        "High Cost Ratio Q3",
        f"{high_cost_threshold:.2f}%"
    )


    t3.metric(
        "Low Sales Q1",
        f"${low_sales_threshold:,.2f}"
    )


    t4.metric(
        "Median Sales",
        f"${median_sales_threshold:,.2f}"
    )


    t5.metric(
        "Low Profit Q1",
        f"${low_profit_threshold:,.2f}"
    )

# 18. Merge live metrics with final Cost flags

    action_columns = [

        "Product ID",

        "Cost_Heavy",

        "Margin_Poor",

        "Pricing_Inefficiencies",

        "Repricing_Flag",

        "Cost_Renegotiation_Flag",

        "Discontinuation_Review_Flag",

        "Recommended_Action"
    ]

    live_cost = (

        product_metrics.merge(

            cost_report[
                action_columns
            ],

            on="Product ID",

            how="left"
        )
    )

# 19. Cost vs Sales scatter

    fig = px.scatter(

        live_cost,

        x="Total_Cost",

        y="Total_Sales",

        size="Total_Gross_Profit",

        color="Recommended_Action",

        hover_name="Product Name",

        hover_data=[

            "Division",

            "Gross_Margin(%)",

            "Cost_Ratio(%)",

            "Profit_per_Unit"
        ],

        title="Cost vs Sales Scatter Analysis"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 20. Cost Ratio vs Margin chart

    fig = px.scatter(

        live_cost,

        x="Cost_Ratio(%)",

        y="Gross_Margin(%)",

        size="Total_Sales",

        color="Recommended_Action",

        hover_name="Product Name",

        title=(
            "Cost Ratio vs Gross Margin"
        )
    )

#Add your Q3 high-cost threshold:
    fig.add_vline(

        x=high_cost_threshold,

        line_dash="dash",

        annotation_text="High Cost Q3"
    )

#Add your Q1 low-margin threshold:
    fig.add_hline(

        y=low_margin_threshold,

        line_dash="dash",

        annotation_text="Low Margin Q1"
    )

#Also show interactive selected margin:
    fig.add_hline(

        y=margin_threshold,

        line_dash="dot",

        annotation_text=(
            "Selected Margin Threshold"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 21. Recommended Action table

    st.dataframe(

        live_cost[
            [
                "Product Name",
                "Division",

                "Total_Sales",
                "Total_Cost",
                "Total_Gross_Profit",

                "Gross_Margin(%)",
                "Cost_Ratio(%)",
                "Profit_per_Unit",

                "Cost_Heavy",
                "Margin_Poor",

                "Pricing_Inefficiencies",

                "Repricing_Flag",

                "Cost_Renegotiation_Flag",

                "Discontinuation_Review_Flag",

                "Recommended_Action"
            ]
        ].round(2),

        use_container_width=True,

        hide_index=True
    )

# 22. Margin Volatility Dashboard

elif page == "Margin Volatility":

    st.subheader(
        "Margin Volatility KPI"
    )


    company_monthly = (
        create_monthly_margin(
            filtered_df
        )
    )


    division_monthly = (
        create_monthly_margin(
            filtered_df,
            group="Division"
        )
    )

#KPI:
    company_avg = (

        company_monthly[
            "Monthly_Gross_Margin(%)"
        ].mean()
    )


    company_sd = (

        company_monthly[
            "Monthly_Gross_Margin(%)"
        ].std()
    )


    company_min = (

        company_monthly[
            "Monthly_Gross_Margin(%)"
        ].min()
    )


    company_max = (

        company_monthly[
            "Monthly_Gross_Margin(%)"
        ].max()
    )

    c1, c2, c3, c4 = (
        st.columns(4)
    )


    c1.metric(
        "Average Monthly Margin",
        f"{company_avg:.2f}%"
    )


    c2.metric(
        "Margin Volatility SD",
        f"{company_sd:.2f} pp"
    )


    c3.metric(
        "Minimum Margin",
        f"{company_min:.2f}%"
    )


    c4.metric(
        "Maximum Margin",
        f"{company_max:.2f}%"
    )

#Company chart:
    fig = px.line(

        company_monthly,

        x="Month",

        y="Monthly_Gross_Margin(%)",

        markers=True,

        title=(
            "Company Monthly "
            "Gross Margin Trend"
        )
    )


    fig.add_hline(

        y=company_avg,

        line_dash="dash"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Division trend:
    fig = px.line(

        division_monthly,

        x="Month",

        y="Monthly_Gross_Margin(%)",

        color="Division",

        markers=True,

        title=(
            "Monthly Gross Margin "
            "Volatility by Division"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# 23. Reports & Downloads module

#First create:
def convert_csv(data):

    return data.to_csv(
        index=False
    ).encode("utf-8")

#Then page:
if page == "Reports & Downloads":

    st.subheader(
        "Previous Colab Analysis Reports"
    )

#Available reports:
    available_reports = {

        key: value

        for key, value
        in reports.items()

        if value is not None
    }

# Stop cleanly if no archived reports are available
    if not available_reports:
        st.warning(
            "No archived Colab reports were found in the reports folders."
        )
        st.stop()

#Selector:
    selected_report = (
        st.selectbox(

            "Select Report",

            list(
                available_reports.keys()
            )
        )
    )

#Show:
    report_df = (
        available_reports[
            selected_report
        ]
    )


    st.dataframe(

        report_df,

        use_container_width=True,

        hide_index=True
    )

#Download:
    st.download_button(

        "Download Selected Report",

        data=convert_csv(
            report_df
        ),

        file_name=FILES[selected_report].name,

        mime="text/csv"
    )

#Also download current filtered dataset:
    st.download_button(

        "Download Current Filtered Data",

        data=convert_csv(
            filtered_df
        ),

        file_name=(
            "Filtered_Nassau_Candy_Data.csv"
        ),

        mime="text/csv"
    )
