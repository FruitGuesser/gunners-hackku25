import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyAFPVwBrBCA4hlmtUrrGYS9POeLKHqQR6Q")

# List available models
try:
    models = genai.list_models()
    for model in models:
        print(model.name)
except Exception as e:
    print(f"Error: {e}")
