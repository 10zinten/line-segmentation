import io
from google.cloud import vision
from google.cloud.vision import types

vision_client = vision.ImageAnnotatorClient()

def text_annotations(fn):
    with io.open(fn, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)

    response = vision_client.document_text_detection(image=image)
    texts = response.text_annotations

    try:
        return texts[0].description
    except:
        return ""

    
if __name__ == "__main__":

    img_fn = 'data/book-097/page-051.png'
    texts = text_annotations(img_fn)
    print(texts)
    print("Number of Lines:", len(texts))
