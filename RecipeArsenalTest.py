import streamlit as st
import google.generativeai as genai
import requests

# ✅ Set page config
st.set_page_config(page_title="🍴 Recipe Arsenal", page_icon="🍴", layout="centered")

# ✅ Custom Styles
st.markdown("""
    <style>
        /* Hide default Streamlit UI */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Apply deep red background color for everything */
        body, .main, .block-container {
            background-color: #660000 !important; /* Deep red for the outer background */
        }

        /* Inner content (keeping the same background color for the content area) */
        .block-container {
            background-color: #2C2C2C !important; /* Grayish-black for the content area */
            border-radius: 10px;
            padding: 20px;
        }

        /* Persistent Top Bar */
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 50px;
            background-color: #9A1111;
            color: white;
            display: flex;
            align-items: center;
            padding-left: 20px;
            z-index: 1000;
            font-size: 20px;
            font-weight: bold;
            border-bottom: 1px solid #444;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            text-shadow: -1px 0 #000, 0 1px #000, 1px 0 #000, 0 -1px #000;
        }

        .spacer {
            margin-top: 60px;
        }
    </style>

    <div class="top-bar">🍴 Recipe Arsenal</div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)

# ✅ Configure Gemini
genai.configure(api_key="AIzaSyAFPVwBrBCA4hlmtUrrGYS9POeLKHqQR6Q")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# ✅ Spoonacular API Key
api_key = "59042e23954344b39edfa1b0d271b77a"

# ✅ Functions
def fetch_recipes_from_spoonacular(ingredients):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {"apiKey": api_key, "ingredients": ingredients, "number": 5}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

def fetch_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    response = requests.get(url, params={"apiKey": api_key})
    if response.status_code == 200:
        data = response.json()
        ready_in_minutes = data.get('readyInMinutes')
        if not ready_in_minutes:
            ready_in_minutes = "N/A"  # Fallback if the field is missing
        servings = data.get('servings', "N/A")
        source_url = data.get('sourceUrl', "#")
        return ready_in_minutes, servings, source_url
    return "N/A", "N/A", "#"

def fetch_instructions(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    response = requests.get(url, params={"apiKey": api_key})
    if response.status_code == 200 and response.json():
        return response.json()[0]['steps']
    return None

# ✅ Top images
col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://i.imgur.com/J1Lbcq4.png")
with col1:
    st.image("https://i.imgur.com/qbTCA4D.png", caption="Chef Havertz")
with col3:
    st.image("https://i.imgur.com/Em196xX.png", caption="Chef White")

# ✅ User inputs
ingredients = st.text_input("Enter ingredients (comma-separated):", placeholder="e.g. chicken, rice, spinach")
recipe_preference = st.text_input("Any recipe preferences? (e.g., healthy, high-protein, etc.)", placeholder="e.g., healthy")

# ✅ Generate Recipe
if st.button("Generate Recipe"):
    if not ingredients:
        st.warning("Please enter some ingredients first.")
    else:
        st.write(f"Searching for recipes using: {ingredients}")
        recipes = fetch_recipes_from_spoonacular(ingredients)

        if recipes:
            st.write("### Found Recipes:")
            for recipe in recipes:
                title = recipe['title']
                recipe_id = recipe['id']

                with st.expander(f"{title} (ID: {recipe_id})"):
                    ready_in_minutes, servings, source_url = fetch_recipe_details(recipe_id)
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

            if recipe_preference:
                st.write(f"Refining recipe choice based on preference: '{recipe_preference}'")
                try:
                    titles = ', '.join([recipe['title'] for recipe in recipes])
                    prompt = f"""Given the list of recipes: {titles},
                                 select the best recipe that meets the following criteria: {recipe_preference}.
                                 Provide the title of the best recipe and explain why it fits the preference."""
                    response = model.generate_content(prompt)
                    st.markdown("### Refined Recipe Recommendation:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error generating refined recipe: {e}")
        else:
            st.write("No recipes found for the provided ingredients.")
