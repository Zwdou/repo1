import imp
import os
import configparser
from tools.main_to_audio_convert import v2a_main
from tools.resample import resample_file
from tools.audio_seg_main import audioseg_main
from tools.nemo_main import asr_file
from tools.exttags_main import tag_file
from tempfile import TemporaryDirectory
import time

config = configparser.ConfigParser()
config.read('config.ini')

video_dir = config['asr_text']['video_dir']
text_save_file = config['asr_text']['text_save_dir']

for filepath in os.listdir(video_dir):
    head, tail = os.path.split(filepath)
    tail = tail.replace(".mp4","")
    with TemporaryDirectory() as savepath:
        wavpath = v2a_main(os.path.join(video_dir,filepath),audio_save_dir=savepath)
        resampath = resample_file(wavpath,save_path=savepath)
        segpath = audioseg_main(resampath,snip_to_save=savepath)
        textpath = asr_file(segpath,save_path=savepath)
        tagtext = tag_file(textpath)
        with open(os.path.join(text_save_file,str('asr_tags.txt')),'a', encoding='utf-8') as f :
            f.write(tail + ":")
            f.write(str(tagtext) + '\n')
        time.sleep(1)