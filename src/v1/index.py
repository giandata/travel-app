import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI
import os
import sys
from lists import *
import json
import pandas as pd
import pydantic
import hmac

from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

# The following line allows using absolute imports relative to "src"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here

def run():
    
    st.title("Travel Planner Ai ✈️")
    st.header("Tell the genius about your dream travel, he will plan it for you!")
    
    with st.container(border=True):
        
        st.subheader("Where do you want to travel?")
        col1,col2,col3 = st.columns([1,1,3])

        with col1:
            selected_country = st.selectbox(
                label="Departing country",
                options=country_start,
                index=None,
                key="departure country",
                help="Select the country of departure",
                placeholder="From where you want to start your travel?",
                disabled=False,
                label_visibility="visible")

        selected_cities = european_cities.get(selected_country, [])

        with col2:
            departure = st.selectbox(
                label="Departure City",
                options=selected_cities,
                index=None,
                key="departure",
                help="Select city of departure",
                placeholder="Choose a Departure",
                disabled=False,
                label_visibility="visible",
            )

        with col3:
            selected_countries = st.multiselect(
                label= 'Countries to visit',
                options=countries,
                default=selected_country,
                key='steps',
                help='Select up to 5 countries to visit',
                max_selections=5,
                placeholder="Choose at least 1 country",
                label_visibility="visible")

        st.subheader("When do you want to leave?")
        col1,col2 = st.columns(2)
        with col1:
            now = datetime.now()
            date = st.date_input(
                label="Date of departure",
                value=now,
                min_value=now,
                max_value=now + timedelta(days=365),
                key="date",
                help="Select date of departure",
                format="YYYY/MM/DD",
                label_visibility="visible",
            )

        with col2:
            duration = st.slider(
            label="How many days you want to travel?",
            min_value=1, max_value=7,
            step=1,
            key="duration",
            help="Select how many days you want to travel",
            label_visibility="visible")

        st.subheader("What spots do you like to visit?")

        col1,col2 =st.columns(2)
        with col1:
            travel_type = st.radio(
                label= "Types of visits",
                options=travel_options,
                index=None,
                key="travel_type",
                help="Select which kind of points of interest to include in the plan",
                label_visibility="visible")
        with col2:
            with st.expander("Advanced settings"):
                price_range =[]
                price_range = st.select_slider(
                    label="Can you provide an indicative price range? (€)",
                    options=price_ranges,
                    help="Specify the travel budget to organize a travel that best suits you"
                )

        disabled = selected_countries is None or departure is None or travel_type is None 

    content = f"You are a travel planner. I provide you with a departure country from {selected_country}, single or up to 5 destination countries from {selected_countries} and the starting date {date}. Suggest a plan of the duration of {duration} days. Find places to visit and best transporations options. The places you are including must be in line with the provided {travel_type}.The ovarall cost of the travel should respect the range provided from {price_range} if it is provided. Start the travel plan with a phrase of success in finding a plan and print a in bold characters a brief title that describes the travel. For each visit you find give a very short description of it. provide an estimate cost for every day of travel. Every day should appear as a subtitle.No more than 2 cities can be touched in a single day, and account for the travel distance in your recommendations. Structure the response in bullet points."

    pressed = st.button(label="Submit", key="Submit", disabled=disabled)
    if pressed:
      loading = st.info( f"The genius is looking for a **{travel_type}** travel starting in **{departure}**,**{selected_country}**, for the duration of **{duration}** days visiting these countries: **{selected_countries   }**... Wait for the travel plan 🚀🚀", icon="ℹ️")
      client = OpenAI(api_key=st.secrets["OPENAPI_API_KEY"])
      response = client.chat.completions.create(
        model="gpt-4o-mini",
        #response_format={ "type": "json_object" },
        messages=[{"role": "system", "content": content}],
        temperature=0.5,
        max_tokens=700,
        top_p=0.1,
        frequency_penalty=0.2,
        presence_penalty=0
      )
      
      travel = response.choices[0].message.content

      loading.empty()
      st.balloons()
      st.success('Travel planned!',icon="✈️")

      loading.empty()
      st.balloons()
      st.success('Travel planned!',icon="✈️")

      with st.container(border=True):
          st.markdown(response.choices[0].message.content)

      st.download_button(data=travel,label="Download itinerary")

      prompt = ChatPromptTemplate.from_template(travel)
      
      prompt_content = prompt[0]
      prompt_template = prompt_content.prompt.template

      extractionFunctionSchema = {
        "name" :   "extractor",
        "description": "Extracts fields from the input.",
        "parameters": {
          "type": "object",
          "properties": {
            "title":{
              "type":"string",
              "description": "The title of the travel"
            },
            "destinations": {
              "type": "array",
              "items": {"type": "string"},
              "description": "The selected city and country destination of the travel",
            },
            "days": {
              "type": "number",
              "description": "The number of days in the input",
            },
            "activities": {
              "type": "array",
              "items": {"type": "string"},
              "description": "The activities included in the travel",
            },
            "coordinates": {
              "type": "array",
              "items": {"type": "string"},
              "description": "The coordinates of the destiantions included in the travel",
            },
            "cost": {
              "type": "array",
              "items": {"type": "string"},
              "description": "The cost for each day of the travel",
            },
            # "chat_response": {
            #   "type": "string",
            #   "description": "the response travel to the human's input",
            # },
          },
          "required": ["title","destinations", "days","activities","coordinates","cost"],
        },
      }

      model = ChatOpenAI(api_key=st.secrets["OPENAPI_API_KEY"])
      chain = model.bind( functions=[extractionFunctionSchema],
      function_call= {"name": "extractor"})
      
      # chain = prompt | model | JsonOutputFunctionsParser()

      function_response = chain.invoke(prompt_template)

      # Assuming 'function_response' contains the output
      # Assuming 'function_response' contains the output
      response_dict = {
      "content": function_response.content,
      "additional_kwargs": {
          "function_call": {
              "name": function_response.additional_kwargs['function_call']['name']
          }
      },
      # TODO for some reason, response_metadata breaks the code. Maybe the response schema has changed.
      # "response_metadata": {
          # "token_usage": {
          #     "completion_tokens": function_response.response_metadata['token_usage']['completion_tokens'],
          #     "prompt_tokens": function_response.response_metadata['token_usage']['prompt_tokens'],
          #     "total_tokens": function_response.response_metadata['token_usage']['total_tokens']
          # },
          # "model_name": function_response.response_metadata['model_name'],
          # "system_fingerprint": function_response.response_metadata['system_fingerprint'],
          # "finish_reason": function_response.response_metadata['finish_reason'],
          # "logprobs": function_response.response_metadata['logprobs']
      # }
      }

      # Add another level for the arguments
      arguments = function_response.additional_kwargs['function_call']['arguments']

      arguments = json.loads(arguments)

      title = arguments.get("title", "")
      destinations = arguments.get("destinations", [])
      days = arguments.get("days", 0)
      activities = arguments.get("activities", [])
      coordinates = arguments.get("coordinates", [])
      cost = arguments.get("cost", [])

      # Update the "arguments" key with extracted values
      response_dict["additional_kwargs"]["function_call"]["arguments"] = {
          "title": title,
          "destinations": destinations,
          "days": days,
          "activities": activities,
          "coordinates": coordinates,
          "cost": cost
      }

      # Convert dictionary to JSON
      json_response = json.dumps(response_dict, indent=4)
      st.json(json_response)

      import pandas as pd

      # Extract coordinates from the response dictionary
      coordinates = response_dict["additional_kwargs"]["function_call"]["arguments"]["coordinates"]

      # Split each coordinate string into latitude and longitude
      coordinates_split = [coord.split(",") for coord in coordinates]

      # Extract latitude and longitude from each split coordinate
      latitude = [float(coord[0].split("°")[0]) for coord in coordinates_split]
      longitude = [float(coord[1].split("°")[0]) for coord in coordinates_split]

      # Create a DataFrame from latitude and longitude
      df_coordinates = pd.DataFrame({"latitude": latitude, "longitude": longitude})

      # # Print the DataFrame
      st.table(df_coordinates)

      st.map(df_coordinates[['latitude', 'longitude']])

      # import pydeck as pdk
      # # Create a line layer connecting the destinations
      # line_layer = pdk.Layer(
      #     "LineLayer",
      #     data=df_coordinates,
      #     get_source_position=["longitude", "latitude"],
      #     get_target_position=["longitude", "latitude"],
      #     get_color=[255, 0, 0],    # Red color for the line
      #     width_min_pixels=6,
      # )


      # # Create a scatterplot layer for the destination points
      # scatterplot_layer = pdk.Layer(
      #     "ScatterplotLayer",
      #     data=df_coordinates,
      #     get_position=["longitude", "latitude"],
      #     get_radius=12000,  # Increase the radius of the points
      #     get_fill_color=[0, 0, 255],  # Green color for the points
      # )

      # # Set the initial view state
      # view_state = pdk.ViewState(
      #     longitude=df_coordinates["longitude"].mean(),
      #     latitude=df_coordinates["latitude"].mean(),
      #     zoom=5,
      #     bearing=0,
      #     pitch=0,
      # )

      # # Create a Deck object with the layers and view state
      # deck = pdk.Deck(
      #     layers=[line_layer, scatterplot_layer],
      #     initial_view_state=view_state,
      #     map_style="mapbox://styles/mapbox/light-v9",
      # )

      # # Render the map using st.pydeck_chart()
      # st.pydeck_chart(deck)
        
if __name__ == "__main__":
    run()
