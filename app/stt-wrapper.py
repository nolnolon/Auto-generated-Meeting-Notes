from openai import OpenAI
import os
from io import BufferedReader

# retrieve OPENAI_API_KEY from env
client = OpenAI()
model_name = "gpt-4o-transcribe"

def audio_transcription(audio_file: BufferedReader, language: str | None = None, model_name) -> str: 
   """ 
   audio_file: binary mode object 
   : returns: transcribed text 
   """ 
   kwards = {}
   if language: 
      kwargs["language"] = language

  

   response = client.audio.transcriptions.create(model=os.getenv("OPENAI_AUDIO_MODEL", model_name), file = audio_file, **kwargs,)
   return response.text 
