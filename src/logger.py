"""
This module handles all logging configurations.
It saves logs to PROJECT_ROOT/log/processing.log.
"""
import logging
import time
from logging import Logger
from pathlib import Path
from contextlib import contextmanager
from config import PROJECT_ROOT

# Define log directory and file path
LOG_DIR = Path(PROJECT_ROOT) / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger(name: str = "ImageProcessor") -> Logger | None:
    """
    Configures and returns a logger instance.
    Prevents duplicate handlers if called multiple times.
    """
    if name == "":
        print("logger name is empty")
        return
    logger = logging.getLogger(name)

    LOG_FILE = LOG_DIR / f"{name}__processing.log"
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # 1. File Handler (Saves logs to the file)
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 2. Console Handler (Prints logs to terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

@contextmanager
def log_runtime(description: str):
    if logger == None: return 
    """
    특정 코드 블록의 실행 시간을 측정하여 로그로 남깁니다.
    """
    start_time = time.perf_counter() # 고정밀 시간 측정 시작
    logger.info(f"[{description}] 작업을 시작합니다.")
    try:
        yield # with 블록 안의 코드가 실행되는 시점
    finally:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"[{description}] 완료 - 소요 시간: {elapsed_time:.2f}초")