FROM python:3.11

WORKDIR /Groups_app

EXPOSE 5050

COPY Pipfile Pipfile.lock ./ 

RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "main.py"]