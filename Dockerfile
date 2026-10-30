 Dockerfile for Industrial PLC Simulator
FROM python:3.9-slim

 Set working directory
WORKDIR /app

 Copy application files
COPY industrial_plc_simulator.py .
COPY README.md .
COPY LICENSE .

 Expose port
EXPOSE 8001

 Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/tags')" || exit 1

 Run the application
CMD ["python", "industrial_plc_simulator.py"]
