FROM python:3.11

ADD * .

RUN pip install requests 
RUN pip install beautifulsoup4
RUN pip install discord 
RUN pip install urllib3
RUN pip install python-dotenv
RUN pip install art

CMD ["python", "Kraked.py"]

