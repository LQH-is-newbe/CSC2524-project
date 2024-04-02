from gpt4v import gpt4v_call

def initGenPrompt(img, description):
    with open('hello.html', 'r') as f:
        return f.read()

def adjustGenPrompt(origImg, genImg, genHtml, annotations, description):
    with open('hello.html', 'r') as f:
        return f.read()

def selfRevisionPrompt(origImg, genImg, genHtml):
    with open('hello.html', 'r') as f:
        return f.read()
    
def modifyGenPrompt(genImg, genHtml, annotations, description):
    with open('hello.html', 'r') as f:
        return f.read()