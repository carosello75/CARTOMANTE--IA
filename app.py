from flask import Flask, request, jsonify, render_template
from twilio.twiml.voice_response import VoiceResponse
import openai
import os
import json
from google.cloud import texttospeech, speech_v1p1beta1 as speech

# Configurazioni (prende da env invece che da config.py diretto)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configura OpenAI
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return "Cartomante AI è attiva!"

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
