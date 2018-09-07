FROM python:3.6-slim-stretch

RUN pip install --upgrade pip
RUN pip install pipenv

RUN pipenv install --system --deploy

ENTRYPOINT ["python"]