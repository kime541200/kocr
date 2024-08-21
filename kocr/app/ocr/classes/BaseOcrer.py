from kocr.app.ocr.classes import *

class BaseOcrer(ABC):
    def __init__(self,
                 ocr_engine_config: OcrEngineConfig = OcrEngineConfig()):
        
        self.ocr_engine_config = ocr_engine_config.model_dump()
        self.ocr_engine = self._initialize_ocr_engine()
    
    def _initialize_ocr_engine(self):
        return PaddleOCR(**self.ocr_engine_config)
    
    @abstractmethod
    def do_ocr(self, file: Union[str, ndarray, Image.Image], config: OcrConfig = OcrConfig(), verbose: bool = False):
        pass