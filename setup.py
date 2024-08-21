from setuptools import setup, find_packages

setup(
    name="kocr",  # 專案名稱
    version="0.1.3",  # 專案版本
    author="Kim Chen",  # 作者名稱
    author_email="kime541200@outlook.com",  # 作者郵件
    description="Use to build server end-point and client end-point of OCR service.",  # 專案描述
    long_description=open("README.md").read(),  # 長描述 (從 README.md 中讀取)
    long_description_content_type="text/markdown",  # 長描述格式
    url="https://github.com/kime541200/kocr",  # 專案網址 (通常是 GitHub 頁面)
    packages=find_packages(),  # 自動找到所有的包
    install_requires=[  # 專案的依賴項
        "paddlepaddle-gpu",
        "paddleocr",
        "pdf2image",
        "rich",
        'python-multipart',
        "fastapi",
        "uvicorn",
        "pydantic",
        "opencv-python",
    ],
    classifiers=[  # 專案的分類標籤
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',  # 指定 Python 版本
)