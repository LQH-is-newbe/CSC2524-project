from openai import OpenAI

def gpt4v_call(base64_image, prompt):
    response = OpenAI().chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        max_tokens=4096,
        temperature=0.0,
        seed=2024,
    )

    response = response.choices[0].message.content.strip()

    return response