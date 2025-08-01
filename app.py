# app.py

import streamlit as st
import joblib
import numpy as np

# Load model and vectorizer
model = joblib.load("spam_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Constants
SPAM_SIZE_MB = 0.5
SPAM_THRESHOLD_MB = 200

st.set_page_config(page_title="Spam Detector & Storage Alert", layout="wide")

st.title("📱 SMS Spam Detector and Storage Monitor")

st.markdown("""
This app classifies your SMS messages into **spam or ham**, calculates storage taken by spam messages, 
and alerts if it's more than 200 MB.
""")

# Text input box
messages_input = st.text_area("📩 Paste your SMS messages here (one per line)", height=200)

if st.button("🔍 Analyze"):
    if messages_input.strip() == "":
        st.warning("Please enter at least one message.")
    else:
        messages = messages_input.strip().split("\n")

        # Vectorize and predict
        vectors = vectorizer.transform(messages)
        preds = model.predict(vectors)

        # Count spam and storage
        is_spam = preds == 1
        spam_count = np.sum(is_spam)
        spam_storage = spam_count * SPAM_SIZE_MB

        # Show table
        st.subheader("📋 Classification Results")
        results = [{"Message": msg, "Label": "Spam" if pred else "Ham"} for msg, pred in zip(messages, preds)]
        st.dataframe(results, use_container_width=True)

        # Show stats
        st.metric("Spam Messages", spam_count)
        st.metric("Estimated Storage Used by Spam", f"{spam_storage:.1f} MB")

        # Alert if above threshold
        if spam_storage >= SPAM_THRESHOLD_MB:
            st.error("⚠️ ALERT: Spam messages are consuming over 200MB of storage!")
            st.button("🗑️ Suggest Deletion")
        else:
            st.success("✅ You're within the safe limit.")
