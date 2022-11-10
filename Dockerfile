FROM python:3.8.0

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "manage.py", "runserver" ]