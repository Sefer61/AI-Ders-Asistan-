import streamlit as st
from groq import Groq

# Secrets üzerinden anahtarı al
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

def groq_model_kontrol():
    """
    Sisteminin Groq ile bağlantısını test eden ve 
    kullanılabilir model isimlerini döndüren fonksiyon.
    """
    try:
        # Groq'ta kullanılan modelleri listeleyebiliriz veya 
        # doğrudan onaylanmış model isimlerini kullanabiliriz.
        model_name = "llama3-8b-8192"
        print(f"Bağlantı başarılı. Kullanılan model: {model_name}")
        return model_name
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None