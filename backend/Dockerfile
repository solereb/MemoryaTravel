FROM python:3.10-slim

WORKDIR /app

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]