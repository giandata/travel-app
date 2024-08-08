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
