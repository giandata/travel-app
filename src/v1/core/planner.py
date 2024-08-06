import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def make_plan(client, content):
    response = client.chat.completions.create(
            model="gpt-4o-mini",
            #response_format={ "type": "json_object" },
            messages=[{"role": "system", "content": content}],
            temperature=0.5,
            max_tokens=1000,
            top_p=0.1,
            frequency_penalty=0.2,
            presence_penalty=0
        )
    response = response.choices[0].message.content
    return response

def create_image(client,travel_type,selected_countries):
        image_response = client.images.generate(
          model="dall-e-3",
          prompt=f"cinematic {travel_type} travel picture in {selected_countries}",
          size="1024x1024",
          quality="standard",
          n=1,
        )
        image_response = image_response.data[0].url
        return image_response
      
def display_image_from_url(image_response):
    if image_response:
        try:
            response = requests.get(image_response)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Generated Image')
        except Exception as e:
            st.error(f"Error displaying image: {e}")
    