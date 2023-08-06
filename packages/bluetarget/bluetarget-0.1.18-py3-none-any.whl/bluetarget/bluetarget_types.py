import docker

from enum import Enum


class Framework (Enum, str):
    huggingface = 'HUGGING_FACE'
    sklearn = 'SKLEARN'
    pytorch = 'PYTORCH'
    tensorflow = 'TENSORFLOW'
    xgboost = 'XGBOOST'


class Type (Enum, str):
    tabular = 'TABULAR'
    image = 'IMAGE'
    npl = 'NPL'
    other = 'OTHER'


class Implementation (Enum, str):
    py37 = 'py37'
    py38 = 'py38'
    py39 = 'py39'


class ModelType (Enum, str):
    tabular = 'TABULAR'
    image = 'IMAGE'
    npl = 'NPL'
    other = 'OTHER'


class Server(Enum, str):
    standard_micro = 'STANDARD_MICRO'
    standard_small = 'STANDARD_SMALL'
    standard_medium = 'STANDARD_MEDIUM'
    cpu_optimized_small = 'CPU_OPTIMIZED_SMALL'
    cpu_optimized_medium = 'CPU_OPTIMIZED_MEDIUM'
    cpu_optimized_large = 'CPU_OPTIMIZED_LARGE'
    gpu_optimized_xlarge = 'GPU_OPTIMIZED_XLARGE'
    gpu_optimized_2xlarge = 'GPU_OPTIMIZED_2XLARGE'
