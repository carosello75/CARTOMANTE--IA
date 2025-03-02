from flask import Flask, request, jsonify, render_template
from twilio.twiml.voice_response import VoiceResponse
import openai
import os
from google.cloud import texttospeech, speech_v1p1beta1 as speech
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OPENAI_API_KEY

# Carica le credenziali di Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice', methods=['POST'])
def voice():
    response = VoiceResponse()
    response.say("Benvenuto nella linea della cartomante AI. Dimmi la tua domanda dopo il bip.", voice='alice', language='it-IT')
    response.record(timeout=10, transcribe=False, action='/process-voice')
    return str(response)

@app.route('/process-voice', methods=['POST'])
def process_voice():
    recording_url = request.form['RecordingUrl']
    print(f"Audio ricevuto: {recording_url}")
    response = VoiceResponse()
    response.say("Grazie, sto consultando le carte. Ti risponderò a breve.", voice='alice', language='it-IT')
    return str(response)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
