import os
from pathlib import Path
import logging


project_name="researchSummarizer"


logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:%(message)s:')

list_of_files = [
    ".github/workflows/.gitkeep",
    f"{project_name}/app/__init__.py",
    f"{project_name}/app/main.py",
    f"{project_name}/app/api/__init__.py",
    f"{project_name}/app/api/routes.py",
    f"{project_name}/app/services/extractor.py",
    f"{project_name}/app/models/hf_client.py",
    "requirements.txt",
    "tests/test_health.py",
    "setup.py",
    "notebooks/model_prototype.ipynb",
    "docker/Dockerfile",
]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory:{filedir} for  the file {filename}")
    
    if(not os.path.exists(filepath)) or(os.path.getsize(filepath)==0):
        with open(filepath,'w')as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")        
