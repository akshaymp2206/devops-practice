
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from monitor import check_website

st.set_page_config(page_title="Website Monitor", page_icon="🌐")

st.title("🌐 Website Uptime Monitor")
st.write("Check website availability and response time.")

if "history" not in st.session_state:
    st.session_state.history = []

url = st.text_input("Website URL", "https://example.com")
timeout = st.slider("Timeout (seconds)", 2, 15, 5)

if st.button("Check Website"):
    result = check_website(url.strip(), timeout)

    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "website": url.strip(),
        **result,
    }

    st.session_state.history.append(record)

    if result["status"] == "UP":
        st.success("Website is UP")
    else:
        st.error("Website is DOWN")

    st.write("HTTP status code:", result["status_code"])

    if result["latency_ms"] is not None:
        st.write("Response time:", result["latency_ms"], "ms")

    if result["error"]:
        st.caption(result["error"])

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)

    total = len(df)
    successful = int((df["status"] == "UP").sum())
    uptime = successful / total * 100

    latencies = pd.to_numeric(df["latency_ms"], errors="coerce")
    average = latencies.mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Uptime", f"{uptime:.1f}%")
    col2.metric("Average response", f"{average:.0f} ms" if pd.notna(average) else "N/A")
    col3.metric("Failed checks", total - successful)

    chart_df = df.dropna(subset=["latency_ms"])

    st.subheader("Response Time History")

    if not chart_df.empty:
        fig = px.line(
            chart_df,
            x="time",
            y="latency_ms",
            color="website",
            markers=True,
            labels={
                "time": "Check Time",
                "latency_ms": "Response Time (ms)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Check History")
    st.dataframe(df, use_container_width=True)

st.caption("Checks run from the machine hosting this application.")
