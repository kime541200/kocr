from kocr.app.ocr.classes import *
from kocr.app.ocr.classes.BaseOcrer import BaseOcrer

class ImageOcrer(BaseOcrer):
    def __init__(self,
                 ocr_engine_config: OcrEngineConfig = OcrEngineConfig()):
        
        # 在子類的構造函數內部調用super().__init__來初始化基類的屬性，並在之後初始化子類特有的屬性。
        super().__init__(
            ocr_engine_config=ocr_engine_config
        )
    
    def _initialize_ocr_engine(self):
        return PaddleOCR(**self.ocr_engine_config)
    
    def do_ocr(self, 
               file: Union[str, ndarray, Image.Image], 
               config: OcrConfig = OcrConfig(), 
               verbose: bool = False
               ) -> OcrResult:

        if isinstance(file, Image.Image):
            img = image_to_ndarray(image=file)
            ret_img = file
        elif isinstance(file, str):
            if is_image(file) == False:
                raise ValueError('Input file must be a image.')
            img = file
            ret_img = Image.open(file)
        else:
            img = file
            ret_img = ndarray_to_image(np_image=file)

        if len(config.slice) == 0:
            ocr_results = self.ocr_engine.ocr(img,
                                            det=config.det,
                                            rec=config.rec,
                                            cls=config.cls,
                                            bin=config.bin,
                                            inv=config.inv,
                                            alpha_color=config.alpha_color)
        else:
            ocr_results = self.ocr_engine.ocr(img,
                                            det=config.det,
                                            rec=config.rec,
                                            cls=config.cls,
                                            bin=config.bin,
                                            inv=config.inv,
                                            alpha_color=config.alpha_color,
                                            slice=config.slice)
        base64_img = image_to_base64(ret_img)

        return OcrResult(base64_img=base64_img, result=ocr_results)