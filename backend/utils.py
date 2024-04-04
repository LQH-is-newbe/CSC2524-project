from playwright.sync_api import sync_playwright
import os
import cv2

def takeScreenshot(url):
    outputFile = url.replace('.html', '.png')
    if os.path.exists(url):
        url = "file://" + os.path.abspath(url)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.screenshot(
            path=outputFile, full_page=True, animations="disabled", timeout=60000
        )
        browser.close()

def drawText(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          fontScale=3,
          fontThickness=2,
          textColor=(0, 0, 0),
          textColorBg=(0, 0, 255)
          ):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, fontScale, fontThickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), textColorBg, -1)
    cv2.putText(img, text, (x, y + text_h + fontScale - 1), font, fontScale, textColor, fontThickness)

def annotateImage(imgPath, annotations):
    outputPath = imgPath[:-4] + '_annotated.png'
    img = cv2.imread(imgPath)
    for i, annotation in enumerate(annotations):
        left, top, width, height = annotation['left'],annotation['top'], annotation['width'], annotation['height']
        cv2.rectangle(img,(left, top),(left + width, top + height),(0,0,255),2)
        drawText(img, chr(ord('A')+i), pos=(left, top))
    cv2.imwrite(outputPath, img)

def cleanup_response(response):
    ## simple post-processing
    if response[ : 3] == "```":
        response = response[3 :].strip()
    if response[-3 : ] == "```":
        response = response[ : -3].strip()
    if response[ : 4] == "html":
        response = response[4 : ].strip()

    ## strip anything before '<!DOCTYPE'
    if '<!DOCTYPE' in response:
        response = response.split('<!DOCTYPE', 1)[1]
        response = '<!DOCTYPE' + response
		
    ## strip anything after '</html>'
    if '</html>' in response:
        response = response.split('</html>')[0] + '</html>'

    return response 