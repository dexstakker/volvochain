# syntax=docker/dockerfile:1
FROM python:3.8
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install wheel python-dotenv
CMD ["python", "./main.py"]