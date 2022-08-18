FROM python:3.9
WORKDIR /code
ARG app_id=1
COPY ./app${app_id}/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app${app_id} /code/app
COPY ./data /code/app/data
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]