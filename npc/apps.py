from openai import Image

import os
import time 
from dotenv import load_dotenv
load_dotenv()

def get_dalle_template(text):
    return f"{text} fantasy horror rpg, first person cinematic beautiful warm light #ffe466"

class DalleApp:
    def __init__(self, size="512x512"):
        self.size = size
        self.cache = {}

    def get_image(self, text):
        """Get an image from OpenAI's DALL-E model."""
        if text in self.cache:
            # print(f"Using cached image for {text}")
            return self.cache[text]
        # print(f"Generating image for {text}")
        response = Image.create(
            prompt=get_dalle_template(text),
            n=1,
            size=self.size,
            api_key=os.getenv("OPENAI_API_KEY"),
            )

        url = response['data'][0]['url']
        url = str(url)
        self.cache[text] = url
        
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
        