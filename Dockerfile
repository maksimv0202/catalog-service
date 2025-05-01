FROM python:3.12-slim

RUN apt-get update -y

ARG USERNAME=python
ARG UID=1005
ARG GID=2000

RUN groupadd -g "${GID}" ${USERNAME} && useradd --create-home -u "${UID}" -g "${GID}" ${USERNAME}

USER ${USERNAME}

WORKDIR /home/${USERNAME}/api

ENV PATH="$PATH:/home/${USERNAME}/.local/bin"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --chown=${USERNAME}:${USERNAME} requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=${USERNAME}:${USERNAME} ./src .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]