import streamlit as st

# Split the response into sections
import re


def response_splitter(response):

    # Extract the title and itinerary summary
    title_and_summary_pattern = re.compile(r"^(.*?)(?=Day 1:)", re.DOTALL)
    title_and_summary_match = title_and_summary_pattern.search(response)
    if title_and_summary_match:
        title_and_summary = title_and_summary_match.group(1).strip()
    else:
        title_and_summary = "Title and Itinerary Summary not found."

    # Extract day details and costs
    day_pattern = re.compile(r"(Day \d+:.*?)(?=Day \d+:|Travel Summary|$)", re.DOTALL)
    days = day_pattern.findall(response)

    # Extract the overall summary
    overall_summary_pattern = re.compile(r"Travel Summary(.*)$", re.DOTALL)
    overall_summary_match = overall_summary_pattern.search(response)
    if overall_summary_match:
        overall_summary = overall_summary_match.group(0).strip()
    else:
        overall_summary = "Itinerary Summary not found."

    return title_and_summary, days, overall_summary, overall_summary_match


def show_response(days, overall_summary_match, overall_summary):
    tab_names = [day.split(":")[0] for day in days]
    if overall_summary_match:
        tab_names.append("Itinerary Summary")
        tabs = st.tabs(tab_names)
        # Loop through tabs and generate content
        for i, tab in enumerate(tabs[:-1]):
            with tab:
                st.markdown(days[i])
        with tabs[-1]:
            st.markdown(overall_summary)
