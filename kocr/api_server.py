import os
import logging
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import requests
import base64
from PIL import Image
import io
from contextlib import asynccontextmanager
from typing import List
from rich import print as rprint

from kocr.app.ocr.classes import OcrConfig
from kocr.app.ocr.classes import OcrEngineConfig
from kocr.app.ocr.classes.ImageOcrer import ImageOcrer
from kocr.app.ocr.classes.PdfOcrer import PdfOcrer
from kocr.app.ocr.utils.utils import decode_base64_image

# 定義接收圖片的JSON數據模型
class OcrImageData(BaseModel):
    base64_image_data: str
    config: OcrConfig

class OcrPdfData(BaseModel):
    pdf_data: List[OcrImageData]


PORT = int(os.environ.get('OCR_PORT', '8868'))


# Initial logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Execute when start the service
    global image_ocrer
    try:
        image_ocrer = ImageOcrer()

        logger.info("Initial done")
    except Exception as ex:
        logger.error(f"Initial fail, {ex}")
        raise

    yield

    # execute when closing
    logger.info("Closing...")

app = FastAPI(lifespan=lifespan)

# 伺服器端點, 用於接收Base64編碼影像
@app.post("/image")
async def ocr_image(data: OcrImageData):
    try:
        image = decode_base64_image(data.base64_image_data)
        config = data.config
        result = image_ocrer.do_ocr(file=image, config=config)

    except Exception as ex:
       logger.error(f"Failed to decode base64 image: {ex}")
       raise HTTPException(status_code=500, detail="Invalid image data")

    return JSONResponse(content=result.model_dump())

@app.post("/pdf")
async def ocr_pdf(data: OcrPdfData):
    async def ocr_generator():
        for image_data in data.pdf_data:
            try:
                image = decode_base64_image(image_data.base64_image_data)
                config = image_data.config
                result = image_ocrer.do_ocr(file=image, config=config)
                yield json.dumps(result.model_dump()) + "\n"
            except Exception as ex:
                logger.error(f"Failed to process image: {ex}")
                yield json.dumps({"error": str(ex)}) + "\n"

    return StreamingResponse(ocr_generator(), media_type="application/x-ndjson")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)