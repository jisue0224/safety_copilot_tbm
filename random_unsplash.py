import requests
from PIL import Image
import streamlit as st

def img_requests(txt):
    try:
        response = requests.get("https://source.unsplash.com/random/600*300/?{0}".format(txt))
        file = open('image.jpg', 'wb')
        file.write(response.content)
        img = Image.open(r"image.jpg")
        # img.show()
        file.close()
        return file.name, img.size[0], img.size[1]
    except:
        pass



if __name__ == "__main__":
    img = img_requests("family")
