import torch
from espnet2.bin.tts_inference import Text2Speech
import soundfile

class Pesuda:
    def __init__(self):
        device = f'cuda:{torch.cuda.current_device()}' if torch.cuda.is_available() else 'cpu'
        self.model = Text2Speech.from_pretrained("espnet/kan-bayashi_ljspeech_vits",device = device)
    
    def pesu(self, text):
        speech = self.model(text)["wav"]
        soundfile.write("out.wav", speech.cpu().numpy(), self.model.fs, "PCM_16")
        return "out.wav"