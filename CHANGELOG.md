# Histórico do Projeto (Changelog)

## [2026-03-23] - Limpeza de Código e Consolidação do Gemini
### Adicionado
- **Prevenção de Cache Residual**: Adicionado comando no `main.py` para exclusão forçada do arquivo `conteudo.md` pré-existente antes da extração de um novo PDF, impedindo contaminação de sessões e memórias estáticas.
- **Documentação Master**: O `README.md` foi inteiramente reescrito e documentado para refletir as inclusões modernas (16 prompts isolados do FSLM e a utilização maciça de roteamento com `llm_config.py`).

### Alterado
- **Simplificação Didática de Prompts**: O arquivo `prompts_adaptacao.py` foi completamente reescrito para abandonar os laços cartesianos complexos (itertools) e agora conta com todos os 16 estados da arquitetura Felder-Silverman descritos de maneira explícita, facilitando muito o entendimento acadêmico, estrutural e testes independentes de cada combinação.
- **Tuplas do Rewrite**: A tupla de indexação das regras no `rewrite.py` foi recalibrada para `(Compreensão, Percepção, Entrada, Processamento)` adequando-se melhor a ordem lógica proposta para os prompts de ensino atualizados.

### Removido
- Função `_selecionar_llm()` do `main.py`. A decisão do projeto foi engessar e apostar inteiramente no processamento universal com o Google Gemini. 
- Remoção definitiva de chamadas a arquivos não rastreados ou defasados (como o antigo `assuntos_llm.py`).

## [2026-03-20] - Limpeza de Dependências, 16 Prompts Matemáticos e Fluxo Completo Ativo
### Adicionado
- **Arquitetura de Prompts Isolados**: Criado o módulo `prompts_adaptacao.py` que gera precisamente 16 combinações de prompts exatos e fechados, cobrindo todo o modelo Felder-Silverman. Isso possibilita ao sistema escolher matematicamente a instrução perfeita baseada na tupla do aluno sem escrever enormes templates redundantes em `rewrite.py`.
- Finalização da liberação do código em `main.py`, efetivando oficialmente as etapas iterativas conectadas de leitura -> perfilamento -> LLM para PDF.

### Removido
- Removido o longo e obsoleto script `assuntos_llm.py` que fragmentava páginas de pdf em um método ineficiente antigo.
- Deletado arquivo temporário/ruído `projeto.py` que engessava as simulações e duplicava códigos principais.

## [2026-03-20] - Refatoração do Motor de Extração e Seleção
### Adicionado
- Nova funcionalidade de parsing dinâmico de assuntos do sistema pela LLM (Google Gemini) diretamente no arquivo `seletor_conteudo.py`.
- Adoção da biblioteca `PyMuPDF` (`fitz`) para uma leitura estruturada do PDF significativamente mais rápida e com mais inteligência em conversão de parágrafos.

### Alterado
- **Motor de Leitura Universal**: O foco da `leitor_pdf.py` modificado retirou a limitação do sistema buscar por formatos de sumários da "Casa do Código". Agora o script processa de forma genérica o conteúdo inteiro do PDF e armazena em formato de longo texto no `conteudo.md`.
- **Seleção Dinâmica de Capítulo**: O menu rígido de seleção das partes separadas por Python sumiu. Agora a inteligência artificial entende o conteúdo completo do PDF (`conteudo.md`), gera uma listagem em JSON dos tópicos lógicos daquele arquivo, imprime num menu visual humanizado para o aluno escolher, e despacha a requisição de foco junto ao documento inteiro para o módulo de reescrita em `rewrite.py`.
- **Limpeza no Main**: O arquivo `main.py` foi simplificado e reestruturado para acompanhar o fluxo das novas extrações, delegando a responsabilidade de escolha e contexto amplamente à inteligência analítica em vez de heurísticas tradicionais de Regex.
