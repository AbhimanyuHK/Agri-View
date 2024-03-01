import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

from service import HttpClient

st.set_page_config(
    page_title="Today's Agri Price Dashboard",
    page_icon="✅",
    layout="wide",
)

df = pd.DataFrame(HttpClient().data_list())
df["modal_price"] = df["modal_price"].astype(int)
df["max_price"] = df["max_price"].astype(int)
df["min_price"] = df["min_price"].astype(int)

print(df.columns)
# dashboard title
st.title("Today's Agri Price Dashboard")

# top-level filters
# state_filter = st.selectbox("Select the State", pd.unique(df["state"]))
commodity_filter = st.selectbox("Select the commodity", pd.unique(df["commodity"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
# if state_filter:
# df = df[df["state"] == state_filter]

# if commodity_filter:
df = df[df["commodity"] == commodity_filter]

# creating KPIs
modal_price = df[df['modal_price'] > 0.1]["modal_price"].max().item()
min_price = df[df['min_price'] > 0.1]["min_price"].min().item()
max_price = np.max(df["max_price"]).item()

Commodity_Uom = df['Commodity_Uom'].values[0]

max_modal_price_df = df[df['modal_price'] == df[df['modal_price'] > 0.1]["modal_price"].max()]
min_model_price_df = df[df['modal_price'] == df[df['modal_price'] > 0.1]["modal_price"].min()]
# max_price_df = df[df['max_price'] == df['max_price'].max()]

# model_state = modal_price_df['state'].values[0]
min_state = min_model_price_df['state'].values[0]
min_state_model_price = min_model_price_df['modal_price'].values[0]
min_state_apmc_model_price = min_model_price_df['apmc'].values[0]

max_state = max_modal_price_df['state'].values[0]
max_state_model_price = max_modal_price_df['modal_price'].values[0]
max_state_apmc_model_price = max_modal_price_df['apmc'].values[0]

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="⏳ Avg. Model Price ( ₹ )",
        value=f"{round(modal_price)}",
        delta=round(modal_price) - min_price,
        help=Commodity_Uom
    )

    kpi2.metric(
        label="Min Price ( ₹ )",
        value=int(min_price),
        delta=round(modal_price - min_price),
        help=Commodity_Uom
    )

    kpi3.metric(
        label="Max Price ( ₹ )",
        value=f"{round(max_price, 2)}",
        delta=round(modal_price) - round(max_price),
        help=Commodity_Uom
    )

    st.write('\n')
    st.write('\n')

    kpi1_s, kpi2_s = st.columns(2)

    kpi1_s.metric(
        label=f"⏳ (Max) {max_state} - {max_state_apmc_model_price} ( ₹ )",
        value=f"{round(max_state_model_price)}",
    )
    kpi2_s.metric(
        label=f"⏳ (Min) {min_state} - {min_state_apmc_model_price} ( ₹ )",
        value=f"{round(min_state_model_price)}",
    )

    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Linear Price Chart")
        st.line_chart(df, x="state", y="modal_price")

    with fig_col2:
        st.markdown("### Histogram Price Chart")
        fig2 = px.histogram(data_frame=df, x="modal_price")
        st.write(fig2)

    st.markdown("### Detailed Data View")
    new_df = df[['state', 'apmc', 'commodity', 'min_price', 'modal_price', 'max_price', 'Commodity_Uom']]
    st.dataframe(new_df)
