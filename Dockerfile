# base python
FROM python:2.7

# add requirements and install
ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
