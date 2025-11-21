# Auto-generated Meeting Notes with LLM

A ready-to-use service suitable for local machines. 
Easy use instructions, fast run time, and consistent output formatting. 
- Accepts audio files OR raw transcripts
- Transcribes audio with OpenAI's audio API
- Summarizes the meeting in under 200 words.
- Records *decisions* and *action items* with any associated details. 


Current system requirements and their implementation: 
| **System Requirements**                                                  | **Features**                                                   |
| ------------------------------------------------------------------------ | -------------------------------------------------------------- |
| Ensure that the model always outputs notes in the same consistent format | pydantic schemas (`MeetingSummary`)                            |
| Validate all incoming requests to ensure they are in the right format    | pydantic models (`TranscriptRequest`, `ErrorResponse`)         |
| Transcribe audio using OpenAI API                                        | OpenAI Audio API wrapper (`gpt-4o-transcribe` or `whisper-1`)  |
| Provide a programmatic interface (API) for other services to call        | FastAPI server                                                 |
| Should be possible to run in a browser (browser frontends)               | CORS                                                           |
| Local                                                                    | Simple virtual environment setup + `uvicorn` hot reload        |
| Containerised                                                            | Dockerfile                                                     |


## How to set up locally?
```
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="sk-..."    # Windows: set OPENAI_API_KEY=sk-...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```


Using Docker: from the project root... 
```
docker build -t meeting-minutes-llm .
docker run --rm -p 8000:8000 \
  -e OPENAI_API_KEY="sk-YOUR_KEY_HERE" \
  meeting-minutes-llm
```
