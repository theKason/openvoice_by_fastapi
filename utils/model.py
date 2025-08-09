from pathlib import Path
from typing import Union

import torch
from openvoice_service.openvoice import se_extractor
from openvoice_service.openvoice.api import ToneColorConverter
from melo.api import TTS

from fastapi import HTTPException

# Base directory where this file resides
BASE_DIR = Path(__file__).resolve().parent

class OpenVoiceManager:
    def __init__(self,
                 base_checkpoint_dir: str = "checkpoints_v2",
                 device: str = None):
        # set checkpoint paths - go up one level to project root
        self.base_checkpoint_dir = BASE_DIR.parent / "openvoice_service" / base_checkpoint_dir
        self.base_speaker = self.base_checkpoint_dir / "base_speakers/ses"
        self.ckpt_converter = self.base_checkpoint_dir / "converter"

        # choose device: CUDA if available, else CPU
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")

        # initialize tone-color converter and load its checkpoint
        self.tone_color_converter = ToneColorConverter(
            str(self.ckpt_converter / "config.json"),
            device=self.device
        )
        self.tone_color_converter.load_ckpt(str(self.ckpt_converter / "checkpoint.pth"))

        # load the default (source) speaker embedding for conversion
        self.source_se = torch.load(
            str(self.base_speaker / "en-default.pth"),
            map_location=self.device
        )

        # load the TTS model once at startup
        self.model = TTS(language="EN", device=self.device)

        # will hold the user's extracted embedding after extract_tone_color()
        self.target_se = None

    async def extract_tone_color(self, reference_speaker: Union[str, Path]):
        """
        Extract the user's voice embedding from a .wav file.
        Stores result in self.target_se.
        """
        path = Path(reference_speaker)
        if not path.exists():
            raise FileNotFoundError(f"Reference file not found: {path}")
        if path.suffix.lower() != ".wav":
            raise ValueError("Only .wav files are supported for voice extraction")

        # perform speaker embedding extraction with VAD enabled
        self.target_se, _ = se_extractor.get_se(
            str(path),
            self.tone_color_converter,
            vad=True
        )

    async def generate_clone_voice(self,
                                   text: str,
                                   tmp_wav_path: str,
                                   output_path: str,
                                   speed: float = 1.0):
        """
        1) Use base speaker to synthesize a temporary wav file.
        2) Convert its voice style using the extracted target embedding.
        """
        if self.target_se is None:
            raise RuntimeError("No target embedding: call extract_tone_color() first")

        # lookup the base speaker ID from model config
        spk2id = self.model.hps.data.spk2id
        base_id = spk2id["EN-Default"]


        # synthesize base audio (no style conversion yet)
        self.model.tts_to_file(
            text=text,
            speaker_id=base_id,
            output_path=tmp_wav_path,
            speed=speed
        )

        # apply tone-color conversion: source_se -> target_se
        self.tone_color_converter.convert(
            audio_src_path=tmp_wav_path,
            src_se=self.source_se,
            tgt_se=self.target_se,
            output_path=output_path,
            message="@MyShell"
        )
