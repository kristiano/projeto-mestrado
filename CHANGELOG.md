# Histórico do Projeto (Changelog)

## [2026-03-20] - Refatoração do Motor de Extração e Seleção
### Adicionado
- Nova funcionalidade de parsing dinâmico de assuntos do sistema pela LLM (Google Gemini) diretamente no arquivo `seletor_conteudo.py`.
- Adoção da biblioteca `PyMuPDF` (`fitz`) para uma leitura estruturada do PDF significativamente mais rápida e com mais inteligência em conversão de parágrafos.

### Alterado
- **Motor de Leitura Universal**: O foco da `leitor_pdf.py` modificado retirou a limitação do sistema buscar por formatos de sumários da "Casa do Código". Agora o script processa de forma genérica o conteúdo inteiro do PDF e armazena em formato de longo texto no `conteudo.md`.
- **Seleção Dinâmica de Capítulo**: O menu rígido de seleção das partes separadas por Python sumiu. Agora a inteligência artificial entende o conteúdo completo do PDF (`conteudo.md`), gera uma listagem em JSON dos tópicos lógicos daquele arquivo, imprime num menu visual humanizado para o aluno escolher, e despacha a requisição de foco junto ao documento inteiro para o módulo de reescrita em `rewrite.py`.
- **Limpeza no Main**: O arquivo `main.py` foi simplificado e reestruturado para acompanhar o fluxo das novas extrações, delegando a responsabilidade de escolha e contexto amplamente à inteligência analítica em vez de heurísticas tradicionais de Regex.
