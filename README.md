# Aplicação blog - frontend + api + banco de dados




## Opção 1. (recomendado)
### Executando com Docker

Esta e a forma principal para subir a aplicacao.

1. Construir e iniciar os containers:

```bash
docker compose up --build
```

2. Acessar a aplicacao:

- Home HTML: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

3. Para parar os containers:

```bash
docker compose down
```
## Opção 2.
### Executando localmente com gerenciador de pacotes uv (alternativa)
Necessário ter o gerenciador de pacotes uv instalado.
uv é a versão moderna e mais rápida do pip

Use esta opcao se preferir rodar sem Docker.

1. Instalar dependencias:

```bash
uv sync
```

2. Iniciar o servidor FastAPI:

```bash
uv run fastapi dev --host 0.0.0.0 main.py
```

3. Acessar a aplicacao:

- Home HTML: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estrutura de rotas

As rotas estao divididas entre endpoints HTML (templates) e endpoints da API.

### Rotas HTML

| Metodo | Rota | Descricao |
|---|---|---|
| GET | / | Pagina inicial com lista de posts |
| GET | /posts | Alias da pagina inicial com lista de posts |
| GET | /posts/{id} | Pagina HTML de um post especifico |
| GET | /users/{user_id}/posts | Pagina HTML com posts de um usuario |

### Rotas da API - Posts

| Metodo | Rota | Descricao |
|---|---|---|
| GET | /api/posts | Lista todos os posts |
| POST | /api/posts | Cria um novo post |
| GET | /api/posts/{id} | Retorna um post especifico |
| PUT | /api/posts/{id} | Atualiza um post |
| DELETE | /api/posts/{id} | Remove um post |

Schema de criacao de post (POST /api/posts):

```json
{
	"title": "Titulo do post",
	"content": "Conteudo do post",
	"user_id": 1
}
```

Schema de atualizacao de post (PUT /api/posts/{id}):

```json
{
	"title": "Novo titulo",
	"content": "Novo conteudo"
}
```

### Rotas da API - Usuarios

| Metodo | Rota | Descricao |
|---|---|---|
| GET | /api/users | Lista todos os usuarios |
| POST | /api/users | Cria um novo usuario |
| GET | /api/users/{user_id} | Retorna um usuario especifico |
| PUT | /api/users/{id} | Atualiza informacoes do usuario |
| DELETE | /api/users/{id} | Remove um usuario |
| GET | /api/users/{user_id}/posts | Lista posts de um usuario |

Schema de criacao de usuario (POST /api/users):

```json
{
	"username": "johndoe",
	"email": "john@example.com"
}
```

Schema de atualizacao de usuario (PUT /api/users/{id}):

```json
{
	"image_file": "nome_arquivo.jpg"
}
```

## Tratamento de erros

- Rotas iniciadas com /api retornam erros em JSON.
- Rotas HTML retornam pagina de erro (template 404.html).
- Erros de validacao (422) seguem o comportamento acima, conforme tipo da rota.


