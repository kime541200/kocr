from kocr.app.client.classes import *

class OcrClient():
    def __init__(self,
                 host: str):
        
        self.host = host

    def send_image(self, img_base64: str, config: OcrConfig = OcrConfig()):
        """傳送影像到伺服器

        此函數將傳入的PIL影像物件轉換為Base64編碼, 然後將其作為JSON資料傳送到指定的URL。

        Args:
            img_base64 (str): 要傳送的影像的base64編碼
            config (OcrConfig): 執行OCR時的參數設定

        Returns:
            requests.Response: HTTP回應對象, 如果請求失敗則傳回None
        """
        
        try:
            # 建立JSON格式的請求體
            payload = {
                "base64_image_data": img_base64,
                "config": config.model_dump()
                } 
            
            # 設定HTTP頭，宣告內容類型為JSON
            headers = {'Content-Type': 'application/json'}

            server_url = urljoin(self.host, 'image')
        
            response = requests.post(url=server_url, json=payload, headers=headers) # 發送POST請求到指定URL
            return response # 回傳伺服器回應
        except Exception as e:
            print(f"Error happend when send image to server: {e}") # 列印錯誤訊息
            return None # 如果發生錯誤，回傳None
    
    
    def _count_pages(self, pdf_path):
        images = convert_from_path(pdf_path)
        return len(images)
    

    def send_pdf(self, pdf_path: str, config: OcrConfig = OcrConfig(), specific_pages: List[int] = None):
        if (not isinstance(pdf_path, str)) or (not os.path.isfile(pdf_path)):
            raise ValueError(f'Please provide the path to the PDF file.')
        
        if is_pdf(file_path=pdf_path) == False:
                raise ValueError('Input file must be a PDF file.')
        
        page_amount = self._count_pages(pdf_path)
        print(f'The PDF file total has {page_amount} pages.')

        if specific_pages != None:
            for page in specific_pages:
                assert isinstance(page, int) and 0 < page <= page_amount, f"All values in specific_pages must be integers which is between [1-{page_amount}]."
            print(f'Specific do OCR in these pages: {specific_pages}')
        else:
            specific_pages = list(range(1, page_amount + 1))
            
        pages:List[Image.Image] = pdf_to_images(pdf_path)
        
        pdf_data=[]
        for i, page in enumerate(pages):
            if (i + 1) in specific_pages:
                img_base64 = image_to_base64(image=page)
                data = {
                    "base64_image_data": img_base64,
                    "config": config.model_dump()
                    }
                page_data = OcrImageData(**data)
                pdf_data.append(page_data)

        ocr_pdf_data = OcrPdfData(pdf_data=pdf_data)
        
        # 設定HTTP頭，宣告內容類型為JSON
        headers = {'Content-Type': 'application/json'}

        server_url = urljoin(self.host, 'pdf')

        with requests.post(url=server_url, json=ocr_pdf_data.model_dump(), headers=headers, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        yield json.loads(line)
            else:
                print(f"Error: Received status code {response.status_code}")
                yield {"error": f"Received status code {response.status_code}"}