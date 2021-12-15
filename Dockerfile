FROM python:3.9

RUN pip install pipenv==2021.11.23

ENV PROJECT_DIR /usr/local/src/automation

WORKDIR ${PROJECT_DIR}

COPY . .

RUN pipenv install --system --deploy

ENTRYPOINT [ "python", "./main.py" ]
