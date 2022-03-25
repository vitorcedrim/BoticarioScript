import requests as re

url = f'https://docs.google.com/spreadsheets/d/e/2PACX-1vS-r3TsvVzpM0LScbenDYHyGnquWSJEJ863fxzyYQdpuHkDfEcSQHmgocDgbq5Att41oX8oDLTQQxwy/pub?gid=1879265991&single=true&output=csv'
data = re.get(url)

open('2022.csv', 'wb').write(data.content)