from embedart.prompt import promptsToString, DEFAULT_NEGATIVE_PROMPTS
from embedart.image import pil_to_b64
import io
import base64
import requests
from PIL import Image

class ControlnetRequest:
    def __init__(self, prompt, input_image, seed):
        # self.url = "http://localhost:7860/sdapi/v1/txt2img"
        self.url = "http://192.168.86.30:7860/sdapi/v1/txt2img"
        self.prompt = promptsToString(prompt)
        self.seed = seed
        self.input_image = input_image
        self.body = {
            "prompt": self.prompt,
            "negative_prompt": promptsToString(DEFAULT_NEGATIVE_PROMPTS),
            "batch_size": 1,
            "steps": 20,
            "seed": self.seed,
            "cfg_scale": 7,
            "alwayson_scripts": {
                "controlnet": {
                    "args": [
                        # Worked quite well up to a point.
                        # {
                        #     "enabled": True,
                        #     "weight": 0.9,

                        #     # Preprocessor
                        #     # "module": "inpaint_global_harmonious",
                        #     # "model": "control_v11p_sd15_inpaint",
                        #     # "weight": 0.7,

                        #     # "module": "tile_resample",
                        #     # "model": "control_v11f1e_sd15_tile",

                        #     # "module": "lineart_coarse",
                        #     # "model": "control_v11p_sd15_lineart",
                        #     "module": "lineart_realistic",
                        #     "model": "control_v11p_sd15_lineart",

                        #     # "module": "softedge_hedsafe",
                        #     # "model":"control_v11p_sd15_softedge",
                        #     # "module": "depth_midas",
                        #     # "model":"control_v11f1p_sd15_depth",

                        #     # "module": "canny",
                        #     # "model": "control_v11p_sd15_canny",
                        #     # "weight": 0.65,

                        #     "guidance_start": 0.,
                        #     "guidance_end": 0.9,
                        #     "image": self.input_image,
                        #     "resize_mode": 1,
                        #     "lowvram": False,
                        #     "processor_res": 64,
                        #     "threshold_a": 64,
                        #     "threshold_b": 64,
                        #     "control_mode": 0,
                        #     "pixel_perfect": False
                        # },

                        # https://www.nextdiffusion.ai/tutorials/how-to-create-amazing-looking-qr-codes-with-stable-diffusion
                        {
                            "enabled": True,
                            # Preprocessor
                            "module": "inpaint_global_harmonious",
                            "model": "control_v1p_sd15_brightness",
                            "weight": 0.5,
                            "guidance_start": 0.0,
                            "guidance_end": 0.75,
                            "image": self.input_image,
                            "resize_mode": 1,
                            "lowvram": False,
                            "processor_res": 64,
                            "threshold_a": 64,
                            "threshold_b": 64,
                            "control_mode": 0,
                            "pixel_perfect": False
                        },
                        {
                            "enabled": True,
                            # Preprocessor
                            "module": "inpaint_global_harmonious",
                            "model": "control_v11p_sd15_lineart",
                            "weight": 0.35,
                            "guidance_start": 0,
                            "guidance_end": 0.75,
                            "image": self.input_image,
                            "resize_mode": 1,
                            "lowvram": False,
                            "processor_res": 64,
                            "threshold_a": 64,
                            "threshold_b": 64,
                            "control_mode": 0,
                            "pixel_perfect": False
                        },
                    ]
                }
            }
        }

    def send_request(self):
        response = requests.post(url=self.url, json=self.body)
        return response.json()

def generate(prompt, seed, input_image):
    encoded_input = pil_to_b64(input_image)
    control_net = ControlnetRequest(prompt, encoded_input, seed)
    output = control_net.send_request()

    result = output['images'][0]

    image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
    return image
