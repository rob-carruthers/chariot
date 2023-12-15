FROM --platform=linux/amd64 python:3.10.6-bullseye

COPY requirements.txt /requirements.txt
RUN pip install -U pip
RUN pip install -r /requirements.txt
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN python -m spacy download en_core_web_trf

COPY chariot /chariot

CMD uvicorn chariot.api:app --host 0.0.0.0 --port $PORT
