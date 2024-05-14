import json
import sys
import os

import requests
import base64

root_dir = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(0, root_dir)

from utils.constants import API_KEY, ORGANIZATION_ID, PROJECT_ID

# Function to encode the image
def encode_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def predict_image(image_path: str, prompt: str, max_tokens: int) -> dict:
    """
        :param image_path: Directory to image
        :param prompt: Prompt used in the GPT-4o inference
        :return: dictionary containing the response of GPT-4o inference
    """
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "OpenAI-Organization": ORGANIZATION_ID,
        "OpenAI-Project": PROJECT_ID,
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ],
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()


if __name__ == '__main__':
    image_path = os.path.join(root_dir, 'clip-gpt-captioning/images/screwdriver.jpeg')
    prompt = 'In four to five words, answer this question: what object is in the center of this image?'

    response = predict_image(image_path, prompt, 10)

    output_name = image_path.split('/')[-1].replace('.jpeg', '.json')
    output_dir = os.path.join(root_dir, 'data/output', output_name)

    with open(output_dir, 'w') as json_output:
        json.dump(response, json_output, indent=4)