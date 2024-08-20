from langchain.chains import LLMChain
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
import json
import streamlit as st

prompt = """
    You are a travel planner organizing a trip across Europe. The key details for this trip are as follows:
**1. Destinations and Duration:**
   - Countries to visit: Austria, Czechia.
   - The trip must last exactly 6 days. This duration is non-negotiable, and all days must be fully utilized.
   - Start the trip on the provided departure date: 20/08/2024.
**2. Route Optimization:**
   - Optimize the travel route to minimize time and travel distances.
   - **All selected countries (Austria, Czechia) must be visited unless it is impossible to fit within the 6 days.
        - ** Prioritize geographically closer countries and ensure the route covers all countries unless explicitly stated otherwise.
   - If absolutely necessary, skip the furthest country, but explain why this decision was made.
**3. Budget and Transportation:**
    - Where possible, 
   - Use a budget of 500-1000 €, but ensure it fits within the given 6 days.
   - The budget is flexible to ensure all destinations are included within the 6 days.
   - Transportation preference: Train.
   - Prioritize transportation options that align with the transportation preference and the moderate  travel pace, minimizing time spent in transit. 
   - If overnight transfers are preferred (True), suggest transportation that allows for night travel to maximize daytime activities, especially night trains like Nightjets:
   
   - The accomodation preference is in Hotel.
   - The budget  500-1000 € should be distributed across all aspects of the trip, including accommodations, transportation, and activities. 
     - Ensure accommodations are balanced with the overall budget and are aligned with the preference for accomodation.
**4. Travel Pace and Activities:**
   - The travel activities: City sightseeing,relax and welness.
     - You can propose a variable number of activities in each day, when travels consist of several days.
     - Take into account how much time it takes to get to place and how long it takes in average to complete the activity.
     - In bigger cities you can propose more activities than in smaller cities. 
   - Travel pace: moderate. 
     - Relaxed: 2 activities/day.
     - Moderate: 3-4 activities/day.
     - Fast-paced: 4+ activities/day.
   - Include a maximum of 2 cities per day, regardless of pace.
   - Propose the activities based on the traveler’s type: Solo traveler.
**5. Season and Climate Consideration:**
   - The season during the travel period (20/08/2024) is critical in determining the types of activities and locations. 
   - Make sure to recommend season-appropriate activities that enhance the travel experience.
        - Prioritize indoor activities for colder seasons (fall/winter) and outdoor activities for warmer seasons (spring/summer).  
**Priority:**
   - The trip must last exactly 6 days. This is a non-negotiable requirement.
    - The selected countries (Austria, Czechia) are the primary destinations. 
            -If any must be skipped due to time constraints, explain why and prioritize the closest and most significant destinations based on the traveler's preferences.
**6. Itinerary Output:**
 - Ensure the output is clearly structured with distinct sections, bullet points, and easy-to-read formatting. Each day's plan should be self-contained and clear, with logical transitions between days.
   - Start with an **itinerary summary** with a brief, catchy title.
   - Structure the itinerary with a daily plan, each day titled with bold characters and an emoji. Do not use emoji of flags.
   - Provide a detailed description for each place, including activities, accommodation, and transportation.
      -  Be verbose: you can provide some details about accomodation, traditional meals, transportation or activities. 
   - End with a **Travel Summary** covering costs, transfers, and additional suggestions regarding clothing and equipment.
     - Explain here why a destination was eventually skipped or why the travel is shorter than 6 days.
Ensure the final itinerary meets the exact duration of 6 days, the exact Austria, Czechia and moderate and that it is optimized for time, distance, and the travel preferences provided.
"""




# from langchain_core.prompts.chat import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

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
