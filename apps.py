import replicate
from dotenv import load_dotenv
load_dotenv

# model = replicate.models.get("cjwbw/elden-ring-diffusion")
# version = model.versions.get("664395b745271027942906c3846671cc71c49f75509078bf3ac9d85388b2f6ac")
model = replicate.models.get("nitrosocke/arcane-diffusion")
version = model.versions.get("a8cd5deb8f36f64f267aa7ed57fce5fc7e1761996f0d81eadd43b3ec99949b70")


class DiffusionApp:
    def __init__(self):
        self.cache = {}
        
    async def get_image(self, text):
        clean_text = text.replace('\n', ' ').replace('\r', ' ').strip()
        prompt = f"Adventure game screencap, beautiful graphics, elden ring style:{clean_text} first person beautiful graphics, CRT screen vignette scanlines"
        print(prompt)
        if prompt in self.cache:
            return self.cache[prompt]
        inputs = {
            # Input prompt
            'prompt': prompt,

            # Width of output image. Maximum size is 1024x768 or 768x1024 because
            # of memory limits
            'width': 512,

            # Height of output image. Maximum size is 1024x768 or 768x1024 because
            # of memory limits
            'height': 256,

            # Number of images to output
            'num_outputs': 1,

            # Number of denoising steps
            # Range: 1 to 500
            'num_inference_steps': 35,

            # Scale for classifier-free guidance
            # Range: 1 to 20
            'guidance_scale': 10,

            # Random seed. Leave blank to randomize the seed
            'seed': 42,
        }
        output = version.predict(**inputs)
        self.cache[prompt] = output
        return output