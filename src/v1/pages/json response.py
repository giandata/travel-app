import streamlit as st
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
import form
from openai import OpenAI

from src.v1.Planner import check_password

if not check_password():
    st.stop()

content, picture, loading = form.render_form()

if content != None:
    loading.empty()
    client = OpenAI(api_key=st.secrets["OPENAPI_API_KEY"])

    prompt = content

    json_example = {
        "itinerary_summary": "title",
        "   itinerary": [
            {
                "day": "Day 1: Arrival place",
                "description": {
                    "activities": ["activity 1", "activity 2"],
                    "accommodation": "accommodation example",
                    "transportation": "transportation example",
                },
            }
        ],
        "travel_summary": {
            "total_cost": "Approx cost €",
            "cost_breakdown": {"example_cost_item": "€100"},
            "additional_suggestions": ["suggestion 1", "suggestion 2"],
            "explanation": "eventual explanations",
        },
    }

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON. The data schema wil be like this"
                + json.dumps(json_example),
            },
            {"role": "user", "content": prompt},
        ],
    )
    # Extract the response content
    response_content = chat_completion.choices[0].message.content

    finish_reason = chat_completion.choices[0].finish_reason

    if finish_reason == "stop":
        # Attempt to parse the response as JSON
        try:
            response_json = json.loads(response_content)
            # Display the parsed JSON response
            st.subheader("Parsed Response")
            # full response
            # st.json(response_json)

            # example print of json chunk
            st.json(response_json["itinerary"])

        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON: {e}")
            st.write("Raw response content:", response_content)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error(f"Finish reason {finish_reason}")
