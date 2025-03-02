import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
import openai
import requests
from google.cloud import texttospeech, speech_v1p1beta1 as speech
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, OPENAI_API_KEY

print(">>> Cartomante AI sta partendo...")

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
    audio_file = 'question.wav'
    
    download_audio(recording_url, audio_file)
    question = transcribe_audio(audio_file)
    response_text = get_cartomante_response(question)

    generate_response_audio(response_text, 'response.mp3')

    response = VoiceResponse()
    response.play('/static/response.mp3')
    return str(response)

def download_audio(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def transcribe_audio(filepath):
    client = speech.SpeechClient()
    with open(filepath, 'rb') as f:
        content = f.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="it-IT"
    )

    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else "Non ho capito la domanda."

def get_cartomante_response(question):
    prompt = f"Sei una cartomante sensuale e intrigante. Una cliente ti chiede: '{question}'. Rispondi come una cartomante."
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message['content']

def generate_response_audio(text, output_file):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="it-IT", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(f'static/{output_file}', 'wb') as out:
        out.write(response.audio_content)

# Questa è la parte fondamentale per Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Legge la porta da Render, fallback a 10000 in locale
    app.run(host='0.0.0.0', port=port)
