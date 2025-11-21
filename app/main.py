# app/main.py
from io import BytesIO

# fastapi 
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# using schemas to avoid edge-case handling 
from .schemas import TranscriptRequest, MeetingSummary, ErrorResponse
# files imports 
from .stt import transcribe_audio
from .summarizer import summarize_transcript

app = FastAPI(
    title="Meeting Minutes LLM Service",
    version="0.1.0",
    description="Transcribe audio and generate meeting summaries, decisions and action items.",
)

# cors for browsers 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for prod? 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# health check for docker 
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/summarize/transcript",
    response_model=MeetingSummary,
    responses={400: {"model": ErrorResponse}},
)
def summarize_from_transcript(payload: TranscriptRequest):
    transcript = payload.transcript.strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    summary = summarize_transcript(transcript)
    return summary


@app.post(
    "/summarize/audio",
    response_model=MeetingSummary,
    responses={400: {"model": ErrorResponse}},
)

# async for better scaling 
async def summarize_from_audio(file: UploadFile = File(..., description="Audio file (e.g. mp3, m4a, wav)")):
    if not file.filename:
        # no filename exception 
        raise HTTPException(status_code=400, detail="No filename.")
    if not file.content_type.startswith("audio/"):
        #  wrong content type 
        raise HTTPException(
            status_code=400,
            detail=f"Wrong content type: {file.content_type}. Must be audio.",
        )
    # expand exception handling later! 
  
    try:
        audio_bytes = await file.read()
        
        if not audio_bytes:
            # empty file 
            raise HTTPException(status_code=400, detail="Empty audio file.")

        audio_file = BytesIO(audio_bytes)
        audio_file.name = file.filename
        transcript = transcribe_audio(audio_file) 
        summary = summarize_transcript(transcript)
        return summary
      
    except HTTPException:
        raise
    except Exception as e:
        # general error 
        raise HTTPException(status_code=500, detail=f"Some sort of error, idk: {e}")
