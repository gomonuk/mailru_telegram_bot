## mailru_telegram_bot

#### tldr

`docker pull gomonuk/calcbot:latest && docker run --env TG_BOT_TOKEN=12345 gomonuk/calcbot:latest`

#### Что сделано хорошо:

- ci на гитхабе
- cd на хироку
- coverage 99% (`coverage run --omit 'venv/*'  -m pytest && coverage report -m`)

#### Что сделано плохо:

- работает только с числами от 0 до 9 - сознательно забил, это парсинг, на алгоритм не влияет
- тесты не содержат достаточного количества граничных значений - решил что для тестового сойдет