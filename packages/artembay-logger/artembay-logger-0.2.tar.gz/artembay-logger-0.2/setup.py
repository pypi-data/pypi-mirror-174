from setuptools import setup, find_packages
from io import open


def read(filename):
   with open(filename, "r", encoding="utf-8") as file:
      return file.read()


setup(name="artembay-logger",
   version="0.2", # Версия твоего проекта. ВАЖНО: менять при каждом релизе
   description="Simple logger by Artem Bay",
   long_description=read("README.md"), # Здесь можно прописать README файл с длинным описанием
   long_description_content_type="text/markdown", # Тип контента, в нашем случае text/markdown
   author="Artem Bay",
   author_email="admin@artembay.site",
   url="https://pypi.org/project/artembay-logger/", # Страница проекта
   keywords="logger log print file debug", # Ключевые слова для упрощеннего поиска пакета на PyPi
   packages=find_packages() # Ищем пакеты, или можно передать название списком: ["package_name"]
)