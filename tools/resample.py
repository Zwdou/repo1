import os
import librosa
import soundfile as sf
import numpy as np

def wav_file_resample(src, dst, dst_sample):
    """
    对目标文件进行降采样，采样率为dst_sample
    :param src:源文件路径
    :param dst:降采样后文件保存路径
    :param dst_sample:降采样后的采样率
    :return:
    """
    src_sig, sr = sf.read(src)
    src_sig = src_sig.T
    dst_sig = librosa.resample(src_sig, sr, dst_sample)
    dst_sig = dst_sig.T
    sf.write(dst, dst_sig, dst_sample)

def _pcm16to32(audio):
    assert (audio.dtype == np.int16)
    audio = audio.astype("float32")
    bits = np.iinfo(np.int16).bits
    audio = audio / (2 ** (bits - 1))
    return audio

def _pcm32to16(audio):
    assert (audio.dtype == np.float32)
    bits = np.iinfo(np.int16).bits
    audio = audio * (2 ** (bits - 1))
    audio = np.round(audio).astype("int16")
    return audio

def resample_from_paddlespeech(src,dst,dst_sample):
    audio, audio_sample_rate = sf.read(src, dtype="int16", always_2d=True)
    if audio.shape[1] >= 2:
        audio = audio.mean(axis=1, dtype=np.int16)
    else:
        audio = audio[:, 0]
    # pcm16 -> pcm 32
    audio = _pcm16to32(audio)
    audio = librosa.resample(audio, audio_sample_rate, dst_sample)
    # pcm32 -> pcm 16
    audio = _pcm32to16(audio)
    sf.write(dst, audio, dst_sample)

def resample_file(raw_audio_path, save_path):
    print("start resampling" + " " + raw_audio_path)
    head, tail = os.path.split(raw_audio_path)
    tail = tail.replace(".wav","_16k.wav")
    dst  = os.path.join(save_path, tail)
    resample_from_paddlespeech(src=raw_audio_path, dst = dst, dst_sample=16000)
    return dst
        
if __name__ == '__main__':
    resample_file(raw_audio_path='./tmp/test1.wav',save_path="./tmp")
    
