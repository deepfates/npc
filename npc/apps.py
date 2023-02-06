from openai import Image # type: ignore

import os
from asyncstdlib.functools import lru_cache # type: ignore
from dotenv import load_dotenv
load_dotenv()

def get_dalle_template(text):
    return f"{text} fantasy horror rpg, first person cinematic beautiful warm light #ffe466"

@lru_cache(maxsize=None)
async def generate_image(text):
    """Get an image from OpenAI's DALL-E model."""
    # print(f"Generating image for {text}")
    response = Image.create(
        prompt=get_dalle_template(text),
        n=1,
        size="256x256",
        api_key=os.getenv("OPENAI_API_KEY"),
        )

    url = response['data'][0]['url']
    url = str(url)
    
    return url

def get_template(token):
    def template(text):
        return f"Adventure game screencap, beautiful graphics, {token}:{text} first person beautiful graphics, CRT screen vignette scanlines"
    return template


from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document

class Summarizer():

    def __init__(self) -> None:
        self.llm = OpenAI(temperature=0.0, max_tokens=60)
        self.chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        self.cache: dict[str, str] = {}

    def run(self, text):
        if text in self.cache:
            return self.cache[text]
        doc = Document(page_content=text)
        summary = self.chain.run([doc])
        self.cache[text] = summary
        return summary
        