"""日志配置模块"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = "calculator", level: int = logging.INFO) -> logging.Logger:
    """
    配置并返回日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 禁止日志传播到父logger，避免重复输出
    logger.propagate = False
    
    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（可选）
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "calculator.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # 如果无法创建日志文件，仅使用控制台输出
        pass
    
    return logger


# 创建默认日志记录器
logger = setup_logger()
