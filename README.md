![image](https://github.com/user-attachments/assets/e98bd231-acfb-4bbd-88cf-8114430b9d95)# Trabalho Estrutura de Dados - Grupo 1
## Integrantes
* Bruna Machado Gravina - 1252221676
* Fabio Cunha de Abreu - 302210481
* Guilherme Del Rio - 321113402
* João Vitor Santos Santana - 823211842
* Matheus Loureiro de Albuquerque - 82116773

## Tecnologias utilizadas
* Python

## Preparando o ambiente
### 1. Instalação do Python
Caso o Python ainda não esteja instalado em sua máquina, você pode baixá-lo [AQUI](https://www.python.org/downloads).

### 2. Instalação do gerenciador de pacotes (PIP)
Para instalar o gerenciador de pacotes do Python, abra o terminal (CMD/Prompt de Comando) e execute o seguinte comando:

```
python -m ensurepip --upgrade
```

ou, caso esteja usando python3:

```
python3 -m ensurepip --upgrade
```

### 3. Configurando ambiente virtual (venv)
Após clonar o repositório e garantir que você está na branch main, siga os passos abaixo para configurar o ambiente virtual:

1. Navegue até o diretório do projeto e crie o ambiente virtual:

```
python3 -m venv venv
```

2. Ative o ambiente virtual (lembre-se de ativá-lo sempre que for rodar o projeto):
```
.\venv\Scripts\activate
```

3. Com o ambiente virtual ativo, instale as dependências necessárias:

* Instalar python-dotenv:
```
pip install python-dotenv
```

* Instalar requests:
```
pip install requests
```

### 4. Configurando arquivos json no código
Para rodar o projeto, no código Main.py, os caminhos de cada arquivo deve ser substituído no codigo, peço que copie o path de cada arquivo na pasta "Data" e subistitua no código, conforme print abaixo

![image](https://github.com/user-attachments/assets/7026c9fa-b8ec-4530-a5b4-891d84f0c612)

Para testar, sugiro que apague os dados do json de all_route, closest_routes e trucks_allocations para ver funcionando de fato, deixando somente o [], vazio.

1. Caminhos para os arquivos JSON

```
ORDER_PATH='substituir para caminho para o arquivo order.json dentro da pasta Data'
CD_PATH='substituir caminho para o arquivo distribution_center.json dentro da pasta Data'
ALL_ROUTES_PATH='substituir caminho para o arquivo all_routes.json dentro da pasta Data'
```
