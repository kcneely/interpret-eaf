##Interpret .eaf to produce .opus clips ELAN 6.1##
##Version 2021-05-01##
##Kelsey C. Neely and Alexander Dougal##

import subprocess
import glob
import os

file_path = "C:\\Users\\Kelsey\\Desktop\\Example\\Segments.eaf"
wav_file = "C:\\Users\\Kelsey\\Desktop\\Example\\Audio.wav"

output_stem = "C:\\Users\\Kelsey\\Desktop\\Example\\Clips\\"


with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

def find_time_from_ts(ts_value):
    return data.split('<TIME_SLOT TIME_SLOT_ID="{}" TIME_VALUE="'.format(ts_value))[1].split('"')[0]

def list_order(e):
    return e['start']


ordered_list = []
speaker_strings = []

def split_into_speaker_strings(full_string):
    full_split = full_string.split('<TIER LINGUISTIC_TYPE_REF="')
    for i in range(0, len(full_split)):
        if full_split[i][0:7] == "Phrases":
            speaker_strings.append(full_split[i])

split_into_speaker_strings(data)

#print(speaker_strings)

for j in range(0, len(speaker_strings)):
    speaker_name = speaker_strings[j].split('PARTICIPANT="')[1].split('"')[0]
    for i in range (0, 10000):
        try:
            hard_coded_prefix = '<ALIGNABLE_ANNOTATION ANNOTATION_ID="a{}"\n                TIME_SLOT_REF1="'.format(i)


            first_part = speaker_strings[j].split(hard_coded_prefix)[1]
            first_time_value = first_part.split('" TIME_SLOT_REF2="')[0]
            second_time_value = first_part.split('" TIME_SLOT_REF2="')[1].split('"')[0]

            start_time = int(find_time_from_ts(first_time_value))
            end_time = int(find_time_from_ts(second_time_value))
            duration = end_time - start_time
            ordered_list.append({"start":start_time, "end":end_time, "speaker":speaker_name, "duration": duration})
        except IndexError as e:
            k = i


print(ordered_list)
ordered_list.sort(key=list_order)

for i in range (0, len(ordered_list)):
    line_number = i+1
    
    start = ordered_list[i]['start']
    duration = ordered_list[i]['duration']
    speaker = ordered_list[i]['speaker']
    makewav = 'ffmpeg -i {} -ss "{}ms" -t "{}ms" {}{}-{}.wav'.format(wav_file, start, duration, output_stem, line_number, speaker)
    subprocess.call(makewav)
    
files = glob.glob('Clips\\*.wav')
for file in files:
    name = ''.join(file.split('.')[:-1])
    output = '{}.opus'.format(name)
    reencode = 'ffmpeg -i {} -ac 1 {}'.format(file, output)
    subprocess.call(reencode)

files = glob.glob('Clips\\*.wav')
for file in files:
    os.remove(file)