<h1>pip command</h1>
<h2>Библиотека для выполнения команд pip</h2>

***
<h2>Установка</h2>

    pip install pip_command
***


<h3>install | installs | install_requirements</h3>

 * install - установка библиотеки
 * installs - установка нескольких библиотек
 * install_requirements - установка requirements.txt
```python
from pip_command import install, installs, install_requirements

install("requests", version="2.25.1")  # установка библиотеки requests
installs("requests", "bs4")  # установка библиотек requests и bs4
install_requirements("requirements.txt")  # установка библиотек из файла requirements.txt
```
