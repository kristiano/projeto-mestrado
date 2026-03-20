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

1. O aluno responde a um **questionário** de 4 perguntas.
2. A **IA (Gemini)** gera um perfil textual personalizado.
3. O sistema lê e extrai capítulos do **PDF da disciplina**.
4. O aluno escolhe o **assunto** que deseja estudar.
5. A IA **reescreve o conteúdo** adaptado ao perfil do aluno.
6. Um **PDF formatado** é gerado com o material personalizado.

---

## Arquitetura do Sistema

```
main.py
│
├─► questionario.py      → Coleta as respostas e mapeia as dimensões
├─► profiler.py          → Gera o perfil textual do aluno via LLM
├─► leitor_pdf.py        → Extrai capítulos do PDF da disciplina
├─► assuntos_llm.py      → Fallback: usa LLM para sugerir tópicos
├─► seletor_conteudo.py  → Permite ao aluno escolher o capítulo
├─► rewrite.py           → Adapta o conteúdo ao perfil via LLM
├─► gerador_pdf.py       → Gera o PDF final formatado
└─► gemini_config.py     → Configura a SDK do Gemini com retry automático
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
[Etapa 1 – Questionário]
    Coleta 4 respostas (a/b) → mapeia dimensões → exibe perfil inicial
    │
    ▼
[Etapa 1 – Profiler (LLM)]
    Gera descrição textual humanizada do perfil do aluno
    │
    ▼
[Etapa 2 – Leitura do PDF]
    Tenta extrair capítulos via sumário numerado
    Se falhar → tenta via cabeçalhos "CAPÍTULO X"
    Se ainda falhar → chama LLM para sugerir tópicos (assuntos_llm.py)
    │
    ▼
[Etapa 2 – Seleção do Assunto]
    Lista os capítulos/tópicos → aluno escolhe
    Salva conteúdo bruto em conteudo.md
    │
    ▼
[Etapa 2 – Adaptação (LLM)]
    Envia perfil + dimensões + texto original à LLM
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

### `gemini_config.py` – Configuração do Gemini

Responsável por:
- Carregar a `GEMINI_API_KEY` do arquivo `.env`
- Descobrir dinamicamente o modelo disponível que suporta `generateContent`
- Aplicar **retry automático** com backoff incremental (15 s, 30 s, 45 s) em caso de cota excedida
- Expor `QuotaExceededError` para tratamento externo

**Funções públicas:**

| Função / Classe       | Descrição |
|-----------------------|-----------|
| `criar_modelo(system_instruction)` | Configura o Gemini e retorna um `GenerativeModel` pronto para uso |
| `QuotaExceededError`  | Exceção lançada após esgotar todas as tentativas de retry |

---

### `questionario.py` – Questionário de Estilos de Aprendizagem

Aplica 4 perguntas (uma por dimensão do modelo Felder-Silverman) em modo interativo no terminal.

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `aplicar_questionario()` | Exibe perguntas e coleta respostas `a`/`b`. Retorna dict `{dimensao: resposta}` |
| `mapear_dimensoes(respostas)` | Converte respostas em rótulos textuais (ex.: `"Sequencial"`, `"Visual"`) |
| `exibir_resultado(dimensoes)` | Exibe o resultado formatado no terminal |

---

### `profiler.py` – Gerador de Perfil

Usa a LLM para transformar as 4 dimensões em uma **descrição humanizada e personalizada** do perfil do aluno (3–4 frases).

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `get_student_profile(respostas, dimensoes)` | Retorna string com o perfil de aprendizagem gerado pela LLM |

Em caso de cota esgotada (`QuotaExceededError`), retorna uma mensagem de fallback e **não interrompe** o programa.

---

### `leitor_pdf.py` – Leitura e Extração do PDF

Extrai os capítulos do PDF da disciplina usando **três estratégias em cascata**:

1. **Sumário numerado** — detecta a seção "Sumário" e extrai capítulos do tipo `N Título ... pág`.
2. **Cabeçalhos CAPÍTULO X** — percorre o corpo do PDF buscando padrão regex.
3. **Fallback via LLM** (delegado a `assuntos_llm.py`) — caso as estratégias anteriores falhem.

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `extrair_texto_pagina(pagina)` | Extrai texto de uma página filtrando rodapés |
| `extrair_capitulos_do_sumario(texto_sumario)` | Parseia a lista de capítulos do sumário |
| `extrair_conteudo_capitulos(caminho_pdf)` | Retorna `dict {título_do_capítulo: texto}` |

---

### `assuntos_llm.py` – Identificação de Tópicos via LLM

**Fallback** usado quando o PDF não possui sumário ou cabeçalhos identificáveis.

Estratégia:
1. Extrai amostra textual do PDF (até 40 páginas, 12 linhas/página, max 12.000 chars).
2. Envia à LLM para sugestão de 3–8 tópicos em formato JSON.
3. O aluno escolhe o tópico.
4. Extrai do PDF as páginas que contêm as palavras-chave do tópico.

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `localizar_assunto_com_llm(caminho_pdf)` | Retorna `(titulo, texto)` ou `None` em caso de falha/cancelamento |

---

### `seletor_conteudo.py` – Seleção Interativa do Capítulo

Exibe a lista de capítulos extraídos e permite ao aluno escolher um pelo número.

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `selecionar_assunto(capitulos)` | Retorna `(nome_do_capitulo, texto_do_capitulo)` |

---

### `rewrite.py` – Adaptação do Material (LLM)

Reescreve o conteúdo original do capítulo respeitando as diretrizes de cada dimensão do modelo Felder-Silverman. O texto gerado mantém precisão e completude, com estrutura organizada (títulos, subtítulos, resumo final).

Envia ao modelo:
- O perfil textual do aluno
- As 4 dimensões mapeadas
- O trecho do capítulo (limitado a 8.000 chars)

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `adaptar_material(perfil, dimensoes, assunto, texto)` | Retorna o conteúdo adaptado como string Markdown |

---

### `gerador_pdf.py` – Geração do PDF Final

Gera um PDF formatado usando **fpdf2** com fonte DejaVu (suporte completo ao português).

Recursos do PDF:
- **Capa** com título do assunto e perfil do aluno destacado
- **Cabeçalho e rodapé** com numeração de páginas
- Suporte a Markdown: `#`, `##`, `###`, listas (`-`, `*`, `1.`), blockquotes (`>`)
- Salva em `materiais_gerados/material_<timestamp>.pdf`

**Funções públicas:**

| Função | Descrição |
|--------|-----------|
| `gerar_pdf(material_adaptado, assunto, dimensoes, pasta_saida)` | Gera e salva o PDF, retorna o caminho do arquivo |

---

## Dependências

Instale com:

```bash
pip install -r requirements.txt
```

| Pacote            | Uso no projeto |
|-------------------|----------------|
| `google-generativeai` | SDK do Gemini (LLM) |
| `google-api-core`     | Exceção `ResourceExhausted` |
| `pdfplumber`          | Leitura e extração de texto do PDF |
| `fpdf2`               | Geração do PDF de saída |
| `python-dotenv`       | Leitura do arquivo `.env` |
| `matplotlib`          | Apenas pelo caminho das fontes DejaVu |

> **Obs.:** O projeto usa as fontes DejaVu instaladas junto ao `matplotlib` em
> `/opt/anaconda3/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf`.
> Se o caminho for diferente no seu ambiente, ajuste as constantes em `gerador_pdf.py`.

---

## Configuração

### 1. Arquivo `.env`

Crie o arquivo `.env` na raiz do projeto com sua chave da API Gemini:

```env
GEMINI_API_KEY=sua_chave_aqui
```

> Obtenha sua chave em: https://aistudio.google.com/app/apikey

### 2. PDF da Disciplina

Coloque o PDF da disciplina na raiz do projeto com o nome:

```
disciplina.pdf
```

O sistema funciona melhor com PDFs que possuem **sumário numerado** (ex: livros da Casa do Código).

---

## Como Executar

```bash
cd /caminho/para/projeto
python main.py
```

O sistema irá:
1. Exibir o questionário interativo no terminal
2. Gerar seu perfil de aprendizagem
3. Listar os capítulos/assuntos disponíveis
4. Pedir para você escolher um assunto
5. Adaptar o conteúdo e gerar o PDF personalizado

O arquivo PDF será salvo em:
```
materiais_gerados/material_YYYYMMDD_HHMMSS.pdf
```

---

## Estrutura de Arquivos

```
projeto/
│
├── main.py                  # Ponto de entrada principal
├── gemini_config.py         # Configuração e retry da API Gemini
├── questionario.py          # Questionário Felder-Silverman (4 perguntas)
├── profiler.py              # Geração do perfil do aluno via LLM
├── leitor_pdf.py            # Extração de capítulos do PDF
├── assuntos_llm.py          # Fallback: identificação de tópicos via LLM
├── seletor_conteudo.py      # Seleção interativa do capítulo pelo aluno
├── rewrite.py               # Adaptação do conteúdo via LLM
├── gerador_pdf.py           # Geração do PDF final formatado
│
├── disciplina.pdf           # PDF de entrada da disciplina
├── conteudo.md              # Artefato intermediário: texto bruto do capítulo selecionado
│
├── materiais_gerados/       # PDFs gerados pelo sistema
│   └── material_*.pdf
│
├── .env                     # Chave da API Gemini (não versionar!)
└── README.md                # Esta documentação
```

---

## Limitações e Observações

- **Cota da API Gemini (Free Tier):** O plano gratuito permite 20 requisições/dia para `gemini-2.5-flash`. O sistema tenta retry automático (até 3 tentativas, 15/30/45 s de espera). Ao esgotar a cota, o `profiler.py` continua com perfil de fallback e o `rewrite.py` pode falhar.

- **Tamanho do conteúdo:** O `rewrite.py` limita o texto enviado à LLM a **8.000 caracteres**. Para capítulos muito longos, somente o início será adaptado.

- **Dependência do formato do PDF:** A extração automática de capítulos funciona melhor em PDFs com sumário estruturado. PDFs de slides, digitalizados (imagem) ou sem estrutura textual podem não ser suportados.

- **Fontes DejaVu:** O caminho das fontes está fixo para o ambiente Anaconda. Ajuste `gerador_pdf.py` se necessário.

- **Modelo Gemini selecionado dinamicamente:** O sistema usa o primeiro modelo disponível que suporte `generateContent`. Se desejar fixar um modelo específico, altere `criar_modelo()` em `gemini_config.py`.
