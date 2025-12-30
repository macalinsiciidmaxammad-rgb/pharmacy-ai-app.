import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import pandas as pd

# 1. Isku xidhka Gemini AI (Ka soo akhriso Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Khalad: API Key-ga Gemini lama helin!")

# 2. Isku xidhka Google Sheets
def connect_to_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    # HUBI: Magaca halkan ku qoran waa inuu la mid noqdo magaca Google Sheets-kaaga
    sheet = client.open("Pharmacy_Smart_DB").sheet1
    return sheet

st.set_page_config(page_title="AI Pharmacy Manager", layout="wide")
st.title("🏥 Pharmacy AI Smart Inventory")

try:
    sheet = connect_to_sheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    st.success("✅ Xogta bakhaarka waa lagu xidhay!")

    # Liiska Bakhaarka
    st.subheader("📦 Liiska Daawooyinka")
    st.dataframe(df, use_container_width=True)

    # Qaybta AI-da
    st.divider()
    st.subheader("🤖 Weydii AI-da (Gemini)")
    query = st.text_input("Maxaad rabtaa inaan kaaga falanqeeyo bakhaarka? (tusaale: Maxaa gabaabsi ah?)")
    
    if query:
        with st.spinner("AI-du way fekeraysaa..."):
            context = f"Xogta bakhaarku waa: {df.to_string()}"
            prompt = f"{context}\n\nUser Question: {query}\n(Fadlan ugu jawaab Af-Soomaali)"
            response = model.generate_content(prompt)
            st.info(response.text)

except Exception as e:
    st.error(f"Khalad ayaa dhacday: {e}")
