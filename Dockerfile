FROM python:latest
RUN pip install CherryPy
WORKDIR /etc/scripts
COPY fizzbuzz.py .
RUN chmod +x fizzbuzz.py
CMD ["python", "./fizzbuzz.py", "-flag"]
