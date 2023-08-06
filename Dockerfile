FROM python:3.11-slim

RUN apt-get update -y
RUN apt install libgl1-mesa-glx wget libglib2.0-0 -y

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

COPY . /app

CMD streamlit run --server.port 8080 --server.headless true --server.fileWatcherType none --browser.gatherUsageStats false app.py
