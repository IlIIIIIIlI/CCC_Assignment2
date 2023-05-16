FROM python:3.8-slim

RUN mkdir /backend

COPY environment.txt /backend

WORKDIR /backend

RUN pip install -r environment.txt

COPY . /backend

EXPOSE 8000

# CMD ["backend", "run", "main.py"]

CMD ["python", "main.py"]
