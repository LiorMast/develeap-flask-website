FROM python:3.12-alpine as builder

WORKDIR /app
RUN python3 -m venv /opt/venv
COPY requirements.txt .
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

COPY templates ./templates
COPY chat.py .
RUN mkdir -p logs
EXPOSE 80 5000
VOLUME [ "/app/logs" ]

RUN adduser -D myuser
RUN chown -R myuser:myuser /app/logs
USER myuser

ENTRYPOINT ["python", "chat.py"]