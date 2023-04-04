FROM python:3.10
COPY requirements.txt /opt/dvmn_homework_bot/requirements.txt
WORKDIR /opt/dvmn_homework_bot
RUN pip3 install -r requirements.txt
COPY . /opt/dvmn_homework_bot/
CMD ["python", "./main.py"]