FROM python:3.6
WORKDIR /api
ENV FLASK_APP api.py
ENV FLASK_RUN_HOST 0.0.0.0
ADD api.py requirements.txt /api/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]