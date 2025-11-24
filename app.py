import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="natation", page_icon="🏊")  # , layout="wide")
st.write("# 🏊 Natation - Elsa")

sheet_id = "1dihW4wjFui7uhXVe9pXQXyVt60OdZpGXJEk_V_KZth0"
df = pd.read_excel(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export")

config = {
    "Date": st.column_config.DatetimeColumn(format="DD/MM/YYYY"),
    "Piscine": st.column_config.ListColumn(),
    "Résultats": st.column_config.LinkColumn(display_text="link"),
}
st.dataframe(
    df.drop(columns=["Lieu"]).fillna(value=""),
    column_config=config,
    width="stretch",
    hide_index=True,
)

# Calculate total time in seconds
time = pd.to_datetime(
    df["Temps"].str.extract(r"(\d+):(\d+)\.(\d+)").astype(float).dot([60, 1, 0.01]), unit="s"
)

kwargs = dict(
    legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0.0),
    yaxis=dict(tickformat="%M:%S.%f", title="Temps"),
    xaxis=dict(title=None),
)

for nage in [50, 100]:
    mask = df.Nage.str.startswith(f"{nage}m")
    fig = px.line(df[mask], x="Date", y=time[mask], color="Nage", markers=True, template="seaborn")
    st.plotly_chart(fig.update_layout(**kwargs))
