FROM alpine:latest

RUN apk --no-cache add py3-flask

RUN mkdir -p /schort/data
ADD run.py schort.py /schort/
ADD static/ /schort/static/
ADD templates/ /schort/templates/
RUN chmod +x /schort/run.py

ENTRYPOINT ["/schort/run.py"]

