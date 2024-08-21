import os
from paddleocr import PaddleOCR
from rich import print as rprint
from typing import List,Tuple
from PIL import Image, ImageDraw, ImageFont

import numpy as np
from numpy import ndarray
from pdf2image import convert_from_path
import cv2

import base64
import io
from fastapi import FastAPI, HTTPException