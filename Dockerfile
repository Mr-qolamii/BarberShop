FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend && cd /backend
WORKDIR /backend
COPY . .
RUN mkdir media
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

