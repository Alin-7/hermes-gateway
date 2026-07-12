FROM nousresearch/hermes-agent:latest

# Zeabur 会自动识别 EXPOSE 的端口并生成公网域名
EXPOSE 7860
ENV PORT=7860

CMD ["gateway", "run"]
