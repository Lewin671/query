import logging

from config import LOGGER_URI

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 定义日志的文件，等级和格式
logging.basicConfig(filename=LOGGER_URI, level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger(__name__)

# 设置数据库提示的level
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
