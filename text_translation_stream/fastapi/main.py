import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

load_dotenv()
deployment_name = os.getenv('GPT_3_5_DEPLOYMENT_NAME')

model = AzureChatOpenAI(
    azure_deployment=deployment_name,
    openai_api_version="2024-02-01"
)

app = FastAPI()


class TranslationPayload(BaseModel):
    language: str | list
    text: str


async def generate_translation(payload):
    system_template = "Translate the following text into {language}. Create separate paragraphs for every language."

    prompt_template = ChatPromptTemplate.from_messages([
        ('system', system_template),
        ('user', '{text}')
    ])

    parser = StrOutputParser()

    chain = prompt_template | model | parser

    async for chunk in chain.astream(payload.dict()):
        yield chunk


@app.post("/translate/")
async def translate(payload: TranslationPayload):
    generator = generate_translation(payload)
    return StreamingResponse(generator, media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000)
