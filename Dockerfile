FROM openjdk:slim
COPY --from=python:3-alpine / /

COPY generate_allure_report.py /generate_allure_report.py
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
