import streamlit as st
import pdfplumber
import time
from groq import Groq
from gtts import gTTS

# --- 1. AYAR (GROQ BAĞLANTISI) ---
# Secrets üzerinden anahtarı alıyoruz
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- AYARLAR & SESSION STATE ---
if 'ozet' not in st.session_state: st.session_state.ozet = None
if 'quiz' not in st.session_state: st.session_state.quiz = None
if 'anahtar_kelimeler' not in st.session_state: st.session_state.anahtar_kelimeler = None
if 'tam_metin' not in st.session_state: st.session_state.tam_metin = None

def ai_islemini_yurut(model_gorevi, metin):
    try:
        # Groq API ile Llama3 modelini kullanıyoruz
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Sen profesyonel bir akademik asistansın."},
                {"role": "user", "content": f"{model_gorevi}: {metin[:10000]}"}
            ],
            model="llama-3.3-70b-versatile", 
        )
        return chat_completion.choices[0].message.content, None
    except Exception as e:
        return None, f"Hata: {str(e)}"

st.set_page_config(page_title="AI Ders Asistanı", layout="wide", page_icon="📚")
st.sidebar.title("🛠️ Navigasyon")
secim = st.sidebar.radio("Sayfalar:", ["Ana Sayfa", "AI Asistan Modülü"])

# --- ANA SAYFA ---
if secim == "Ana Sayfa":
    st.title("🚀 AI Ders Asistanı Projesi")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Model", "Llama 3 (Groq)")
    col2.metric("Dil", "Türkçe")
    col3.metric("Durum", "Aktif/Hızlı")
    st.info("Hoş geldiniz ")
    
    st.subheader("🛠️ Uygulama Özellikleri")
    features = {
        "📄 PDF İşleme": "pdfplumber ile hızlı metin çıkarımı.",
        "🤖 Yapay Zeka": "Groq/Llama 3 ile ultra hızlı analiz.",
        "🔊 Seslendirme": "gTTS ile metinleri sese dönüştürme.",
        "⚡ Hata Yönetimi": "Sistem korumalı (Exception Handling) yapı."
    }
    for f, d in features.items(): st.write(f"**{f}**: {d}")

# --- AI ASİSTAN MODÜLÜ ---
elif secim == "AI Asistan Modülü":
    st.header("🤖 PDF Analiz Paneli")
    uploaded_file = st.file_uploader("Bir PDF dosyası yükleyiniz", type="pdf")
    
    if uploaded_file:
        if st.session_state.tam_metin is None:
            with st.spinner("PDF işleniyor..."):
                with pdfplumber.open(uploaded_file) as pdf:
                    st.session_state.tam_metin = "".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Özet ve Anahtar Kelime Analizi"):
                with st.spinner("Analiz ediliyor..."):
                    ozet, h1 = ai_islemini_yurut("Bu ders notunu 5 madde halinde özetle", st.session_state.tam_metin)
                    anahtar, h2 = ai_islemini_yurut("En önemli 5 anahtar kelimeyi virgülle listele", st.session_state.tam_metin)
                    if h1 or h2: st.error("API Hatası: " + (h1 or h2))
                    else: st.session_state.ozet, st.session_state.anahtar_kelimeler = ozet, anahtar
            
            if st.session_state.ozet:
                st.write("### 📝 Özet:", st.session_state.ozet)
                st.write("### 🔑 Anahtar Kelimeler:", st.info(st.session_state.anahtar_kelimeler))
                if st.button("🔊 Özeti Seslendir"):
                    tts = gTTS(text=st.session_state.ozet, lang='tr')
                    tts.save("ozet.mp3")
                    st.audio("ozet.mp3", format="audio/mp3")

        with col2:
            if st.button("Quiz Hazırla"):
                with st.spinner("Quiz hazırlanıyor..."):
                    quiz, hata = ai_islemini_yurut("Bu metinden 5 adet çoktan seçmeli soru hazırla", st.session_state.tam_metin)
                    if hata: st.error(hata)
                    else: st.session_state.quiz = quiz
            if st.session_state.quiz:
                st.write("### 🧠 Quiz:", st.session_state.quiz)