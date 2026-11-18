from io import BytesIO
from PIL import Image, ImageOps
from .config import settings

ALLOWED = {"JPEG", "PNG", "WEBP"}

def prepare_image(data: bytes):
    if not data:
        raise ValueError("Файл порожній.")
    if len(data) > settings.max_image_bytes:
        raise ValueError("Файл завеликий.")
    try:
        img = Image.open(BytesIO(data))
        img.verify()
        img = Image.open(BytesIO(data))
    except Exception as e:
        raise ValueError("Файл не є коректним зображенням.") from e
    if img.format not in ALLOWED:
        raise ValueError("Підтримуються JPEG, PNG та WEBP.")
    img = ImageOps.exif_transpose(img).convert("RGB")
    before = img.size
    img.thumbnail((settings.max_image_side, settings.max_image_side), Image.Resampling.LANCZOS)
    out = BytesIO()
    img.save(out, format="JPEG", quality=90, optimize=True)
    return out.getvalue(), before, img.size
