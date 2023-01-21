import replicate
from dotenv import load_dotenv
load_dotenv


def get_template(token):
    def template(text):
        return f"Adventure game screencap, beautiful graphics, {token}:{text} first person beautiful graphics, CRT screen vignette scanlines"
    return template

# I want to make a type here that only takes certain strings
# and this function will return the correct model and version
# based on the string
def get_model(model_name):
    if model_name == "elden-ring-diffusion":
        model = replicate.models.get("cjwbw/elden-ring-diffusion")
        version = model.versions.get("664395b745271027942906c3846671cc71c49f75509078bf3ac9d85388b2f6ac")
        template = get_template('elden ring style')
    elif model_name == "arcane-diffusion":
        model = replicate.models.get("nitrosocke/arcane-diffusion")
        version = model.versions.get("a8cd5deb8f36f64f267aa7ed57fce5fc7e1761996f0d81eadd43b3ec99949b70")
        template = get_template('arcane style')
    elif model_name == "sd2":
        model = replicate.models.get("stability-ai/stable-diffusion")
        version = model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")
        template = lambda x: f"fantasy horror rpg, {x} first person cinematic beautiful warm light chiaroscuro #ffe466"
    else:
        raise ValueError("Model not found")
    return model, version, template
    
class DiffusionApp:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model, self.version, self.template = get_model(model_name)
        self.cache = {}
        
    async def get_image(self, text):
        clean_text = text.replace('\n', ' ').replace('\r', ' ').strip()
        prompt = self.template(clean_text)
        print(prompt)
        if prompt in self.cache:
            return self.cache[prompt]
        inputs = {
            # Input prompt
            'prompt': prompt,

            # Specify things to not see in the output
            'negative_prompt': 'muddy, blurry, grainy, photorealist, bad composition, bodies, people, portrait, pastoral,',

            # Choose a scheduler
            'scheduler': 'K_EULER',

            # Width of output image. Maximum size is 1024x768 or 768x1024 because
            # of memory limits
            'width': 768 if self.model_name == "sd2" else 512,

            # Height of output image. Maximum size is 1024x768 or 768x1024 because
            # of memory limits
            'height': 512 if self.model_name == "sd2" else 256,

            # Number of images to output
            'num_outputs': 1,

            # Number of denoising steps
            # Range: 1 to 500
            'num_inference_steps': 25,

            # Scale for classifier-free guidance
            # Range: 1 to 20
            'guidance_scale': 8,

            # Random seed. Leave blank to randomize the seed
            'seed': 42,
        }
        output = self.version.predict(**inputs)
        self.cache[prompt] = output
        return output

from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.docstore.document import Document
  
class Summarizer():

    def __init__(self) -> None:
        self.llm = OpenAI(temperature=0.0, max_tokens=60)
        self.chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        self.cache = {}

    def run(self, text):
        if text in self.cache:
            return self.cache[text]
        doc = Document(page_content=text)
        summary = self.chain.run([doc])
        self.cache[text] = summary
        return summary
        