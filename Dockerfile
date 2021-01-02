FROM python:3.7.2-stretch

WORKDIR /app

RUN pip install --upgrade pip

RUN python -m pip install mysql-connector flask

COPY main.py /app

CMD python main.py
