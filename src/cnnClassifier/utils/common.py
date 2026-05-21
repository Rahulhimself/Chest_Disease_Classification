from importlib.resources import path
import os
from box.exceptions import BoxValueError
import yaml
from src.cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a yaml file and returns a config_box object.

    Args:
        path_to_yaml (Path): Path to the yaml file.
        """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError :
        raise ValueError("yaml file is invalid/invalid")
    except Exception as e:
        raise e
    
@ensure_annotations
def createt_directories(path_to_directories: list,verbose=True):
    """
    Creates a list of directories.

    Args:
        path_to_directories (list): List of directories to be created.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory: {path} created successfully")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves a dictionary as a json file.

    Args:
        path (Path): Path to the json file.
        data (dict): Dictionary to be saved as json.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a json file and returns a dictionary.

    Args:
        path (Path): Path to the json file.
    """

    with open(path) as f:
        content=json.load(f)
    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves a binary file.

    Args:
        data (Any): Data to be saved as binary.
        path (Path): Path to the binary file.
    """
    joblib.dump(value=data,filename=path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads a binary file and returns the data.

    Args:
        path (Path): Path to the binary file.
    """
    data=joblib.load(path)
    logger.info(f"binary file loaded successfully from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in KB.

    Args:
        path (Path): Path to the file.
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    logger.info(f"file: {path} has size: {size_in_kb} KB")
    return f"~ {size_in_kb} KB"

def decodeImage(imgstring,filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
    