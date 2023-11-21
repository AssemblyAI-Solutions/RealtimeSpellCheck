import assemblyai as aai
from termcolor import colored
from llm import chat, lemur
import sys, os

aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

def on_data(transcript: aai.RealtimeTranscript):
  "This function is called when a new transcript has been received."
  if not transcript.text:
    return

  if isinstance(transcript, aai.RealtimeFinalTranscript):
    words = [word.text for word in transcript.words if word.confidence < 0.5]
    if words != []:
      sentence = ''
      # print(transcript.text)
      for w in transcript.words:
        if w.confidence < 0.5:
          sentence += f'[{w.text}] '
          # print(colored(w.text, 'red'), end=' ')
        else:
          # print(w.text, end=' ')
          sentence += f'{w.text} '
      correction = chat(sentence)
      if correction != 'none':
        correction = correction.replace('[', '').replace(']', '')
        correction = correction.replace('<order>', '').replace('</order>', '')

        if correction == transcript.text:
          print(transcript.text)
        else:
          print(colored(transcript.text, 'red'), end=' => ')
          print(colored(correction, 'green'))
    else:
      print(transcript.text)

def on_error(error: aai.RealtimeError):
  "This function is called when the connection has been closed."

  print("An error occured:", error)

with open('menu.txt', 'r') as f:
  menu_items = f.read().split('\n')

# Create the Real-Time transcriber
transcriber = aai.RealtimeTranscriber(
  on_data=on_data,
  on_error=on_error,
  sample_rate=8000,
  word_boost=menu_items
)

# Start the connection
transcriber.connect()

# filename = './audio/' + '263cf221-5919-4c06-a98c-fa18c6d9e3c2' + '.wav'
filename = sys.argv[1]
if not filename:
  print('Please provide a file path')
  sys.exit()

file_stream = aai.extras.stream_file(
  filepath=f"{filename}",
  sample_rate=8000,
)

transcriber.stream(file_stream)

transcriber.close()