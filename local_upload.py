import requests
import os

class AssemblyAI:
    def __init__(self):
        pass

    def initialize(self):
        list_of_files = os.listdir(r'./Media')
        for index, file in enumerate(list_of_files):
            filename = r'./Media/' + file
            link = self.__run__(filename)
            id = self.__submit__(link)
            self.__transcription__(id, index)
    
    def __run__(self, filename):
        def read_file(filename, chunk_size = 5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data
        headers = {'authorization' : "63255e5b7c7142e0b9360909d425649d"}
        response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data = read_file(filename))
        return response


    def __submit__(self, link):
        endpoint = "https://api.assemblyai.com/v2/transcript"
        headers = {"authorization": "63255e5b7c7142e0b9360909d425649d",
                    "content-type": "application/json"
                    }
        url = link.json()['upload_url']
        json = {'audio_url': url}

        response = requests.post(endpoint, json=json, headers=headers)
        return response.json()['id']
    


    def __transcription__(self, id, index):
        endpoint = "https://api.assemblyai.com/v2/transcript/" + id
        headers = {
            "authorization": "63255e5b7c7142e0b9360909d425649d",
        }
        response = requests.get(endpoint, headers=headers)
        if response.json()['status'] != 'completed':
            while response.json()['status'] != 'completed':
                response = requests.get(endpoint, headers=headers)

        with open('transcription#' + str(index) + '.txt', 'w') as f:
            f.write(response.json()['text'])







