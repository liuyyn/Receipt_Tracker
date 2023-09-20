import io
import base64
from PIL import Image

def compress_image(base64_str):
    buffer = io.BytesIO()
    imgdata = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(imgdata))
    new_img = img.resize((400, 1000))  # x, y
    new_img.save(buffer, format="PNG")
    new_img.save("test.png", format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue())
    return {"compressed_img": str(img_b64)[2:-1], "png_image": buffer.getvalue()}