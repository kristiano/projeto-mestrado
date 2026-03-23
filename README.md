# Sistema de Personalização de Materiais Didáticos

**Projeto de Pesquisa – Mestrado em Ciência da Computação · UFMA · 2026**

Baseado em: Vaccaro et al. (2025), Troussas et al. (Entropy 2020), Felder-Silverman Learning Styles Model.

---

## Sumário

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Fluxo de Execução](#fluxo-de-execução)
4. [Módulos](#módulos)
5. [Dependências](#dependências)
6. [Configuração](#configuração)
7. [Como Executar](#como-executar)
8. [Estrutura de Arquivos](#estrutura-de-arquivos)
9. [Limitações e Observações](#limitações-e-observações)

---

## Visão Geral

Este sistema adapta automaticamente o conteúdo de uma disciplina universitária (fornecida em PDF) ao **perfil de aprendizagem individual do aluno**, com base no **Modelo de Estilos de Aprendizagem de Felder-Silverman**.

O fluxo completo é:

1. O usuário escolhe no terminal qual LLM prefere utilizar (GPT da OpenAI ou Gemini do Google).
2. O aluno responde a um **questionário** interativo de 4 perguntas.
3. A **IA** gera um perfil textual humanizado personalizado.
4. O sistema converte o **PDF da disciplina** em Markdown.
5. A LLM examina todo o texto e sugere **assuntos/tópicos** para o aluno estudar.
6. A IA **reescreve o conteúdo** adaptado com base em 16 prompts sistêmicos especializados para o perfil do aluno.
7. Um **PDF formatado** é gerado com o material personalizado.

---

## Arquitetura do Sistema

```
main.py
│
├─► llm_config.py          → Gerencia o roteamento dinâmico entre LLMs (GPT e Gemini)
├─► questionario.py        → Coleta as respostas e mapeia as dimensões Felder-Silverman
├─► profiler.py            → Gera o perfil textual do aluno via LLM
├─► leitor_pdf.py          → Extrai capítulos do PDF da disciplina e converte para Markdown
├─► seletor_conteudo.py    → Aciona a LLM para ler o Markdown, listar os assuntos e o aluno escolher
├─► prompts_adaptacao.py   → Fornece os 16 prompts dinâmicos baseados nas dimensões de Felder-Silverman
├─► rewrite.py             → Adapta o conteúdo ao perfil via LLM escolhida
├─► gerador_pdf.py         → Gera o PDF final formatado contendo capa, estilos e numeração
└─► gemini_config.py       → Configura a SDK do Gemini com retry automático
```

### Modelo de Estilos de Aprendizagem (Felder-Silverman)

| Dimensão       | Polo A         | Polo B        |
|----------------|----------------|---------------|
| Compreensão    | Sequencial     | Global        |
| Percepção      | Sensorial      | Intuitivo     |
| Entrada        | Visual         | Verbal        |
| Processamento  | Ativo          | Reflexivo     |

---

## Fluxo de Execução

```
[Início]
    │
    ▼
[Etapa 0 – Inicialização e Seleção da LLM]
    O usuário seleciona (a) GPT ou (b) GEMINI.
    O módulo llm_config.py define a provedora da sessão.
    │
    ▼
[Etapa 1 – Questionário]
    Coleta 4 respostas (a/b) → mapeia dimensões → exibe perfil inicial
    │
    ▼
[Etapa 1 – Profiler (LLM)]
    Gera descrição textual humanizada do perfil do aluno
    │
    ▼
[Etapa 2 – Leitura do PDF e Seleção do Assunto]
    Converte disciplina.pdf para conteudo.md
    LLM analisa o MD para sugerir assuntos (seletor_conteudo.py)
    Lista os capítulos/tópicos → aluno escolhe no terminal
    │
    ▼
[Etapa 2 – Adaptação (LLM e Prompts)]
    Identifica o prompt em prompts_adaptacao.py com base nos 4 polos mapeados
    Envia perfil + dimensões + texto original à LLM escolhida
    Recebe o conteúdo reescrito e personalizado
    │
    ▼
[Etapa 2 – Geração do PDF]
    Gera PDF formatado em materiais_gerados/material_<timestamp>.pdf
    │
    ▼
[Fim]
```

---

## Módulos

### `llm_config.py` – Roteamento de Modelos
Encapsula as chamadas de inicialização do GPT (`openai`) e do Gemini (`google-generativeai`), permitindo padronizar o retorno e realizar chamadas modulares. Centraliza qual IA está ativa na sessão corrente.

### `gemini_config.py` – Configuração Específica do Gemini
- Carrega a `GEMINI_API_KEY`.
- Descobre dinamicamente o modelo disponível que suporta `generateContent`.
- Aplica **retry automático** com backoff incremental.
- Expõe `QuotaExceededError`.

### `questionario.py` – Questionário de Aprendizagem
Aplica as perguntas no terminal; coleta e avalia as respostas a/b; converte as respostas das dimensões nos polos do FSLM.

### `profiler.py` – Gerador de Perfil
Usa a LLM escolhida para transformar as 4 dimensões em uma **descrição humanizada e personalizada** (3–4 frases).

### `leitor_pdf.py` – Leitura e Extração do PDF
Processa a extração de conteúdo nativo do `.pdf` limitando a quantidade de informação extraída desnecessariamente (cabeçalhos irritantes, etc) e transforma em log unificado `.md`.

### `seletor_conteudo.py` – Seleção Interativa de Tópicos (via LLM)
Aciona a IA para percorrer o `conteudo.md` gerado e fornecer uma lista formatada e estruturada de tópicos para o usuário escolher na CLI.

### `prompts_adaptacao.py` – Geração Dinâmica de 16 Prompts (FSLM)
Responsável por gerar (previamente) os 16 combinados possíveis do modelo Felder-Silverman. Assegura a fidelidade das sub-diretrizes para orientar a requisição final da API sobre como o material modificado deve se parecer em sintaxe Markdown.

### `rewrite.py` – Adaptação do Material (LLM)
Importa o dicionário com 16 prompts de `prompts_adaptacao.py`, seleciona o prompt que se opõe ao perfil detectado e envia todos esses conjuntos estáticos junto à fatia crua da matéria selecionada. Recebe um estofamento de Markdown transformado e pronto para uso.

### `gerador_pdf.py` – Geração do PDF Final
Classe estendida em **fpdf2**:
- Numeração automática, header, footer, capa estilizada e tratamento Unicode nativo com fonte DejaVu instalada no pacote `matplotlib`.

---

## Dependências

Instale com:

```bash
pip install -r requirements.txt
```

Principais pacotes:
- `google-generativeai` (SDK do Gemini)
- `openai` (SDK do GPT)
- `pdfplumber` (Leitura do PDF)
- `fpdf2` (Geração do PDF de saída)
- `python-dotenv` (Variáveis de ambiente)
- `matplotlib` (Apenas pelo caminho das fontes DejaVu, necessário no fpdf2)

---

## Configuração

### 1. Arquivo `.env`

Crie o arquivo `.env` na raiz do projeto com as suas chaves de API:

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 2. PDF da Disciplina

Coloque o PDF da disciplina na raiz do projeto com o nome:

```
disciplina.pdf
```

---

## Como Executar

```bash
cd /Users/skyneton/krf-docs/UFMA/MESTRADO\ COMPUTAÇÃO/2026/projeto
python main.py
```

O sistema irá guiá-arlo passo a passo: escolha do banco LLM que gerenciará o chat, questionário de estilo, extração das ementas do PDF via prompt, e finalmente gerará um ebook.

O arquivo PDF será salvo em:
```
materiais_gerados/material_YYYYMMDD_HHMMSS.pdf
```

---

## Estrutura de Arquivos

```
projeto/
│
├── main.py                  # Ponto de entrada (Inicialização e menu GPT/Gemini)
├── llm_config.py            # Roteamento e wrapper amigável OpenAI <=> Google AI
├── gemini_config.py         # Utils do Gemini (Retry e validação)
├── questionario.py          # Lógica do chat CLI de perguntas limitadas (FS)
├── profiler.py              # Consolida resposta e aciona LLM para humanizá-la
├── leitor_pdf.py            # Transforma as laudas de pdf em MD puro e cru
├── seletor_conteudo.py      # LLM lê o MD completo enumerando os tópicos extraídos para o usuário
├── prompts_adaptacao.py     # Base de conhecimento sistêmica dos 16 sub-prompts exclusivos (FSLM)
├── rewrite.py               # Requisita a IA aplicando o recorte técnico do material vs Perfil do aluno
├── gerador_pdf.py           # Processamento e montagem final das laudas formatadas em PDF
│
├── disciplina.pdf           # Documento de origem acadêmico
├── conteudo.md              # Artefato intermediário criado pela leitura
│
├── materiais_gerados/       # Onde os arquivos dinâmicos surgirão adaptados
│   └── material_*.pdf
│
├── .env                     # Variáveis de sistema e das chaves LLM
└── README.md                # Sumário central de arquitetura (você está aqui)
```

---

## Limitações e Observações

- **Cota da API Gemini (Free Tier):** O plano gratuito permite algumas dezenas de requisições por dia. O módulo `gemini_config.py` tem tratativas para reconexão; estourando os limites, você receberá erro.
- **Custos do GPT:** Caso use GPT (`openai`), certifique-se de ter créditos pré-pagos ou uma conta API ativa na OpenAI (os custos serão atrelados à conta do seu projeto baseado na chave API inserida).
- **Fontes DejaVu:** O projeto usa o `matplotlib` puro e simples para referenciar as fontes abertas no FPDF. Dependendo de como você tiver instalado seu Python env, os paths em `gerador_pdf.py` podem necessitar alteração!
