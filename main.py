import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "openvoice_service"))

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import uuid
import torch

from utilts.model import OpenVoiceManager

app = FastAPI()

BASE_DIR      = Path(__file__).resolve().parent
USER_DATA_DIR = BASE_DIR / "user_data"
UPLOADS_DIR   = USER_DATA_DIR / "uploads"
EMBEDS_DIR    = USER_DATA_DIR / "embeddings"
TMP_DIR       = USER_DATA_DIR / "tmp"
OUTPUTS_DIR   = USER_DATA_DIR / "outputs"

# ensure dirs exist
for d in (UPLOADS_DIR, EMBEDS_DIR, TMP_DIR, OUTPUTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

manager = OpenVoiceManager()


@app.post("/clone")
async def clone_voice(
    text: str = Form(...),
    audio: UploadFile = File(None),
    embed_id: str = Form(None),
):
    """
    - If `audio` provided: extract new embedding, ignore any embed_id field.
    - Else if valid `embed_id` provided: reuse saved embedding.
    - Returns: audio file (wav) as response body, with header X-Embed-ID set.
    """
    # 1) Determine or generate embed_id
    if audio:
        # new embedding
        embed_id = uuid.uuid4().hex
        wav_path = UPLOADS_DIR / f"{embed_id}.wav"
        with open(wav_path, "wb") as f:
            f.write(await audio.read())

        await manager.extract_tone_color(str(wav_path))
        torch.save(manager.target_se, EMBEDS_DIR / f"{embed_id}.pth")

    elif embed_id:
        # reuse existing embedding
        emb_file = EMBEDS_DIR / f"{embed_id}.pth"
        if not emb_file.exists():
            return JSONResponse({"message": "Invalid or expired embed_id"}, status_code=404)
        manager.target_se = torch.load(str(emb_file), map_location=manager.device)

    else:
        return JSONResponse({"message": "Provide either audio or embed_id"}, status_code=400)

    # 2) Paths for tmp and output
    tmp_wav = TMP_DIR     / f"{embed_id}_tmp.wav"
    out_wav = OUTPUTS_DIR / f"{embed_id}_out.wav"

    # 3) Generate cloned voice
    await manager.generate_clone_voice(
        text=text,
        tmp_wav_path=str(tmp_wav),
        output_path=str(out_wav),
        speed=1.0
    )

    # 4) Serve the file directly, with embed_id in headers
    response = FileResponse(
        str(out_wav),
        media_type="audio/wav",
        filename=f"{embed_id}.wav"
    )
    response.headers["X-Embed-ID"] = embed_id
    return response
