import streamlit as st

# Title of the app
st.title("Recipe Arsenal")

#Arsenal crest
st.image("https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/1200px-Arsenal_FC.svg.png", caption="Up the Gunners!")

# Some text
st.write("I love gooning!!")

# A text input field
name = st.text_input("What's your name?")

# Show a greeting when the user submits their name
if name:
    st.write(f"Hello, {name}!")
