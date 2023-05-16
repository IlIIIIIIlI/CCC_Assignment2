FROM python:3.8-slim

RUN mkdir /Backend

COPY environment.txt /Backend

WORKDIR /Backend

RUN pip install -r environment.txt

COPY . /Backend

EXPOSE 8000

CMD ["Backend", "run", "main.py"]