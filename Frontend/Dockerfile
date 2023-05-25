FROM python:3.8-slim

RUN mkdir /frontend

COPY requirements.txt /frontend

WORKDIR /frontend

RUN apt-get update && apt-get install -y sudo

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . /frontend

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
