import requests
import time
import datetime
import pyaudio
import wave

API_KEY_ASSEMBLY_AI = "9fb1af9191744d6ea898e45a018ab7ad"
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY_ASSEMBLY_AI}

def audio_file_handler(audio_file):
    audio_url = upload(audio_file)
    text = save_transcript(audio_url, audio_file)
    return text

    #UPLOADING FILE TO ASSEMBLYAI API
### PARAMETER: Name of uploaded file
### RETURN: string:URL of our file on ASSEMBLYAI
def upload(filename):
    upload_response = requests.post(upload_endpoint,
                            headers=headers,
                            data=filename)

    audio_url = upload_response.json()['upload_url']
    return audio_url


#TRANSCRIPTION
### PARAMETER: Url of our file n ASSEMBLYAI
### RETURN: int:ID of the job working on the transcription of our file
def transcribe(audio_url):
    transcript_request = { "audio_url": audio_url, "language_detection": True }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    job_id= transcript_response.json()['id']
    return job_id

#ASKING API TO CHECK FILE TRANSCRIPTION STATUS
### PARAMETER: Job ID working on the transcription
### RETURN: ASSEMBLYAI API response, containting job status
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

#KEEP CHECKING STATUS UNTIL TRANSCRIPTION IS COMPLETED
### PARAMETER: ID of the job working on the transcription
### RETURN: string:Transcription status (completed, error, in progress)
def get_transcription_status(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        data = poll(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        print('Transcription not ready.. Waiting 10 seconds before calling ASSEMBLYAI API again.')
        time.sleep(10)
    
        
#SAVING TRANSCRIPTION IN TXT FILE
### PARAMETER: Id of the job working on the transcription
### RETURN: /
def save_transcript(audio_url, filename):
    data, error = get_transcription_status(audio_url)
    
    if data:
        print(data)
        print(data['text'])
        return data['text']

    elif error:
        print("ERROR!!", error)