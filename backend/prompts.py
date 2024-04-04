from gpt4v import gpt4v_call, gpt4v_call_adjust, gpt4v_call_modify
from utils import cleanup_response

def initGenPrompt(img, description):

    ## Extract text from the webpage
    extract_prompt = "Extract all texts from this image. One line for each block of text."
    print("Extracting ...")
    texts = gpt4v_call(img, extract_prompt)
    print("Extracted")

    ## Generate the Html
    text_augmented_prompt = ""
    text_augmented_prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    
    if description:
        text_augmented_prompt += "A user will provide you with a screenshot of a webpage and a description to follow, along with all texts that they want to put on the webpage.\n"
        text_augmented_prompt += "The description is :\n" + description + "\n"
    else:
        text_augmented_prompt += "A user will provide you with a screenshot of a webpage to follow, along with all texts that they want to put on the webpage.\n"

    text_augmented_prompt += "The texts are:\n" + texts + "\n"
    text_augmented_prompt += "You should generate the correct layout structure for the webpage, and put the texts in the correct places so that the resultant webpage will look the same as the given one.\n"
    text_augmented_prompt += "You need to return a single html file that uses HTML and CSS to reproduce the given website.\n"
    text_augmented_prompt += "Include all CSS code in the HTML file itself.\n"
    text_augmented_prompt += "If it involves any images, use \"rick.jpg\" as the placeholder.\n"
    text_augmented_prompt += "Some images on the webpage are replaced with a blue rectangle as the placeholder, use \"rick.jpg\" for those as well.\n"
    text_augmented_prompt += "Do not hallucinate any dependencies to external files. You do not need to include JavaScript scripts for dynamic interactions.\n"
    text_augmented_prompt += "Pay attention to things like size, text, position, and color of all the elements, as well as the overall layout.\n"
    text_augmented_prompt += "Respond with the content of the HTML+CSS file (directly start with the code, do not add any additional explanation):\n"

    print("Generating html ...")
	## call GPT-4V
    html = gpt4v_call(img, text_augmented_prompt)

    print("Generated")

    return cleanup_response(html)

def adjustGenPrompt(origImg, genImg, genHtml, annotations, description):

    prompt = ""
    prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    prompt += "I have an HTML file for implementing a webpage but it has some missing or wrong elements that are different from the original webpage. The current implementation I have is:\n" + genHtml + "\n\n"
    prompt += "I will provide the reference webpage that I want to build as well as the rendered webpage of the current implementation.\n"

    if description:
        prompt += "Extra description: " + description + "\n"

    prompt += "Pay attention to things like size, text, position, and color of all the elements, as well as the overall layout. Blue boxes represent images and use \"rick.jpg\" as the placeholder.\n"
    prompt += "Respond directly with the content of the new revised and improved HTML file without any extra explanations:\n"

    print("Adjusting ...")

    annotations_prompt = "Find out all RED Rectangles on the Current Webpage. Each of them has their character name and represents one modification."
    annotations_prompt += "Each modification is only applied to the section within the rectangle. Do not change anything outside the rectangle."
    
    for annotation in annotations:
        annotations_prompt += "Rectangle " + annotation[0] + ": " + annotation[1] + "\n"

    html = gpt4v_call_adjust(origImg, genImg, prompt, annotations_prompt)

    print("Adjusted")

    return cleanup_response(html)

def selfRevisionPrompt(origImg, genImg, genHtml):
    

    ## Find the comparison between the current webpage and the reference page
    diff_prompt = ""
    diff_prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    diff_prompt += "Find out the difference between the current webpage and the reference page\n"
    diff_prompt += "The aim is to make the current webpage look exactly like the reference page.\n" 
    diff_prompt += "The difference is not limited to the size of the image, the position of the text and the color of the text"
    diff_prompt += "One line for each differenece. Only output the difference with out any explanation.\n"

    print("Revising ...")

    diff = gpt4v_call_adjust(origImg, genImg, diff_prompt)
    print(diff)

    prompt = ""
    prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    prompt += "I have an HTML file for implementing a webpage but it has some missing or wrong elements that are different from the original webpage. The current implementation I have is:\n" + genHtml + "\n\n"
    prompt += "The differences are included\n" + diff + "\n"
    prompt += "Make current webpage look exactly the same as the reference webpage. Make sure the code is syntactically correct and can render into a well-formed webpage. You can use \"rick.jpg\" as the placeholder image file.\n"
    prompt += "Pay attention to things like size, text, position, and color of all the elements, as well as the overall layout. Blue boxes represent images and use \"rick.jpg\" as the placeholder.\n"
    prompt += "Respond directly with the content of the new revised and improved HTML file without any extra explanations:\n"

    html = gpt4v_call_adjust(origImg, genImg, prompt)

    print("Revised")

    return cleanup_response(html)

def modifyGenPrompt(genImg, genHtml, annotations, description):
   
    prompt = ""
    prompt += "You are an expert web developer who specializes in HTML and CSS.\n"
    prompt += "The current html implementation I have is:\n" + genHtml + "\n\n"
    prompt += "Help me to correct the html code based on the ANNOTATIONS I provided below.\n"

    if description:
        prompt += "Extra description: " + description + "\n"

    prompt += "Respond directly with the content of the new revised and improved HTML file without any extra explanations:\n"

    print("Modifying ...")

    annotations_prompt = "Find out all RED Rectangles on the Current Webpage. Each of them has their character name and represents one modification."
    annotations_prompt += "Each modification only apply to the area within the rectangle. Do not change anything outside the rectangle."
    
    for annotation in annotations:
        annotations_prompt += "Rectangle " + annotation[0] + ": " + annotation[1] + "\n"
    html = gpt4v_call_modify(genImg, prompt, annotations_prompt)

    print("Modified")

    return cleanup_response(html)