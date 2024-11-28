# ETAL 2024 Hackathon - Sistema de Análise de Geração de Energia

## 📋 Descrição

Sistema para análise e previsão de geração de energia, com funcionalidades de detecção de outliers, análise estatística e visualização de dados.

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Flask
- PostgreSQL
- SQLAlchemy
- Pandas
- Scikit-learn
- Docker

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose
- Python 3.x
- pip (gerenciador de pacotes Python)

### Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/vitorqf/etal-2024-hackathon.git
cd etal-2024-hackathon
```

2. Configure as variáveis de ambiente:

```bash
cd back
cp .env.example .env
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicie o banco de dados:

```bash
docker-compose up -d
```

5. Execute a aplicação:

```bash
cd back
python run.py
```

## 📡 API Endpoints

### Cidades

- `GET /cidades`

  - Retorna lista paginada de cidades
  - #### Parâmetros:
    - limit (int, default: 10)
    - offset (int, default: 0)
    - search (string)
    - region (string)

- `GET /cidades/{id_cidade}/usinas`

  - Retorna usinas da cidade específica
  - #### Parâmetros:
    - limit (int, default: 100)

- `GET /cidades/{id_usina}/historico`
  - Retorna histórico de geração da usina

## 📊 Scripts de Análise

### Análise de Depreciação

```bash
python depreciation.py
```

- Gera gráficos de análise de depreciação de usinas

### Limpeza e Análise de Dados

```bash
python clean.py
```

- Realiza detecção de outliers
- Gera visualizações estatísticas
- Treina modelo de previsão

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza PostgreSQL com as seguintes tabelas principais:

- cidade
- estado
- usina
- geracao
- unidade_consumidora

## 👥 Contribuição

1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/nome-da-feature`)
3. Commit suas mudanças (git commit -m 'Adicionando nova feature')
4. Push para a branch (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

## ⚠️ Observações

- Certifique-se de que as portas 5432 (PostgreSQL) e 5000 (Flask) estejam disponíveis
- Os dados sensíveis devem ser configurados no arquivo .env
- Recomenda-se o uso de ambiente virtual Python
