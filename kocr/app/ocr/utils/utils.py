from kocr.app.ocr.utils import *

def draw_text_box(img: Image.Image, ocr_results: List[List[Tuple[List[List[float]], Tuple[str, float]]]]):
    """
    在圖片上繪製文字方框和文字內容，包括文字和其信心度。

    Args:
        image_path (str): 圖片檔案路徑。
        ocr_results (List[List[Tuple[List[List[float]], Tuple[str, float]]]]): OCR辨識結果，包含文字方框座標和文字內容。
    """

    draw = ImageDraw.Draw(img)

    def interpolate_color(confidence: float) -> Tuple[int, int, int]:
        """
        分數越高會越接近綠色, 越低則越接近紅色
        """
        r = int(255 * (1 - confidence))
        g = int(255 * confidence)
        return (r, g, 0)

    # 迭代每個OCR辨識結果
    for result_list in ocr_results:
        # 迭代每個文字方框和文字內容
        for coordinates, (text, confidence) in result_list:
            # 將座標展平成一維列表
            flat_coordinates = []
            for point in coordinates:
                for coord in point:
                    flat_coordinates.append(coord)

            color = interpolate_color(confidence)

            # 繪製文字方框
            draw.polygon(flat_coordinates, outline=color, width=2)

            # 計算文字位置
            x_min = min(coord[0] for coord in coordinates)
            y_min = min(coord[1] for coord in coordinates)

            # 設定字型（確保字型檔案存在，否則使用預設字型）
            font_size = 20
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()

            # 繪製文字內容和信心度（紅色）
            text_with_confidence = f"{text} ({confidence:.2f})"
            draw.text((x_min, y_min - font_size), text_with_confidence, fill=color, font=font)

    # 顯示圖片
    img.show()


def pdf_to_ndarrys(pdf_path) -> List[ndarray]:
    # 將PDF轉換為圖像(ndarray)
    pages = convert_from_path(pdf_path)
    
    # 創建一個列表來存儲ndarray格式的圖像
    image_list = []
    
    # 將每一頁轉換為ndarray並添加到列表中
    for page in pages:
        # 將PIL Image轉換為numpy數組
        np_image = image_to_ndarray(image=page)
        image_list.append(np_image)
    
    return image_list

def pdf_to_images(pdf_path) -> List[Image.Image]:
    # 將PDF轉換為圖像
    pages = convert_from_path(pdf_path)
    
    return pages


def ndarray_to_image(np_image:ndarray) -> Image.Image:
    return Image.fromarray(np_image)


def image_to_ndarray(image:Image.Image) -> ndarray:
    return np.array(image)


def ndarray_to_base64(arr: np.ndarray) -> str:
   _, encoded = cv2.imencode('.png', arr)
   base64_str = base64.b64encode(encoded).decode('utf-8')
   return base64_str


def image_to_base64(image: Image.Image, format: str = "JPEG", encoding: str='utf-8') -> str:
   """將Image影像轉換為Base64編碼

   Args:
       image (Image.Image): 一個PIL圖像對象
       format (str, optional): 保存圖像的格式，可以是'JPEG', 'PNG', 'GIF'等。預設為'JPEG'
       encoding (str, optional): 編碼字符串的方式，預設為'utf-8'

   Returns:
       str: Base64編碼後的字符串
   """
   buffered = io.BytesIO()
   image.save(buffered, format=format)  # 根據需要選擇合適的格式
   img_str = base64.b64encode(buffered.getvalue()).decode(encoding)
   return img_str


def decode_base64_image(base64_str: str) -> Image.Image:
   """將Base64編碼的圖像數據解碼為PIL圖像對象

   Args:
       base64_str (str): Base64編碼的字符串表示的圖像數據

   Raises:
       Exception: 如果輸入的Base64字符串無法解碼為有效的圖像, 將會拋出這個異常, 並附帶錯誤信息"Invalid image data"

   Returns:
       Image.Image: 解碼後的PIL圖像對象
   """
   try:
       image_data = base64.b64decode(base64_str)
       image = Image.open(io.BytesIO(image_data))
       return image
   except Exception as e:
       raise Exception("Invalid image data")


def is_image(file_path: str) -> bool:
   """
   檢查給定文件路徑是否指向一個圖像文件

   參數：
       file_path (str): 文件的路徑

   返回：
       bool: 如果文件是圖像，則返回 True, 否則返回 False
   """
   if not os.path.isfile(file_path):
       return False
   try:
       with Image.open(file_path) as img:
           img.verify()  # 驗證圖像文件的完整性
       return True
   except (IOError, SyntaxError):
       return False


def is_pdf(file_path: str) -> bool:
   """
   檢查文件是否為PDF格式

   參數:
       file_path (str): 文件的路徑

   返回:
       bool: True如果文件是PDF, 否則False
   """
   if not os.path.isfile(file_path):
       return False
   _, extension = os.path.splitext(file_path)
   return extension.lower() == '.pdf'

