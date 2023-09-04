FROM python:3.11

ENV BOT_URL='http://bot_api:3001'

WORKDIR /Groups_app

EXPOSE 5050

COPY Pipfile Pipfile.lock ./ 

RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . ./

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5050"]