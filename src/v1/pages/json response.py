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

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides responses in JSON format.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    # Extract the response content
    response_content = chat_completion.choices[0].message.content

    # Attempt to parse the response as JSON
    try:
        response_json = json.loads(response_content)
        # Display the parsed JSON response
        st.subheader("Parsed Response")
        st.json(response_json)
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON: {e}")
        st.write("Raw response content:", response_content)

    except Exception as e:
        st.error(f"An error occurred: {e}")
