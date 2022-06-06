#!/usr/bin/env python3
#apt-get update && apt-get install -y libsndfile1 ffmpeg
'''
Author: iris.yan
Created Date: Thursday, May 17th 2022, 18:50 pm

Edited 2022-06-01 16:53:57 By Zhiwei Dou
Description: convert video to audio

Copyright (c) 2022 philips
'''

import sys
import time
import os
import pipes


def video_to_audio(video_dir, audio_save_dir):
    
    try:
        file, file_extension = os.path.splitext(video_dir)
        head, tail = os.path.split(video_dir)
        tail = tail.replace(".mp4","")
        file = pipes.quote(file)
        video_to_wav = 'ffmpeg -i ' + file + file_extension + ' ' + audio_save_dir +'/'+ tail + '.wav'
        # final_audio = 'lame ' + file + '.wav' + ' ' + file + '.mp3'
        os.system(video_to_wav)
        # os.system(final_audio)
        print("sucessfully converted ", video_dir, " into audio!")
        audio_path = audio_save_dir+'/'+tail+'.wav'
        return audio_path
    except OSError as err:
        print(err.reason)
        exit(1)


def v2a_main(path,audio_save_dir):
    try:
        if os.path.exists(path):
            print("file found!")
    except OSError as err:
        print(err.reason)
        exit(1)
        # convert video to audio
    return video_to_audio(path, audio_save_dir)
        


# install ffmpeg and/or lame if you get an error saying that the program is currently not installed
if __name__ == '__main__':
    v2a_main(path = 'video-keyframe-ocr-text/demo_thing/videos_apitest',audio_save_dir = './tmp')