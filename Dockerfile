FROM python:3.10

WORKDIR /opt/dvmn_homework_bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python", "./main.py"]