from .log_handler import get_logger
import settings

# 实例化日志模块

logger = get_logger(**settings.LOG_CONFIG)
