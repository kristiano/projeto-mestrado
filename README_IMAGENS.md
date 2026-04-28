# Sistema de Geração de Imagens Personalizadas com Gemini

## Visão Geral

Este sistema gera imagens detalhadas e personalizadas de acordo com o estilo de aprendizado do aluno, utilizando a API do Gemini (modelo Imagen via Gemini 2.0 Flash).

## Como Funciona

### 1. Extração de Descrições de Imagens

O módulo `gerador_imagens.py` extrai automaticamente descrições de imagens do texto adaptado usando padrões como:
- `[INSERIR IMAGEM: descrição]`
- `[INSERIR DIAGRAMA: descrição]`
- `[INSERIR GRÁFICO: descrição]`
- `[INSERIR INFOGRÁFICO: descrição]`
- `[INSERIR FLUXOGRAMA: descrição]`
- `[INSERIR ESQUEMA: descrição]`
- `[INSERIR MAPA CONCEITUAL: descrição]`
- `[INSERIR MAPA VISUAL: descrição]`
- `[INSERIR PAINEL: descrição]`
- `[INSERIR QUADRO: descrição]`

### 2. Criação de Prompts Enriquecidos

Para cada descrição extraída, o sistema cria um prompt enriquecido baseado nas dimensões Felder-Silverman do aluno:

#### Dimensão: Percepção (Sensorial vs Intuitivo)
- **Sensorial**: Estilo realista, exemplos concretos do mundo real, aplicações práticas, elementos tangíveis, texturas familiares
- **Intuitivo**: Estilo abstrato, conceitual, diagramas teóricos, representações simbólicas, metáforas visuais inovadoras

#### Dimensão: Processamento (Ativo vs Reflexivo)
- **Ativo**: Composição dinâmica, cores vibrantes, elementos que sugerem interação
- **Reflexivo**: Layout limpo, design contemplativo, espaço para processamento mental

#### Dimensão: Compreensão (Global vs Sequencial)
- **Global**: Visão holística, diagramas de visão geral mostrando conexões entre todos os elementos
- **Sequencial**: Diagrama passo a passo mostrando progressão lógica, fluxo linear, etapas numeradas

### 3. Geração de Imagens com Gemini

O sistema utiliza o modelo `gemini-2.0-flash-exp-image-generation` que integra a tecnologia Imagen do Google para geração de imagens de alta qualidade.

**Fluxo:**
1. Configura a API do Gemini com a chave do `.env`
2. Envia o prompt enriquecido para o modelo
3. Processa a resposta para extrair dados da imagem (inline_data)
4. Salva a imagem em formato PNG na pasta `imagens_geradas/`
5. Substitui o placeholder no texto pelo caminho da imagem gerada

## Estrutura dos Prompts por Perfil

Os prompts de adaptação em `prompts_adaptacao.py` agora incluem descrições EXTREMAMENTE DETALHADAS para cada tipo de aluno visual:

### Exemplo para Aluno Sequencial-Sensorial-Visual-Ativo:
```
[INSERIR DIAGRAMA: descrição EXTREMAMENTE DETALHADA mostrando elementos 
concretos com cores específicas (ex: azul #0066CC para entradas, verde 
#00AA44 para saídas), formas geométricas definidas (retângulos 
arredondados para processos, losangos para decisões), rótulos claros em 
português fonte Arial 14pt, setas grossas indicando fluxo]

Exemplo: [INSERIR INFOGRÁFICO: fluxograma horizontal com 5 etapas, cada 
etapa em caixa retangular colorida (laranja, verde, azul, amarelo, roxo), 
ícones representativos à esquerda de cada caixa, setas pretas grossas 
conectando as etapas, título em destaque no topo]
```

### Exemplo para Aluno Global-Intuitivo-Visual-Reflexivo:
```
[INSERIR MAPA CONCEITUAL ABSTRATO: estrutura fractal ou recursiva 
começando do centro e expandindo em camadas concêntricas, cada camada 
representando um nível de profundidade teórica, camadas de significado 
diferenciadas por texturas (pontilhado, hachurado, gradiente), relações 
profundas entre teorias mostradas por túneis ou pontes entre camadas, 
paleta sóbria e contemplativa (tons de azul profundo, cinza, branco)]

Exemplo: [INSERIR MANDALA TEÓRICA: círculo central com princípio 
fundamental, 6 pétalas ao redor com teorias derivadas, anel externo com 
aplicações e críticas, linhas sutis conectando elementos opostos, fundo 
degradê radial]
```

## Arquivos Gerados

- **Pasta**: `imagens_geradas/`
- **Formato**: PNG
- **Nomenclatura**: `imagem_{timestamp}.png`
- **Qualidade**: Alta resolução, adequada para material educacional universitário

## Tratamento de Erros

O sistema inclui:
- Retry automático para limites de quota da API
- Fallback para métodos alternativos (implementação futura)
- Logging detalhado de falhas
- Manutenção de placeholders não gerados com marcação `[IMAGEM_NAO_GERADA: descrição]`

## Requisitos

```bash
pip install google-generativeai pillow python-dotenv
```

## Configuração

Adicione sua API key no arquivo `.env`:
```
GEMINI_API_KEY=sua_chave_aqui
```

## Exemplo de Uso

```python
from gerador_imagens import substituir_placeholders_por_imagens

material_com_imagens, lista_imagens = substituir_placeholders_por_imagens(
    texto=material_adaptado,
    dimensoes=dimensoes,
    pasta_imagens="imagens_geradas",
    max_imagens=5
)

print(f"Imagens geradas: {len(lista_imagens)}")
for img in lista_imagens:
    print(f"  - {img}")
```

## Vantagens

1. **Personalização Real**: Cada imagem é única para o perfil do aluno
2. **Alta Qualidade**: Modelo Imagen do Google para geração profissional
3. **Contextualização**: Imagens refletem o conteúdo específico do material
4. **Automatização**: Processo totalmente integrado ao fluxo de adaptação
5. **Detalhamento**: Prompts ricos garantem imagens informativas e pedagógicas

## Limitações

- Quota da API pode limitar o número de imagens por sessão
- Tempo de geração varia conforme complexidade (tipicamente 5-15 segundos por imagem)
- Requer conexão com internet para acessar API do Gemini
