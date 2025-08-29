import mimetypes
import os
import argparse
import google.generativeai as genai
from PIL import Image

from google.generativeai import types

def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to: {file_name}")

def generate(image_path, prompt_text, save_path):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model_name = "gemini-2.5-flash-image-preview"
    model = genai.GenerativeModel(model_name)

    # Read image file using PIL
    img = Image.open(image_path)

    contents = [
        img,
        prompt_text
    ]

    generation_config = genai.GenerationConfig()

    file_index = 0
    for chunk in model.generate_content(contents, generation_config=generation_config, stream=True):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"{save_path}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            # Ensure the save_path has an extension, if not, add the guessed one
            if not os.path.splitext(file_name)[1]:
                file_name += file_extension
            save_binary_file(file_name, data_buffer)
        else:
            print(chunk.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AI image with a prompt.")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image file.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for image generation.")
    parser.add_argument("--output", type=str, default="generated_image.jpeg", help="Path to save the generated image file.")
    args = parser.parse_args()

    generate(args.image, args.prompt, args.output)
