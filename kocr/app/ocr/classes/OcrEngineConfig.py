import os
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt, field_validator
from typing import Optional, Union, List, Tuple, Dict, Set

OCR_MODEL_ROOT=os.environ.get('OCR_MODEL_ROOT', os.getcwd())
DET_MODEL=os.environ.get('DET_MODEL', os.getcwd()+'/det')
REC_MODEL=os.environ.get('REC_MODEL', os.getcwd()+'/rec')
CLS_MODEL=os.environ.get('CLS_MODEL', os.getcwd()+'/cls')

class OcrEngineConfig(BaseModel):
    """
    這邊只寫了目前有用到的參數, 完整參數清單請參考 ./ref/paddleocr_params.txt
    """
    det_model_dir: str = Field(f"{OCR_MODEL_ROOT}{DET_MODEL}", description='path to detect model')
    rec_model_dir: str = Field(f"{OCR_MODEL_ROOT}{REC_MODEL}",description='path to  model recognition model')
    cls_model_dir: str = Field(f"{OCR_MODEL_ROOT}{CLS_MODEL}", description='path to classification model')
    use_angle_cls: bool = Field(True, description='whether to enable the angle classification model')
    use_gpu: Optional[NonNegativeInt] = Field(None, description='whether to user GPU, if want to use GPU, specific the GPU index here')
    lang: str = Field("en", description='language to detect')

    @field_validator('det_model_dir')
    def check_det_model_dir(cls, v):
        if not os.path.isdir(v):
            raise ValueError(f'`det_model_dir` must be a directory with detect model, fot {v}')
        return v
    
    @field_validator('rec_model_dir')
    def check_rec_model_dir(cls, v):
        if not os.path.isdir(v):
            raise ValueError(f'`rec_model_dir` must be a directory with recognition model, fot {v}')
        return v
    
    @field_validator('cls_model_dir')
    def check_cls_model_dir(cls, v):
        if not os.path.isdir(v):
            raise ValueError(f'`cls_model_dir` must be a directory with classification model, fot {v}')
        return v