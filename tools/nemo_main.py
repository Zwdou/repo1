##nemo installation https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/starthere/intro.html#installation
## asr using NeMo
##pip install Cython
##pip install nemo_toolkit[all]
import os
import paddle
from paddlespeech.cli import TextExecutor
import nemo
# Import Speech Recognition collection
import nemo.collections.asr as nemo_asr
import pycorrector



##sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# Speech Recognition model - stt_zh_citrinet_512
##model -stt_zh_citrinet_1024_gamma_0_25

def asr(audio_file):
    quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="stt_zh_citrinet_1024_gamma_0_25").cuda()
    text = quartznet.transcribe([audio_file])
    print('ASR Result: \n{}'.format(text))
    return text

def asr_corr(text):
    correct_sent, detail = pycorrector.correct(text)
    print('Corrected Result: \n{}'.format(correct_sent))
    print('Detail: \n{}'.format(detail))
    return correct_sent

def textExecutor(text):
    if not text or text == '':
        return ''
    try:
        text_executor = TextExecutor()
        result = text_executor(
            text=text,
            task='punc',
            model='ernie_linear_p7_wudao',
            lang='zh',
            config=None,
            ckpt_path=None,
            punc_vocab=None,
            device=paddle.get_device())
        print('Text Result: \n{}'.format(result))
        return result
    except:
        return ''
    
def asr_file(segment_path, save_path):
    print("start processing " + segment_path)
    audiofiles = []
    head, tail = os.path.split(segment_path)
    
    for files in os.listdir(segment_path):
        if files.endswith('.wav') :
            audiofiles.append(files)
    audiofiles.sort(key=lambda x : int(x[6:-4]))
    for audiofile in audiofiles:
        audiofile_path = os.path.join(segment_path,audiofile)
        #print(audiofile)
        text = str(asr(audio_file=audiofile_path))
        #corr_text = asr_corr(text)
        punc_text = textExecutor(text)
        with open(os.path.join(save_path,str(tail +'.txt')),'a', encoding='utf-8') as f :
            f.write(punc_text + '\n')
    return os.path.join(save_path,str(tail +'.txt'))

if __name__ == '__main__':
    asr_file(segment_path="/tmp/test1",save_path="/tmp")
    
        