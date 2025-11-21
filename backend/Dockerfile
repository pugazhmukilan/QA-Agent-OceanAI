FROM python:3.11-slim AS build 

WORKDIR /app
COPY requirement.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirement.txt


# RUN useradd -m user 
# USER user
# COPY --chown=user:user . .


# FROM python:3.11-slim 
COPY . .
FROM python:3.11-slim
COPY --from=build /app /app


CMD ["uvicorn", "app:app", "--host","0.0.0.0", "--port", "9000"]