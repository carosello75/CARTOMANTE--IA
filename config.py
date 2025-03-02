import os

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "inserisci_il_tuo_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "inserisci_il_tuo_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "inserisci_il_tuo_numero_twilio")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "inserisci_la_tua_api_key_openai")
