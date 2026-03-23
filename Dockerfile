FROM python:3.10-slim

WORKDIR /app

ARG RUN_ID=unknown

RUN echo "Preparing image for MLflow Run ID: ${RUN_ID}" \
	&& echo "Downloading model for Run ID: ${RUN_ID} (mock)"

CMD ["sh", "-c", "echo 'Container ready for Run ID: ${RUN_ID}'"]
