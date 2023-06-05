import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Configuration:
    USER: str
    PASSWORD: str               
    FLASK_APP: str
    FLASK_DEBUG: str
    SECRET_KEY: str


config = Configuration(
    USER=os.getenv("user"),
    PASSWORD=os.getenv('password'),
    FLASK_APP=os.getenv('FLASK_APP'),
    FLASK_DEBUG=os.getenv('FLASK_DEBUG'),
    SECRET_KEY=os.getenv('SECRET_KEY')                                      
)
