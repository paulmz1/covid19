FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard_app ./dashboard_app

WORKDIR dashboard_app
CMD [ "python", "./main.py" ]