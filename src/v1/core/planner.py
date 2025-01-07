import openai
import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def make_plan(client, content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            # response_format={ "type": "json_object" },
            messages=[{"role": "system", "content": content}],
            ## add user message
            temperature=0.8,  # (0-1) Controls the randomness or creativity of the model's responses.A higher value (e.g., 0.8) introduces more randomness and creativity in the responses.
            max_tokens=1500,
            top_p=0.3,  # Controls the diversity of the output by sampling from the top p percentage of possible next tokens.A value of 0.2 means the model will sample from the top 20% of possible next tokens, leading to more focused and deterministic output.(0-1)
            frequency_penalty=0.5,  # (-2,+2)Reduces the likelihood of the model repeating the same phrases or tokens.
            presence_penalty=-0.5,  # (-2,+2) Encourages or discourages the model from mentioning new concepts that haven't been mentioned in the conversation so far.Negative values (e.g., -1.0) would encourage the model to introduce new ideas or topics in the conversation.
        )
        response = response.choices[0].message.content
        # st.balloons()
        return response
    except Exception as e:
        st.error(f"Error Occurred: {e}")
        return None


def create_image(client, selected_countries, activities):
    try:

        # Ensure selected_countries is a string if it's a list
        if isinstance(selected_countries, list):
            selected_countries = ", ".join(selected_countries)
        if isinstance(activities, list) and activities:
            activity = activities[0]  # Take the first activity from the list
        else:
            activity = activities  # If it's not a list, just use the value directly

        # Generate the image using the provided parameters
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic travel picture in {selected_countries} recalling {activity} activities",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Extract the image URL from the response
        image_url = image_response.data[0].url
        return image_url

    except Exception as e:
        # Handle any errors that occur during the image generation
        st.warning(f"Error creating image: {e}")
        return None


def display_image_from_url(image_response):
    if image_response:
        try:
            response = requests.get(image_response)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Generated Image")
        except Exception as e:
            st.error(f"Error displaying image: {e}")
