FROM python:3.8-slim

RUN mkdir /frontend

COPY requirements.txt /frontend

WORKDIR /frontend

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /frontend

EXPOSE 8501

CMD ["dbus-uuidgen", "--ensure"]  # Ensuring dbus-uuidgen is executed

CMD ["streamlit", "run", "app.py"]