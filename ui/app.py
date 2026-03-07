import streamlit as st
import requests

st.title("Autonomous Research Agent")

query = st.text_input("Enter a research question")

if st.button("Run Research"):

    with st.spinner("Running research pipeline..."):

        response = requests.post(
            "http://localhost:8000/research-plan",
            json={"query": query}
        )

        result = response.json()

    st.subheader("Final Report")

    report = result.get("final_report")

    if report:
        st.markdown(report)
    else:
        st.error("No report generated")

    st.subheader("Metrics")

    st.json({
        "execution_time": result.get("execution_time_seconds"),
        "grounding": result.get("grounding_check")
    })