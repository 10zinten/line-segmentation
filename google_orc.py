import io
from google.cloud import vision
from google.cloud.vision import types

vision_client = vision.ImageAnnotatorClient()
img_fn = 'data/book-097/page-051.png'

def text_annotations(fn):
    with io.open(img_fn, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)

    response = vision_client.document_text_detection(image=image)
    texts = response.text_annotations
    
    return texts[0].description.split('\n')

if __name__ == "__main__":

    texts = text_annotations(img_fn)
    print(texts)
    print("Number of Lines:", len(texts))
