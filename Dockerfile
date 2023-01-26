FROM python:3
ADD main.py /
COPY requirements.txt /tmp/requirements.txt
COPY / /
RUN pip3 install -r /tmp/requirements.txt
CMD ["python", "./main.py"]