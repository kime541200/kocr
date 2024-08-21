
from pdf2image import convert_from_path
from kocr.app.ocr.classes import *
from kocr.app.ocr.classes.BaseOcrer import BaseOcrer

class PdfOcrer(BaseOcrer):
    def __init__(self,
                 ocr_engine_config: OcrEngineConfig = OcrEngineConfig(),
                 ):
        
        # 在子類的構造函數內部調用super().__init__來初始化基類的屬性，並在之後初始化子類特有的屬性。
        super().__init__(
            ocr_engine_config=ocr_engine_config
        )
    
    def _initialize_ocr_engine(self):
        return PaddleOCR(**self.ocr_engine_config)
    
    def _count_pages(self, pdf_path):
        images = convert_from_path(pdf_path)
        return len(images)
    
    def do_ocr(self, 
               file: Union[str, ndarray, Image.Image],
               config: OcrConfig = OcrConfig(), 
               verbose: bool = True, 
               specific_pages: List[int] = None
               ) -> List[OcrResult]:
        
        if (not isinstance(file, str)) or (not os.path.isfile(file)):
            raise ValueError(f'Please provide the path to the PDF file.')
        
        if is_pdf(file_path=file) == False:
                raise ValueError('Input file must be a PDF file.')
        
        page_amount = self._count_pages(file)
        if verbose == True:
            print(f'The PDF file total has {page_amount} pages.')
        if specific_pages is not None:
            for page in specific_pages:
                assert isinstance(page, int) and 0 < page <= page_amount, f"All values in specific_pages must be integers which is between [1-{page_amount}]."
            if verbose == True:
                print(f'Specific do OCR in these pages: {specific_pages}')
        else:
            specific_pages = list(range(1, page_amount + 1))
            
        pages:List[ndarray] = pdf_to_ndarrys(file)

        pages_ocr_results = []
        for page_id in specific_pages:
            if verbose == True:
                print(f'Do OCR in page {page_id}')
            
            img = pages[page_id - 1]

            ocr_results = self.ocr_engine.ocr(img,
                                            det=config.det,
                                            rec=config.rec,
                                            cls=config.cls,
                                            bin=config.bin,
                                            inv=config.inv,
                                            alpha_color=config.alpha_color,
                                            slice=config.slice)
            
            page_img = ndarray_to_image(np_image=img)
            base64_page_img = image_to_base64(image=page_img)

            pages_ocr_results.append(
                OcrResult(
                    base64_img=base64_page_img,
                    result=ocr_results)
                    )

        return pages_ocr_results