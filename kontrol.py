api_key = st.secrets["GCP_API_KEY"]
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)