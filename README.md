# Build-with-AI-GDG

Um projeto Python profissional para demonstrar um agente AI baseado em LLM, com ambiente virtual configurado e controle de versão Git.

## Visão Geral

Este repositório contém uma implementação inicial de um agente inteligente utilizando o Google ADK para agentes LLM. O projeto já foi estruturado com:

- Ambiente Python isolado em `.venv`
- Arquitetura de pacote Python em `my_agent/`
- Agente configurado em `my_agent/agent.py`
- Controle de versão Git com repositório remoto em `https://github.com/laizafernandes/Build-with-AI-GDG.git`

## Estrutura do Projeto

- `.venv/` - ambiente virtual Python local
- `my_agent/` - pacote Python principal
  - `agent.py` - definição do agente e configuração do modelo
  - `__init__.py` - inicialização do pacote
- `.gitignore` - arquivos e diretórios ignorados pelo Git
- `README.md` - documentação do projeto

## Agente AI

O agente principal é definido em `my_agent/agent.py` com a seguinte configuração básica:

- `model='gemini-2.5-flash'`
- `name='root_agent'`
- `description='A helpful assistant for user questions.'`
- `instruction='Answer user questions to the best of your knowledge'`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/laizafernandes/Build-with-AI-GDG.git
cd Build-with-AI-GDG
```

2. Ative o ambiente Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale dependências adicionais, se necessário:

```bash
pip install -r requirements.txt
```

> Se `requirements.txt` não existir, adicione as dependências do SDK AI e outras bibliotecas usadas pelo projeto.

## Uso

Execute ou importe o agente a partir do pacote `my_agent`:

```bash
source .venv/bin/activate
python -c "from my_agent.agent import root_agent; print(root_agent.description)"
```

### Interface web do agente

Uma interface web simples foi adicionada ao projeto em `app.py`.

1. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Defina sua chave de API do Google Gemini:

```bash
export GOOGLE_API_KEY="sua_chave_aqui"
```

4. Execute o servidor web:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

5. Abra no navegador:

```text
http://127.0.0.1:8000
```

A interface permite enviar perguntas diretamente para o agente e receber respostas em texto.

A partir daqui, você pode expandir o projeto para processar solicitações do usuário, integrar com APIs externas e construir fluxos de trabalho de assistente AI.

## Boas Práticas

- Mantenha a lógica do agente em `my_agent/`
- Use arquivos de configuração e variáveis de ambiente para credenciais
- Versione apenas o código-fonte e não inclua arquivos gerados localmente
- Atualize `README.md` conforme o projeto evolui

## Contribuição

1. Crie um branch a partir de `main`
2. Faça alterações significativas no código
3. Adicione testes ou documentação quando necessário
4. Faça um pull request para `main`

## Licença

Adicione uma licença adequada conforme sua preferência (por exemplo, MIT, Apache 2.0, GPL).