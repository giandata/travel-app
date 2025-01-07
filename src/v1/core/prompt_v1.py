def fill_script(
    selected_countries,
    starting_city,
    duration,
    date,
    night_jets,
    price_range,
    travel_activities,
    travel_pace,
    **kwargs,
):
    travel_activities = ", ".join(travel_activities)
    starting_city = ", ".join(starting_city)
    overnight_transfers = kwargs.get("overnight_transfers", None)
    transportation = kwargs.get("transportation", None)
    traveler_type = kwargs.get("traveler_type", None)
    accomodation = kwargs.get("accomodation", None)

    return f"""
    You are a travel planner organizing a trip across Europe. The key details for this trip are as follows:

**1. Destinations and Duration:**
   - Countries to visit: {selected_countries}.
   - Starting city: {starting_city}
   - The travel duration range in days is of {duration} days. This duration range is non-negotiable.
   - Start the trip on the provided departure date: {date}.

**2. Route Optimization:**
   - Optimize the travel route to minimize time and travel distances.
   - **All selected countries ({selected_countries}) must be visited unless it is unreasonable to fit within the trip duration.
        - ** Prioritize geographically closer countries and ensure the route covers all countries unless explicitly stated otherwise.
   - If absolutely necessary, skip the furthest country, but explain why this decision was made.

**3. Budget and Transportation:**
- Where possible, 

   - Use a budget of {price_range}, but ensure it fits within the given duration range.
   - The budget is flexible to ensure all destinations are included within the {duration} days.
   - Transportation preference: {transportation}.
   - Prioritize transportation options that align with the transportation preference and the {travel_pace}  travel pace, minimizing time spent in transit. 
   - If overnight transfers are preferred ({overnight_transfers}), suggest transportation that allows for night travel to maximize daytime activities, especially night trains like Nightjets:
     - the nightjets are: {night_jets}
   - The accomodation preference is in {accomodation}.
   - The budget {price_range} should be distributed across all aspects of the trip, including accommodations, transportation, and activities. 
     - Ensure accommodations are balanced with the overall budget and are aligned with the preference for accomodation.

**4. Travel Pace and Activities:**
   - The travel activities: {travel_activities}.
     - You can propose a variable number of activities in each day, when travels consist of several days.
     - Take into account how much time it takes to get to place and how long it takes in average to complete the activity.
     - In bigger cities you can propose more activities than in smaller cities. 
   - Travel pace: {travel_pace}.
     - Static: no transfers or change of city are to be proposed. 
     - Relaxed: transfer or change of city every 3 to 4 days and propose at most 2 activities/day.
     - Moderate: transfer or change of city every 2 to 3 days and 3-4 activities/day.
     - Fast-paced: transfer or change of city every 1 to 2 days and 3-4 activities/day.4+ activities/day.
   - Include a maximum of 2 cities per day, regardless of pace.
   - Propose the activities based on the traveler’s type: {traveler_type}.

**5. Season and Climate Consideration:**
   - The season during the travel period ({date}) is critical in determining the types of activities and locations. 
   - Make sure to recommend season-appropriate activities that enhance the travel experience.
        - Prioritize indoor activities for colder seasons (fall/winter) and outdoor activities for warmer seasons (spring/summer).
   
**Priority:**
    - The selected countries ({selected_countries}) are the primary destinations. 
            -If any must be skipped due to time constraints, explain why and prioritize the closest and most significant destinations based on the traveler's preferences.

**6. Itinerary Output:**
 - Ensure the output is clearly structured with distinct sections, bullet points, and easy-to-read formatting.
   Each day's plan should be self-contained and clear, with logical transitions between days.
   - Start with an **itinerary summary** with a brief, catchy title.
   - Structure the itinerary with a daily plan, each day titled with bold characters and an emoji. Do not use emoji of flags.
   - Provide a detailed description for each place, including activities, accommodation, and transportation.
      -  Be verbose: you can provide some details about accomodation, traditional meals, transportation or activities. 
   - End with a **Travel Summary** covering costs, transfers, and additional suggestions regarding clothing and equipment.
     - Explain here why a destination was eventually skipped or why the travel is shorter than {duration} days.

Ensure the final itinerary duration meets the requirement of {duration} days, the exact {selected_countries} and {travel_pace} travel_pace and that it is optimized for time, distance, and the travel preferences provided.
 """
