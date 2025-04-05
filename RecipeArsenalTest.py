import streamlit as st
import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key="AIzaSyAFPVwBrBCA4hlmtUrrGYS9POeLKHqQR6Q")

# Use the correct model based on what you found
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Streamlit App
st.title("Recipe Arsenal")
st.image("https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/1200px-Arsenal_FC.svg.png", caption="Up the Gunners!")

# User name input
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")

# Ingredients input
ingredients = st.text_input("Enter ingredients (comma-separated):", placeholder="e.g. chicken, rice, spinach")

# Button to generate recipe
if st.button("Generate Recipe"):
    if not ingredients:
        st.warning("Please enter some ingredients first.")
    else:
        st.write(f"Generating recipe using: {ingredients}")

        # Prompt for Gemini
        prompt = f"""You're a chef. Using only these ingredients: {ingredients}, 
        create a healthy, delicious recipe. Include a title, ingredients list with measurements, and step-by-step instructions."""

        try:
            response = model.generate_content(prompt)
            st.markdown("### Recipe")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error generating recipe: {e}")
