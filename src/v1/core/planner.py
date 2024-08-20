import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def make_plan(client, content):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # response_format={ "type": "json_object" },
        messages=[{"role": "system", "content": content}],
        temperature=0.5,
        max_tokens=1200,
        top_p=0.1,
        frequency_penalty=0.2,
        presence_penalty=0,
    )
    response = response.choices[0].message.content
    return response


def create_image(client, selected_countries, activities):
    try:

        # Ensure selected_countries is a string if it's a list
        if isinstance(selected_countries, list):
            selected_countries = ", ".join(selected_countries)
        if isinstance(activities, list):
            activities = ", ".join(activities)

        # Generate the image using the provided parameters
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic travel picture in {selected_countries} recalling {activities} activities",
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
