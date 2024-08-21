import os
import json
from rich import print as rprint
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import base64
from PIL import Image
import io
from typing import List
from urllib.parse import urljoin
from pdf2image import convert_from_path
from numpy import ndarray

from kocr.app.ocr.classes import OcrConfig
from kocr.app.ocr.utils.utils import image_to_base64, is_pdf, pdf_to_images
from kocr.api_server import OcrImageData, OcrPdfData