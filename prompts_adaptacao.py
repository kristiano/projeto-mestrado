import itertools
from typing import Dict, Tuple

# Definições base das diretrizes para cada um dos polos do modelo Felder-Silverman.
# Você pode editar os textos aqui para afinar a instrução que a LLM receberá.

DIRETRIZES = {
    "Processamento": {
        "Ativo": "Inclua metodologias ativas: sugira exercícios práticos aplicados, debates simulados, e insira perguntas iterativas do tipo 'Como você usaria isso agora?'. O aluno precisa sentir que está colocando a mão na massa.",
        "Reflexivo": "Adicione momentos de reflexão profunda. Insira perguntas abertas que estimulem análises individuais e instigue o aluno a pensar sobre o 'porquê' dos conceitos antes de entregar a resposta."
    },
    "Percepção": {
        "Sensorial": "Apresente fatos concretos, fórmulas, dados empíricos, dicas do mundo prático e resoluções padronizadas de problemas. O aluno é pragmático e focado no que é real e testável.",
        "Intuitivo": "Foque em conceitos abstratos, inovações, teorias subjacentes e conexões criativas. Evite muita repetição e vá direto para os princípios inovadores que sustentam o assunto."
    },
    "Entrada": {
        "Visual": "Como a saída será renderizada em MarkDown (leitura) por PDF, abuse intensamente de recursos visuais ortográficos: crie tabelas elaboradas, esquemas / árvores com caracteres `-` e `>`, blocos de citação, emojis ilustrativos e use formatação em texto (negrito e itálico) para dar cor e foco à leitura.",
        "Verbal": "Desenvolva o texto com explicações verbais ricas. Construa uma excelente narrativa. O estudante prefere ler parágrafos bem fluidos que entreguem cada nuance e detalhe falado à exaustão."
    },
    "Compreensão": {
        "Sequencial": "Estruture o guia em degraus estritos e perfeitamente lógicos. Vá do passo A ao B, evoluindo linearmente, sem pular níveis e sem tentar mostrar o fim antes de explicar o começo.",
        "Global": "Inicie o texto IMEDIATAMENTE entregando o 'The Big Picture' (o Grande Resumo ou a Visão Crítica). Mostre toda a floresta antes de focar nas árvores, destacando como essa matéria isolada se conecta com o plano e o universo maior da aprendizagem."
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
        prompt_especifico = f"""Você é um Tutor Professor Mestre Especialista em Pedagogia e Adaptação de Materiais Didáticos Baseados no modelo de Felder-Silverman.

Aja considerando obrigatoriamente que ALUNO PARA O QUAL VOCÊ ESTÁ ESCREVENDO possui o perfil exato:
[{proc}, {perc}, {ent}, {comp}]

Sua missão é reescrever o texto base fornecido pela disciplina, aplicando o 'fine tuning' pontual para que os canais neurológicos deste estudante específico o absorvam com o mínimo atrito cognitivo.

Para este prompt específico, APLIQUE AS 4 REGRAS ABAIXO na arquitetura da sua reescrita:

1. [{proc}]: {DIRETRIZES["Processamento"][proc]}
2. [{perc}]: {DIRETRIZES["Percepção"][perc]}
3. [{ent}]: {DIRETRIZES["Entrada"][ent]}
4. [{comp}]: {DIRETRIZES["Compreensão"][comp]}

Adapte as palavras, a diagramação e a abordagem do conteúdo original, MANTENDO o rigor técnico.

---
CONTEÚDO ORIGINAL A SER ADAPTADO:
{{conteudo_bruto}}
"""
        prompts_16[chave_tupla] = prompt_especifico.strip()
        
    return prompts_16

# Esta constante exporta no momento em que o arquivo é importado em rewrite.py
PROMPTS_ESPECIFICOS = gerar_16_prompts()

if __name__ == "__main__":
    # Teste para listar e comprovar a existência dos 16 prompts formatados
    for perfil, prompt_text in PROMPTS_ESPECIFICOS.items():
        print(f"\n======================================")
        print(f"PERFIL: {perfil}")
        print(f"--- PREVIEW DO PROMPT ---")
        print(prompt_text[:400] + "...\n")
