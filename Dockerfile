FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV NAME stranded
EXPOSE 80
cmd ["python", "main.py"]
