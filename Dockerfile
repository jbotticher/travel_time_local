FROM python:3.9-slim-bookworm

WORKDIR /app

# COPY /app .
COPY . .

COPY requirements.txt .

ENV APP_ID=ed4953bf
ENV API_KEY=65b15716b757bccf8668bf3c04550682
ENV DATABASE_NAME=travel_time
ENV SERVER_NAME=postgres.cfaauq0oanzb.us-east-2.rds.amazonaws.com
ENV DB_USERNAME=postgres
ENV DB_PASSWORD=9234789JBdkinhtubKSJNIKNFD39287!!
ENV PORT=5432
ENV LOGGING_SERVER_NAME=postgres.cfaauq0oanzb.us-east-2.rds.amazonaws.com
ENV LOGGING_DATABASE_NAME=travel_time
ENV LOGGING_USERNAME=postgres
ENV LOGGING_PASSWORD=9234789JBdkinhtubKSJNIKNFD39287!!
ENV LOGGING_PORT=5432

RUN pip install -r requirements.txt

CMD ["python", "-m", "project.pipelines.travel_time"]