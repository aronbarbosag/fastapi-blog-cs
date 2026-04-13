FROM python:3.12

WORKDIR /fastapi_blog
ENV PATH="/root/.local/bin:$PATH"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY . .

CMD ["uv","sync"]
CMD ["uv","run","fastapi","dev","--host","0.0.0.0","main.py"]
