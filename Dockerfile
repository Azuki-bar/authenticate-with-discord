FROM python:3.10-slim as base
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 


FROM base AS runner
RUN pip install discord.py pyotp
COPY ./main.py .
CMD ["python", "main.py"]

