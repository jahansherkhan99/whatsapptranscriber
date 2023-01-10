import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from local_upload import AssemblyAI

import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import ssl


####This could turn into a function and the second function would be local and that 
####input would be received from the UI

# This function will download all files from Google Drive to a local space
# Returns: N/A
def download_file():
    file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
    for index, file in enumerate(file_list):
        file.GetContentFile(r'./Media/' + file['title'])
        print(index+1, 'file downloaded: ', file['title'])
        file.Trash()

def collect_text_files():
    text_file_array = []
    for filename in os.listdir(r"./"):
        f = os.path.join(r"./", filename)
        # checking if it is a file
        if os.path.isfile(f) and f.endswith('.txt'):
            text_file_array.append(f)
    return text_file_array
        
def rename_files():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    for filename in text_file_array:
        names = []
        with open(filename, 'r') as file:
            file_string = file.read()
            nltk_results = ne_chunk(pos_tag(word_tokenize(file_string)))
            for nltk_result in nltk_results:
                if type(nltk_result) == Tree:
                    name = ''
                    for nltk_result_leaf in nltk_result.leaves():
                        name += nltk_result_leaf[0] + ' '
                    if nltk_result.label() == "PERSON":
                        names.append(name)           
            print(names)
            renamed_file = input('Enter your input:')
            os.rename(r"./" + filename, "" + renamed_file + ".txt")




gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
folder = '1YcfWCcYjBoj2mTkcHFS0z40K5efoKgDW'

download_file()

transcribe_file = AssemblyAI()
transcribe_file.initialize()
text_file_array = collect_text_files()
rename_files()












# # This function will traverse the current directory and search for all
# # audio files 
# # Returns: In list format

# def all_audio_files():
#     files = [f for f in os.listdir(r'./Media') if os.path.isfile(f)]
#     wav_files = []
#     for f in files:
#         if f[-3:] == "wav" or f[-3:] == "m4a":
#             wav_files.append(f)
#     return wav_files


# wav_files = all_audio_files()
# print(wav_files)





# file1 = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : 'helloooo.txt'})
# file1.SetContentString('Hello world!')
# file1.Upload()



