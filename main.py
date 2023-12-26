from fastapi import FastAPI, HTTPException,Query,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from operation import TextOperation,SpeechOperation
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/')
def rootpage():
    return 'This Project is made for BHARAT HACKATHON by Team VedaByte'


@app.get('/text/')
async def text_operation(txt: str = Query(..., title="Text to Translate"),lang: str = Query(..., title="Language Code")):
    try:
        model = TextOperation(lang=lang)  
        output = model.translate(text=txt)
        model.text2speech(text=output)
        audio_path = os.path.join('./result.mp3')
        res= StreamingResponse(open(audio_path, 'rb'), media_type="audio/mp3", headers={"Content-Length": str(os.stat(audio_path).st_size)})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return res

@app.get('/translate/')
async def translate_call(txt:str=Query(...,title='Text To Translate')):
    try:
        model=TextOperation(lang='english')
        output=model.translate(text=txt)
    except Exception as e:
        raise HTTPException(status_code=404,detail=f"translation is not possible due to : {e}")
    return {"translate":output}

@app.post('/voice/')
async def voice_operation(audio: UploadFile = File(...), lang: str = Query(..., title="Language Code")):
    try:
        model = SpeechOperation(lang=lang)
        with open(audio.filename, "wb") as file:
            file.write(audio.file.read())
        txt = model.audio2text(audio.filename)
        output = model.translate(text=txt)
        model.text2speech(text=output)
        audio_path = os.path.join('./result.mp3')
        res = StreamingResponse(open(audio_path, 'rb'), media_type="audio/mp3",
                                headers={"Content-Length": str(os.stat(audio_path).st_size)})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return res