import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import os
import sys
import time

# The following line allows using absolute imports relative to "src"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

import src

# sidebar
logo = "logo1.png"
logo_pic = Image.open(logo)
st.sidebar.write("Welcome to the travel guide shop ")
st.sidebar.image(logo_pic)
st.sidebar.markdown(
    "<h3 style='font-size:28px; text-align:center;'>Follow us on Socials 📸 <a href='https://www.instagram.com/blinktravel_/'>here</a></h3>",
    unsafe_allow_html=True,
)

st.subheader("Blink Travel Shop", anchor=False)
st.subheader("The Practical Tourist guide collection")

book_description = """
🌍 **The Practical Tourist Guide colection** is the ultimate guide for travelers who value well-organized, actionable advice.

✨ Designed with convenience in mind, this guidebook provides all the essential tools you need to plan and enjoy your journey, stress-free.

🎒 Learn **practical tips on packing**, avoiding tourist traps, and staying safe while discovering Europe's cities, top attractions, and hidden gems.

💬 Handy **sections on language essentials** include useful phrases in the local language to help you connect with locals, while the guide’s clear breakdown of transportation options—from airport transfers to taxis—makes getting around a breeze.

🌦️ With insights into countries' weather, currency, festivals, and cultural nuances, these guidebooks go beyond the basics to offer a truly comprehensive travel companion.

📅 **Packed with carefully designed itineraries** for 1, 3, or 5 days, the book helps you make the most of your time, no matter the length of your stay.
"""
st.divider()


book_index = """
    *  **Our first Guide introduces you to Munich!**

    **Guides Index**
    - **Introduction**: Why visit Munich, A brief history of Munich, Culture and lifestyle  
    - **Planning Your Travel**: Best time to visit, Weather and climate, How long to stay, Packing tips  
    - **Getting Around**: From the airport to the city center, Munich public transport, Cycling in Munich, Munich by walk, Taxi and ride sharing  
    - **Attractions & Cultural Experiences**: Top landmarks and historical sites, Hidden gems, Local traditions and festivals, Music, theatre, and performing arts, Food and wine tasting tours, Guided historical walks  
    - **Day Trips and Excursions**: Nearby towns worth visiting, Nature and scenic spots, Guided tours and transportation tips  
    - **Practical Information**: Currency and payments, Language, Emergency numbers  
    - **Sample Itineraries**: 1-day exploration (includes digital itinerary on Google Maps), 3-day travel, 5-day itinerary  
    - **Final Tips**: Staying safe while exploring, How to avoid tourist traps, Making the most of your visit  
    - **Notes**
"""


def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)


st.write_stream(stream_text(book_description))

st.markdown(
    "<h2 style='font-size:32px; text-align:center;'>Order Guide <a href='https://www.amazon.com/dp/B0DSB6WCT6'>here</a></h1>",
    unsafe_allow_html=True,
)

cover_munic = "munich cover.png"
cover_munic_pic = Image.open(cover_munic)
st.image(cover_munic)

st.write(book_index)

col_1, col_2 = st.columns(2)
with col_1:
    st.page_link("Planner.py", label="Go to the Planner", icon="1️⃣")

with col_2:
    st.page_link("Pages/Blog.py", label="Go to the Blog", icon="2️⃣")

## add instagram page
