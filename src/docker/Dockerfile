FROM python:3.9.13

WORKDIR /usr/src/app

COPY ../requirements.txt ./
COPY ../app .
RUN pip install --no-cache-dir -r requirements.txt


ENV FLASK_APP=app.py

ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

CMD ["sh", "-c", "./start.sh"]