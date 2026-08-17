FROM astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --all-groups --frozen

FROM python:3.14-slim-bookworm

COPY --from=builder .venv .venv
COPY ./src .

ENV PATH="/.venv/bin:$PATH"

CMD ["python", "main.py"]
