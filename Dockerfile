FROM python:3.9-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY dream_store/ /app

WORKDIR /app

CMD ["gunicorn", "dream_store.wsgi:application", "--bind", "0:8000" ] 
# CMD ["python3", "manage.py", "runserver", "0:8000"]
LABEL author="Alimov Rinat" email=r-alimov@ya.ru telegram=@Alimovriq