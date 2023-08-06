from gzstv.utils import get_hparams_from_file, load_checkpoint
from gzstv.models import SynthesizerTrn
from gzstv.text.symbols import symbols
from pathlib import Path
import gdown
import os

def get_model(device = 'cpu'):
    
    model_path = Path(__file__).resolve().parent.joinpath("rsa.pth")
    model_url = "https://drive.google.com/file/d/1D5dzRnCeXrxVl6UuMQ8hO_qhBOMXXkUt/view?usp=sharing"
    if not os.file.exists(model_path):
        print("Downloading model...")
        gdown.download(model_url, model_path, quiet=False, fuzzy=True)

    hps = get_hparams_from_file(Path(__file__).resolve().parent.joinpath("rsa.json"))

    net_g = SynthesizerTrn(
        device,
        len(symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    _ = net_g.eval()

    _ = load_checkpoint(model_path, net_g)
    return net_g