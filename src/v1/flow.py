import streamlit as st
from datetime import datetime, timedelta
import os
import sys
from lists import *
import hmac
from openai import OpenAI

#from langchain_core.prompts.chat import ChatPromptTemplate
#from langchain_openai import ChatOpenAI
#from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

# The following line allows using absolute imports relative to "src"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Absolutely importing src requires the workspace root to be set (see project_root)
import src

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
    st.cache_data.clear()
    st.title("Travel Planner Ai ✈️")
    st.header("Tell the Engine about your dream travel, he will plan it for you!")

    #"session state:" ,st.session_state

    with st.container(border=True):
        
        st.subheader("Where do you want to travel?")
        col1,col2 = st.columns([2,2])

        with col1:
            selected_country = st.selectbox(
                label="Departing country",
                options=country_start,
                index=None,
                key="departure_country",
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
                key="departure_city",
                help="Select city of departure",
                placeholder="Choose a Departure",
                disabled=False,
                label_visibility="visible",
            )

        st.divider() 

        selected_countries = st.multiselect(
                label= 'Countries to visit',
                options=countries,
                key='steps',
                help='Select up to 5 countries to visit',
                max_selections=5,
                placeholder="Choose at least 1 country",
                label_visibility="visible")
        
        st.markdown("You selected %s" % ", ".join(selected_countries))


        st.divider()

        st.subheader("When do you want to travel?")
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
            min_value=1, max_value=10,
            step=1,
            key="duration",
            help="Select how many days you want to travel",
            label_visibility="visible")

        st.divider()

        st.subheader("What type of activities you want in your travel plan?")

        col1,col2 =st.columns(2)
        with col1:
            st.write('Select the activities to be searched:')
            from src.v1 import widget
            travel_type = widget.travel_type.render_toggle()
         
        with col2:
            with st.expander("Advanced settings"):
                price_range =[]
                price_range = st.select_slider(
                    label="Can you provide an indicative price range? (€)",
                    options=price_ranges,
                    help="Specify the travel budget to organize a travel that best suits you"
                )

                picture = st.checkbox(
                  label='Generate AI picture',
                  value=False,
                  key='picbox'
                )

        disabled = selected_country is None or selected_countries is None or departure is None or travel_type is None 

        if disabled == False:
            from src.v1.core.prompt_v1 import fill_script
            content = fill_script(selected_country,departure,selected_countries,duration,date,night_jets,price_range,travel_type)

    pressed = st.button(label="Submit", key="submit_form", disabled=disabled)
    if pressed:
    # TRAVEL CREATION    
      loading = st.info( f"The Engine is preparing a travel plan travel starting in **{departure}**,**{selected_country}**, for the duration of **{duration}** days visiting these countr{'y' if len(selected_countries) == 1 else 'ies'}: **{" ".join(selected_countries)}**... Wait for the travel plan 🚀🚀", icon="ℹ️")
      
      client = OpenAI(api_key=st.secrets["OPENAPI_API_KEY"])

      response = src.v1.core.planner.make_plan(client, content)
      
      image_response = None
      if picture:
          image_response =  src.v1.core.planner.create_image(client,travel_type,selected_countries)

      loading.empty()
      st.balloons()
      st.success('Travel planned!',icon="✈️") 

      title_and_summary,days,overall_summary,overall_summary_match = src.v1.core.response_processor.response_splitter(response)

      # Display itinerary summary
      st.markdown(title_and_summary)
      
      if image_response is not None:
           src.v1.core.planner.display_image_from_url(image_response)

      # Display each day’s details in a single expander
      tab_names = [day.split(':')[0] for day in days]
      if overall_summary_match:
        tab_names.append("Itinerary Summary")
      tabs = st.tabs(tab_names)
      # Loop through tabs and generate content
      for i, tab in enumerate(tabs[:-1]):
        with tab:
           st.markdown(days[i])
      with tabs[-1]:
          st.markdown(overall_summary)

      src.v1.widget.rating.render()

      
      #for day in days:
        #st.expander(day.split('\n')[0], expanded=False).markdown(day)

      # Display Overall Trip Summary
      #st.expander("Overall Trip Summary").markdown(overall_summary)

      st.download_button(data=response,label="Download itinerary")

      #full response
      #st.markdown(response)  
      
      #st.cache_data.clear()   


      ##second part of app
      # prompt = ChatPromptTemplate.from_template(travel)
      
      # prompt_content = prompt[0]
      # prompt_template = prompt_content.prompt.template

      # extractionFunctionSchema = {
      #   "name" :   "extractor",
      #   "description": "Extracts fields from the input.",
      #   "parameters": {
      #     "type": "object",
      #     "properties": {
      #       "title":{
      #         "type":"string",
      #         "description": "The title of the travel"
      #       },
      #       "destinations": {
      #         "type": "array",
      #         "items": {"type": "string"},
      #         "description": "The selected city and country destination of the travel",
      #       },
      #       "days": {
      #         "type": "number",
      #         "description": "The number of days in the input",
      #       },
      #       "activities": {
      #         "type": "array",
      #         "items": {"type": "string"},
      #         "description": "The activities included in the travel",
      #       },
      #       "coordinates": {
      #         "type": "array",
      #         "items": {"type": "string"},
      #         "description": "The coordinates of the destiantions included in the travel",
      #       },
      #       "cost": {
      #         "type": "array",
      #         "items": {"type": "string"},
      #         "description": "The cost for each day of the travel",
      #       },
      #       # "chat_response": {
      #       #   "type": "string",
      #       #   "description": "the response travel to the human's input",
      #       # },
      #     },
      #     "required": ["title","destinations", "days","activities","coordinates","cost"],
      #   },
      # }

      # model = ChatOpenAI(api_key=st.secrets["OPENAPI_API_KEY"])
      # chain = model.bind( functions=[extractionFunctionSchema],
      # function_call= {"name": "extractor"})
      
      # # chain = prompt | model | JsonOutputFunctionsParser()

      # function_response = chain.invoke(prompt_template)

      # # Assuming 'function_response' contains the output
      # # Assuming 'function_response' contains the output
      # response_dict = {
      # "content": function_response.content,
      # "additional_kwargs": {
      #     "function_call": {
      #         "name": function_response.additional_kwargs['function_call']['name']
      #     }
      # },
      # # TODO for some reason, response_metadata breaks the code. Maybe the response schema has changed.
      # # "response_metadata": {
      #     # "token_usage": {
      #     #     "completion_tokens": function_response.response_metadata['token_usage']['completion_tokens'],
      #     #     "prompt_tokens": function_response.response_metadata['token_usage']['prompt_tokens'],
      #     #     "total_tokens": function_response.response_metadata['token_usage']['total_tokens']
      #     # },
      #     # "model_name": function_response.response_metadata['model_name'],
      #     # "system_fingerprint": function_response.response_metadata['system_fingerprint'],
      #     # "finish_reason": function_response.response_metadata['finish_reason'],
      #     # "logprobs": function_response.response_metadata['logprobs']
      # # }
      # }

      # # Add another level for the arguments
      # arguments = function_response.additional_kwargs['function_call']['arguments']

      # arguments = json.loads(arguments)

      # title = arguments.get("title", "")
      # destinations = arguments.get("destinations", [])
      # days = arguments.get("days", 0)
      # activities = arguments.get("activities", [])
      # coordinates = arguments.get("coordinates", [])
      # cost = arguments.get("cost", [])

      # # Update the "arguments" key with extracted values
      # response_dict["additional_kwargs"]["function_call"]["arguments"] = {
      #     "title": title,
      #     "destinations": destinations,
      #     "days": days,
      #     "activities": activities,
      #     "coordinates": coordinates,
      #     "cost": cost
      # }

      # # Convert dictionary to JSON
      # json_response = json.dumps(response_dict, indent=4)
      # st.json(json_response)

      # import pandas as pd

      # # Extract coordinates from the response dictionary
      # coordinates = response_dict["additional_kwargs"]["function_call"]["arguments"]["coordinates"]

      # # Split each coordinate string into latitude and longitude
      # coordinates_split = [coord.split(",") for coord in coordinates]

      # # Extract latitude and longitude from each split coordinate
      # latitude = [float(coord[0].split("°")[0]) for coord in coordinates_split]
      # longitude = [float(coord[1].split("°")[0]) for coord in coordinates_split]

      # # Create a DataFrame from latitude and longitude
      # df_coordinates = pd.DataFrame({"latitude": latitude, "longitude": longitude})

      # # # Print the DataFrame
      # st.table(df_coordinates)

      # st.map(df_coordinates[['latitude', 'longitude']])

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
