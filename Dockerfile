FROM python:3.9-slim-bookworm

WORKDIR /code

COPY . /code/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


CMD ["fastapi", "run", "main.py", "--port", "80"]