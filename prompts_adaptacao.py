import itertools
from typing import Dict, Tuple

# Definições base das diretrizes para cada um dos polos do modelo Felder-Silverman.
# Textos atualizados de acordo com as diretrizes do Especialista em Design Instrucional.

DIRETRIZES = {
    "Processamento": {
        "Ativo": "Insira uma atividade de 'mão na massa' ou um desafio imediato para o aluno testar.",
        "Reflexivo": "Insira perguntas instigantes que exijam pausa para análise profunda antes de prosseguir."
    },
    "Percepção": {
        "Sensorial": "Foque em aplicações práticas, exemplos do mundo real e dados concretos.",
        "Intuitivo": "Priorize a teoria subjacente, modelos matemáticos e a inovação conceitual."
    },
    "Entrada": {
        "Visual": "Descreva como estruturar diagramas, mapas mentais ou fluxogramas. Use formatação que facilite a 'escaneabilidade'.",
        "Verbal": "Utilize explicações textuais detalhadas, analogias narrativas e discussões teóricas."
    },
    "Compreensão": {
        "Sequencial": "Apresente o conteúdo em uma trilha linear, passo a passo, garantindo que cada etapa dependa da anterior.",
        "Global": "Comece apresentando o objetivo macro e a utilidade final do conceito antes de mergulhar nos detalhes."
    }
}

def gerar_16_prompts() -> Dict[Tuple[str, str, str, str], str]:
    """
    Gera um dicionário contendo 16 prompts únicos de adaptação sistêmica para 
    todos os possíveis cruzamentos de estilos Felder-Silverman de um aluno.
    
    Chave do dicionário: (Processamento, Percepção, Entrada, Compreensão)
    Exemplo: ('Ativo', 'Sensorial', 'Visual', 'Sequencial')
    """
    prompts_16 = {}
    
    # Extrai todas as combinações (2x2x2x2 = 16)
    estilos_processamento = ["Ativo", "Reflexivo"]
    estilos_percepcao = ["Sensorial", "Intuitivo"]
    estilos_entrada = ["Visual", "Verbal"]
    estilos_compreensao = ["Sequencial", "Global"]
    
    combinacoes = itertools.product(
        estilos_processamento, 
        estilos_percepcao, 
        estilos_entrada, 
        estilos_compreensao
    )
    
    for (proc, perc, ent, comp) in combinacoes:
        chave_tupla = (proc, perc, ent, comp)
        
        # Constrói o template base formatado exclusivamente para essa combinação exata
        prompt_especifico = f"""# Role: Especialista em Design Instrucional e Teoria de Felder-Silverman

## Contexto
Sou um professor universitário e preciso adaptar um conteúdo técnico para um aluno com um perfil de aprendizagem específico, baseado no Index of Learning Styles (ILS).

## Dados do Aluno (Perfil FSLM)
- **Processamento:** {proc}
- **Percepção:** {perc}
- **Entrada:** {ent}
- **Compreensão:** {comp}

## Instruções de Adaptação (Diretrizes Teóricas)
Utilize as seguintes restrições baseadas nos polos de Felder e Silverman para este aluno:

1. **Eixo de Percepção ({perc}):**
   - {DIRETRIZES["Percepção"][perc]}
2. **Eixo de Entrada ({ent}):**
   - {DIRETRIZES["Entrada"][ent]}
3. **Eixo de Processamento ({proc}):**
   - {DIRETRIZES["Processamento"][proc]}
4. **Eixo de Compreensão ({comp}):**
   - {DIRETRIZES["Compreensão"][comp]}

## Formato de Saída
Gere o conteúdo estruturado em Markdown. Use blocos de código para exemplos técnicos e fórmulas matemáticas em texto simples ou notação Markdown padrão (ex: `O(n^2)` ou `2^n`).

## Conteúdo a ser Adaptado
{{conteudo_bruto}}
"""
        prompts_16[chave_tupla] = prompt_especifico.strip()
        
    return prompts_16

# Esta constante exporta no momento em que o arquivo é importado em rewrite.py
PROMPTS_ESPECIFICOS = gerar_16_prompts()

if __name__ == "__main__":
    # Teste para listar e comprovar a existência dos 16 prompts formatados
    for perfil, prompt_text in PROMPTS_ESPECIFICOS.items():
        print(f"\\n======================================")
        print(f"PERFIL: {perfil}")
        print(f"--- PREVIEW DO PROMPT ---")
        print(prompt_text[:400] + "...\\n")
