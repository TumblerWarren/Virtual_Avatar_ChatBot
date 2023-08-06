from fastapi import FastAPI, HTTPException
from voicevox import Client
import translationtest
import uvicorn
import program_run_test

app = FastAPI()


@app.get("/generate_voice/")
async def generate_voice(text: str, speaker_id: int, path: str):
    text=translationtest.translation(text,"ja")
    async with Client() as client:
        try:
            audio_query = await client.create_audio_query(text, speaker=speaker_id)

            with open(path, "wb") as f:
                f.write(await audio_query.synthesis(speaker=speaker_id))
            return {"message": "Voice generated successfully", "file_path": path}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    program_run_test.program_run_main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
