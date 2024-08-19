import streamlit as st
from PIL import Image
import os
import sys
import src
from pages import *


# The following line allows using absolute imports relative to "src"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

# sidebar
logo = "logo.png"
logo_pic = Image.open(logo)
st.sidebar.write("Welcome to the travel blog ")
st.sidebar.image(logo_pic)


st.subheader("Blink Travel Blog", anchor=False)
st.write("Explore the unique travel plans created by Blink Travel")

# Path to the directory containing the itinerary files
directory_path = r"src/v1/travels"

# Get a list of all .txt files in the directory
files = [f for f in os.listdir(directory_path) if f.endswith(".txt")]

if not files:
    st.warning("No itinerary files found in the directory.")
else:
    for file_name in files:
        itinerary_path = os.path.join(directory_path, file_name)
        image_path = os.path.join(directory_path, file_name.replace(".txt", ".jpg"))
        # Display itinerary summary
        try:
            with open(itinerary_path, "r", encoding="utf-8") as file:
                itinerary_content = file.read()
                title_and_summary, days, overall_summary, overall_summary_match = (
                    src.v1.core.response_processor.response_splitter(itinerary_content)
                )
                with st.expander(title_and_summary, expanded=True):

                    image = Image.open(image_path)

                    st.image(
                        image,
                        use_column_width=True,
                    )

                    src.v1.core.response_processor.show_response(
                        days, overall_summary_match, overall_summary
                    )
        except FileNotFoundError:
            st.error(f"File '{itinerary_path}' not found.")
        except UnicodeDecodeError:
            st.error(
                f"Error decoding file '{itinerary_path}'. Try using a different encoding."
            )
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


nav_planner = st.button(
    "Create Your personal travel plan",
    type="primary",
    use_container_width=True,
    key="nav_planner_blog",
)
if nav_planner:
    st.switch_page("Planner.py")
