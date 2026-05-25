import asyncio
import os
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from my_agent.agent import root_agent
from google.adk.agents.context import Context
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.run_config import RunConfig
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.sessions.session import Session

app = FastAPI(
    title="Build-with-AI-GDG Web Agent",
    description="Uma interface web simples para interagir com o agente AI do projeto.",
)

HTML_PAGE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Build-with-AI-GDG</title>
  <style>
    body { font-family: system-ui, sans-serif; background: #f5f7fb; color: #111827; margin: 0; padding: 0; }
    .container { max-width: 760px; margin: 3rem auto; padding: 2rem; background: #ffffff; border-radius: 16px; box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08); }
    h1 { margin-top: 0; }
    textarea { width: 100%; min-height: 120px; padding: 1rem; border: 1px solid #d1d5db; border-radius: 12px; font-size: 1rem; resize: vertical; }
    button { margin-top: 1rem; padding: 0.9rem 1.4rem; border: none; border-radius: 999px; background: #2563eb; color: white; font-size: 1rem; cursor: pointer; }
    button:disabled { background: #9ca3af; cursor: not-allowed; }
    .response { margin-top: 1.5rem; padding: 1.2rem; background: #eef2ff; border-radius: 12px; white-space: pre-wrap; }
    .footer { margin-top: 2rem; font-size: 0.95rem; color: #6b7280; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Build-with-AI-GDG</h1>
    <p>Use esta interface web para enviar perguntas ao agente AI configurado no projeto.</p>
    <textarea id="prompt" placeholder="Digite sua pergunta aqui..."></textarea>
    <button id="send">Enviar</button>
    <div id="result" class="response" style="display:none"></div>
    <div class="footer">Após iniciar o servidor, abra este app em <strong>http://127.0.0.1:8000</strong>.</div>
  </div>
  <script>
    const button = document.getElementById('send');
    const promptField = document.getElementById('prompt');
    const resultBox = document.getElementById('result');

    button.addEventListener('click', async () => {
      const prompt = promptField.value.trim();
      if (!prompt) return;
      button.disabled = true;
      resultBox.style.display = 'block';
      resultBox.textContent = 'Carregando...';

      try {
        const response = await fetch('/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: prompt }),
        });
        const data = await response.json();
        if (!response.ok) {
          resultBox.textContent = 'Erro: ' + (data.detail || JSON.stringify(data));
        } else {
          resultBox.textContent = data.answer || 'Nenhuma resposta recebida.';
        }
      } catch (error) {
        resultBox.textContent = 'Erro de rede: ' + error;
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
"""


@app.get('/', response_class=HTMLResponse)
async def home() -> HTMLResponse:
    return HTML_PAGE


async def invoke_agent(question: str) -> str:
    if not question.strip():
        raise ValueError('A pergunta não pode ficar vazia.')

    invocation_context = InvocationContext(
        session_service=InMemorySessionService(),
        invocation_id=str(uuid.uuid4()),
        session=Session(id=str(uuid.uuid4()), appName='Build-with-AI-GDG', userId='web_user'),
        run_config=RunConfig(response_modalities=['text']),
    )
    ctx = Context(invocation_context=invocation_context)

    answer = ''
    async for event in root_agent.run(ctx=ctx, node_input=question):
        output = getattr(event, 'output', None)
        if output is not None:
            answer = str(output)

    return answer or 'Sem resposta do agente.'


@app.post('/ask')
async def ask(request: Request):
    data = await request.json()
    question = data.get('question', '')
    if not question:
        raise HTTPException(status_code=400, detail='A pergunta não pode ficar vazia.')

    try:
        answer = await invoke_agent(question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {'question': question, 'answer': answer}


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok', 'agent': root_agent.name}
