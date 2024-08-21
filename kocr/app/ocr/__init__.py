from paddleocr import PaddleOCR
from rich import print as rprint
from typing import List,Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFile

import numpy as np
from numpy import ndarray
from pdf2image import convert_from_path

from kocr.app.ocr.utils.utils import draw_text_box, ndarray_to_image, pdf_to_images