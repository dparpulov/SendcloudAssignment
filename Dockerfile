FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./scraper /app
COPY ./scraper/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]