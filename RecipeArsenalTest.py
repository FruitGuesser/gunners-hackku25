import streamlit as st
import google.generativeai as genai
import requests
import os

# Configure Gemini with your API key
genai.configure(api_key="AIzaSyAFPVwBrBCA4hlmtUrrGYS9POeLKHqQR6Q")  # Replace with your actual Google Gemini API key

# Use the correct model (replace with your actual model name)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Spoonacular API key (replace with your actual Spoonacular API key)
api_key = "59042e23954344b39edfa1b0d271b77a"  # Replace with your actual Spoonacular API key

# Function to fetch recipes from Spoonacular based on ingredients
def fetch_recipes_from_spoonacular(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": api_key,
        "ingredients": ingredients,  # Comma-separated list of ingredients
        "number": 5  # You can adjust the number of recipes to fetch
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        recipes = response.json()
        return recipes
    else:
        st.error(f"Error fetching recipes: {response.status_code} - {response.text}")
        return []

# Function to fetch detailed recipe information (including instructions)
def fetch_recipe_details(recipe_id):
    info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    info_params = {
        "apiKey": api_key
    }

    info_response = requests.get(info_url, params=info_params)
    if info_response.status_code == 200:
        info_data = info_response.json()
        ready_in_minutes = info_data['readyInMinutes']
        servings = info_data['servings']
        source_url = info_data['sourceUrl']
        return ready_in_minutes, servings, source_url
    else:
        return None, None, None

def fetch_instructions(recipe_id):
    instructions_url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    instructions_params = {
        "apiKey": api_key
    }

    instructions_response = requests.get(instructions_url, params=instructions_params)
    if instructions_response.status_code == 200:
        instructions_data = instructions_response.json()
        if instructions_data:
            steps = instructions_data[0]['steps']
            return steps
    return None

# Streamlit App
st.title("Recipe Arsenal")

# Display three images side by side using columns
col1, col2, col3 = st.columns(3)

with col2:
    st.image("https://i.imgur.com/J1Lbcq4.png", caption="Up the Gunners!")

with col1:
    st.image("https://i.imgur.com/qbTCA4D.png", caption="Chef Havertz")

with col3:
    st.image("https://i.imgur.com/Em196xX.png", caption="Chef White")

# User name input
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")

# Ingredients input
ingredients = st.text_input("Enter ingredients (comma-separated):", placeholder="e.g. chicken, rice, spinach")

# User preference input for the recipe (e.g., healthy, high-protein, etc.)
recipe_preference = st.text_input("Any recipe preferences? (e.g., healthy, high-protein, etc.)", placeholder="e.g., healthy")

# Button to generate recipe
if st.button("Generate Recipe"):
    if not ingredients:
        st.warning("Please enter some ingredients first.")
    else:
        st.write(f"Searching for recipes using: {ingredients}")

        # Fetch recipes from Spoonacular
        recipes = fetch_recipes_from_spoonacular(ingredients)

        if recipes:
            # Display the recipe titles from Spoonacular with dropdowns for details
            st.write("### Found Recipes:")
            for i, recipe in enumerate(recipes):
                recipe_title = recipe['title']
                recipe_id = recipe['id']

                with st.expander(f"{recipe_title} (ID: {recipe_id})"):
                    # Display detailed information for each recipe
                    ready_in_minutes, servings, source_url = fetch_recipe_details(recipe_id)
                    if ready_in_minutes:
                        st.write(f"**Ready in**: {ready_in_minutes} minutes")
                        st.write(f"**Servings**: {servings}")
                        st.write(f"[**Source**]({source_url})")
                    
                    steps = fetch_instructions(recipe_id)
                    if steps:
                        st.write("### Instructions:")
                        for step in steps:
                            st.write(f"{step['number']}. {step['step']}")
                    else:
                        st.write("No instructions available.")
                    
            # Prompt to refine recipe selection with Gemini based on user preference
            if recipe_preference:
                st.write(f"Refining recipe choice based on preference: '{recipe_preference}'")

                # Generate a prompt for Gemini to refine the recipe selection
                prompt = f"""Given the list of recipes: {', '.join([recipe['title'] for recipe in recipes])},
                             select the best recipe that meets the following criteria: {recipe_preference}.
                             Provide the title of the best recipe and explain why it fits the preference."""

                # Use Gemini to filter and refine recipes
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### Refined Recipe Recommendation:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error generating refined recipe: {e}")
        else:
            st.write("No recipes found for the provided ingredients.")
