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


def gpt4v_call_adjust(origImg, genImg, prompt, annotations = None):

    if annotations:
        response = OpenAI().chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "text", "text": "Reference Webpage: "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{origImg}",
                                "detail": "high",
                            },
                        },
                        {"type": "text", "text": "\nCurrent Webpage "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{genImg}",
                                "detail": "high",
                            },
                        },
                        {"type": "text", "text": "FOCUS ON the RED Rectangles and improve the html by the following annotations:" + annotations},
                    ],
                }
            ],
            max_tokens=4096,
            temperature=0.0,
            seed=2024,
        )
    else:
        response = OpenAI().chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "text", "text": "Reference Webpage: "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{origImg}",
                                "detail": "high",
                            },
                        },
                        {"type": "text", "text": "\nCurrent Webpage Screensht: "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{genImg}",
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

def gpt4v_call_modify(genImg, prompt, annotations):

    response = OpenAI().chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "text", "text": "\nCurrent Webpage Screensht: "},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{genImg}",
                                "detail": "high",
                            },
                        },
                        {"type": "text", "text": "FOCUS ON the section WITHIN the RED Rectangles and improve the html by the following commends:" + annotations},
                    ],
                }
            ],
            max_tokens=4096,
            temperature=0.0,
            seed=2024,
        )
    
    response = response.choices[0].message.content.strip()

    return response
