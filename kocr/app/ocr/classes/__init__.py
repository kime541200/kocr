import os
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt, field_validator
from typing import Optional, Union, List, Tuple, Dict, Set
from numpy import ndarray
from PIL import Image, ImageDraw, ImageFont, ImageFile

from paddleocr import PaddleOCR

from kocr.app.ocr.classes.OcrEngineConfig import OcrEngineConfig
from kocr.app.ocr.utils.utils import is_image, is_pdf, image_to_ndarray, pdf_to_images, ndarray_to_image, image_to_base64, pdf_to_ndarrys


class OcrConfig(BaseModel):
    det: bool = Field(True, description='use text detection or not. If False, only rec will be exec. Default is True')
    rec: bool = Field(True, description='use text recognition or not. If False, only det will be exec. Default is True')
    cls: bool = Field(True, description='use angle classifier or not. Default is True. If True, the text with rotation of 180 degrees can be recognized. If no text is rotated by 180 degrees, use cls=False to get better performance. Text with rotation of 90 or 270 degrees can be recognized even if cls=False.')
    bin: bool = Field(False, description='binarize image to black and white. Default is False.')
    inv: bool = Field(False, description='invert image colors. Default is False.')
    alpha_color: Optional[Tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt]] = Field((255, 255, 255), description='set RGB color Tuple for transparent parts replacement. Default is pure white.')
    slice: Optional[Dict[str, PositiveInt]] = Field({}, description='use sliding window inference for large images, `det` and `rec` must be True. Requires int values for slice["horizontal_stride"], slice["vertical_stride"], slice["merge_x_thres"], slice["merge_y_thres], Default is {}. detail refer to https://paddlepaddle.github.io/PaddleOCR/ppocr/blog/slice.html')

    @field_validator('alpha_color')
    def check_alpha_color(cls, v):
        if len(v) != 3:
            raise ValueError(f'`alpha_color` only accept 3 int values between 0-255, got {v}.')
        for i in range(3):
            if not 0 <= v[i] <= 255:
                raise ValueError(f'`alpha_color` only accept the values between 0-255, got {v}.')
        return v
    
    @field_validator('slice')
    def check_slice(cls, v):
        for key in v.keys():
            if key not in ['horizontal_stride', 'vertical_stride', 'merge_x_thres', 'merge_y_thres']:
                raise ValueError(f"`slice`'s must be one of `['horizontal_stride', 'vertical_stride', 'merge_x_thres', 'merge_y_thres']`, got {v}")
        return v
    
class OcrResult(BaseModel):
    base64_img: str = Field(..., description='Baes64 encoding image')
    result: List[List[Tuple[List[List[float]], Tuple[str, float]]]] = Field(..., description='OCR result')