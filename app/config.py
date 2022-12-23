import logging
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgres://book_store_nkrjgr_user:sxjrGPGByXVQIM3wdLLKtuDk0Orfsdg1@dpg-ce12fio2i3mkuce8pm90-a.singapore-postgres.render.com/book_store_nkrjgr'
    PAGINATION_ITEMS: int = 25
    LOG_FILENAME: str = './fastapi.log'
    FORMAT: str = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t %(message)s \n"
    TIME_FORMAT:  str = "%d.%m.%Y %I:%M:%S %p"
    LOGGING_LEVEL = logging.DEBUG
    CORS_ORIGIN = ["192.168.99.112"]
    ALLOWED_HOSTS = ["192.168.99.112"]
