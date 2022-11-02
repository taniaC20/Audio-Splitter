import os
import io
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub.playback import play
import librosa
import argparse

parser = argparse.ArgumentParser(description='Reading index of unit directories.')
parser.add_argument("-i",'--index',type=int, help='units index')
parser.add_argument("-p",'--practice',type=bool, help='Is Practice?')
args = parser.parse_args()

print(f"Command-line arguments: {args}")

units_index = args.index
is_practice = args.practice

if units_index == None:
  raise Exception("UNITS INDEX IS NONE...")

print(f"UNITS INDEX = {units_index}")

def get_files_directory(directory_path):
  path = f"{directory_path}/"
  files_list=[]
  files = os.listdir(path)

  for f in files:
    files_list.append(str(f))

  print("Files Directory:",files_list)
  return files_list

def get_folders_directory(directory_path):
  folder = f"{directory_path}/"
  files_list=[name for name in os.listdir(folder) if os.path.isdir(name)]
  print("Folder Directory:",files_list)
  return files_list

root_path         = "/project/6045556/tnchevez/audio_splitter"
audio_units_folder = f'{root_path}/all_recordings'
units_array= get_files_directory(audio_units_folder)
print(f"Array of directories:{units_array}")
print(f"Length Array of directories = {len(units_array)}")
all_audios_path   = f'{audio_units_folder}/{units_array[units_index]}'

def split_by_bytes(name,audio_filepath,output_filepath):
  one_mb_size = 1024 * 1024 
  total_byte_size = os.path.getsize(audio_filepath)
  total_byte_size_mb = total_byte_size/one_mb_size
  total_byte_size_gb = total_byte_size/(one_mb_size*1000)
  total_chunks_len = int(total_byte_size_mb / 30)
  
  mb_chunk_size = 30
  chunk_size_b = mb_chunk_size * one_mb_size
  f = open(audio_filepath, 'rb')
  counter = 1

  time="0"
  temp_seconds=0.0
  total_seconds=0.0
  while True:
      byte_chunk = f.read(chunk_size_b)  
      if not byte_chunk:
          print(f"Unable to read chunk at index {counter}")
          break
      sound_chunk = AudioSegment.from_file(io.BytesIO(byte_chunk), format="mp3")
      output_filename = f"{output_filepath}/{name}_{time}.mp3"
      sound_chunk.export(output_filename, format="mp3")
      counter += 1
      total_seconds = librosa.get_duration(filename=output_filename) + temp_seconds
      temp_seconds  = total_seconds
      hours, mins, seconds = audio_duration(int(total_seconds))
      time = f"{hours};{mins};{seconds}"
  f.close()

def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds

def split_all_audios():
  print("Enters")
  all_recordings_directories_list = get_files_directory(all_audios_path)

  for folder in all_recordings_directories_list:
      folder_path = f"{all_audios_path}/{folder}"
      print("Folder_path :", folder_path)
      recordings_list = get_files_directory(folder_path)

      for audio_file in recordings_list:
        recording_path= f"{folder_path}/{audio_file}"
        recording_folder_name = audio_file.strip(".mp3")
        output_folder_recording = f"{folder_path}/{recording_folder_name}"
        
        try:
          if not os.path.exists(output_folder_recording):
              os.makedirs(output_folder_recording)
        except Exception as e:
          print("ERROR CREATING FOLDER: ", e)
        
        
        split_by_bytes(recording_folder_name,recording_path,output_folder_recording)
        os.remove(recording_path)

def check_if_directory(Array):

  for element in Array:
    substring=".mp3"
    if substring not in element:
      Array.remove(element)
  return Array
  

if __name__ == "__main__":
    split_all_audios()   
