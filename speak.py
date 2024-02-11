import torch
from espnet2.bin.tts_inference import Text2Speech
import soundfile

class TextSpeech:

    def __init__(self):
        """
        Initialize the Text2Speech model.
        """
        device = f'cuda:{torch.cuda.current_device()}' if torch.cuda.is_available() else 'cpu'
        self.speech_model = Text2Speech.from_pretrained("espnet/kan-bayashi_ljspeech_vits",device = device)
    
    def render(self, text: str) -> str:
        """
        Render the text to speech and save it as a wav file.

        Args:
        text (str): The input text to be synthesized.

        Returns:
        str: The path of the generated wav file.
        """
        speech = self.speech_model(text=text)["wav"]
        soundfile.write("out.wav", speech.cpu().numpy(), self.speech_model.fs, "PCM_16")
        return "out.wav"