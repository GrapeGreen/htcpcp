FROM python:3
EXPOSE 65432
ADD server.py /
ADD pot.py /
ADD parser.py /
ADD test.py /
ENTRYPOINT ["python3", "server.py"]
