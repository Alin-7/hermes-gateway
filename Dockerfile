FROM nousresearch/hermes-agent:latest

# Copy configuration baseline
COPY config.yaml /root/.hermes/config.yaml

# Copy launcher wrapper
COPY run.py /run.py

EXPOSE 7860
ENV PORT=7860

CMD ["python", "/run.py"]
