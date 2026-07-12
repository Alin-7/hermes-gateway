FROM nousresearch/hermes-agent:latest

# Copy configuration baseline to a readable shared location
COPY config.yaml /app/config.yaml

# Copy launcher wrapper
COPY run.py /app/run.py

EXPOSE 7860
ENV PORT=7860

CMD ["python", "/app/run.py"]
