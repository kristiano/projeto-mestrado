from typing import Dict, Tuple

# Dicionário contendo as diretrizes explícitas para os 16 perfis de Felder-Silverman.
# Organizado na ordem: (Compreensão, Percepção, Entrada, Processamento)
DIRETRIZES_FSLSM = {
    # --- GRUPO 1: SEQUENCIAL E SENSORIAL (Focados em passo a passo e vida real) ---
    ('Sequencial', 'Sensorial', 'Visual', 'Ativo'): 
        "1. Estruture o texto de forma linear, em passos lógicos e incrementais (1, 2, 3...).\n"
        "2. Ancore a teoria em dados concretos, fatos e exemplos práticos do mundo real.\n"
        "3. Substitua longos parágrafos por sugestões de infográficos, tabelas ou listas visuais (use [INSERIR DIAGRAMA: descrição]).\n"
        "4. Termine com um desafio prático ou estudo de caso para ser resolvido em grupo.",

    ('Sequencial', 'Sensorial', 'Visual', 'Reflexivo'): 
        "1. Estruture o texto de forma linear, em passos lógicos e incrementais.\n"
        "2. Ancore a teoria em dados concretos, fatos e procedimentos detalhados.\n"
        "3. Priorize o uso de esquemas visuais, gráficos e listas no lugar de texto denso.\n"
        "4. Insira 'Pausas para Reflexão' ao longo do texto com perguntas para análise introspectiva e individual.",

    ('Sequencial', 'Sensorial', 'Verbal', 'Ativo'): 
        "1. Estruture o texto de forma linear, explicando o conteúdo passo a passo.\n"
        "2. Utilize exemplos da vida real, dados e fatos práticos.\n"
        "3. Evite sugerir gráficos ou diagramas; explique tudo exaustivamente em formato de texto discursivo.\n"
        "4. Inclua perguntas instigantes voltadas para debate em grupo e experimentação prática.",

    ('Sequencial', 'Sensorial', 'Verbal', 'Reflexivo'): 
        "1. Estruture o texto de forma linear, em etapas lógicas e bem explicadas.\n"
        "2. Foque na aplicação prática, utilizando fatos e resolução de problemas reais.\n"
        "3. Forneça explicações textuais ricas e detalhadas, sem depender de recursos visuais.\n"
        "4. Insira momentos de introspecção no texto, pedindo para o aluno refletir sozinho sobre o procedimento.",

    # --- GRUPO 2: SEQUENCIAL E INTUITIVO (Focados em passo a passo e teoria) ---
    ('Sequencial', 'Intuitivo', 'Visual', 'Ativo'): 
        "1. Construa o raciocínio de forma lógica, incremental e contínua.\n"
        "2. Foque nos conceitos, ideias inovadoras e formulações matemáticas, removendo exemplos rotineiros.\n"
        "3. Utilize diagramas conceituais, mapas mentais ou fluxogramas teóricos no lugar de texto.\n"
        "4. Proponha um problema aberto ou inovador para o aluno discutir e resolver com colegas.",

    ('Sequencial', 'Intuitivo', 'Visual', 'Reflexivo'): 
        "1. Avance o conteúdo de forma linear, conectando um conceito ao próximo logicamente.\n"
        "2. Aprofunde-se nas teorias, abstrações e significados ocultos do tema.\n"
        "3. Sugira fortemente o uso de gráficos estruturais e diagramas teóricos.\n"
        "4. Proponha pausas silenciosas e perguntas retóricas para que o aluno processe a teoria sozinho.",

    ('Sequencial', 'Intuitivo', 'Verbal', 'Ativo'): 
        "1. Organize a explicação passo a passo, construindo a teoria gradualmente.\n"
        "2. Foque em conceitos abstratos, significados e teorias fundamentais.\n"
        "3. Desenvolva o conteúdo inteiramente através de texto discursivo rico e argumentativo.\n"
        "4. Sugira tópicos de debate conceitual para serem explorados em um grupo de estudo.",

    ('Sequencial', 'Intuitivo', 'Verbal', 'Reflexivo'): 
        "1. Desenvolva o texto de forma linear e rigidamente estruturada.\n"
        "2. Priorize a explicação de teorias complexas e ideias abstratas.\n"
        "3. Use explicações narrativas longas e detalhadas, evitando imagens ou resumos esquemáticos.\n"
        "4. Crie seções de reflexão teórica para que o aluno pondere profundamente sobre os conceitos de forma isolada.",

    # --- GRUPO 3: GLOBAL E SENSORIAL (Focados em visão geral e vida real) ---
    ('Global', 'Sensorial', 'Visual', 'Ativo'): 
        "1. Inicie com um grande resumo holístico conectando o tema ao panorama geral da disciplina. Evite focar em micro-passos.\n"
        "2. Explique esse panorama geral usando fatos tangíveis e exemplos práticos do dia a dia.\n"
        "3. Sugira mapas visuais da disciplina e diagramas que mostrem a interligação das partes.\n"
        "4. Proponha atividades práticas e experimentações baseadas na visão geral para fazer em grupo.",

    ('Global', 'Sensorial', 'Visual', 'Reflexivo'): 
        "1. Forneça primeiro o contexto geral e a conclusão, para depois entrar nos detalhes tangíveis.\n"
        "2. Mostre como esse conhecimento se aplica a cenários reais, usando dados concretos.\n"
        "3. Utilize painéis visuais, infográficos e esquemas que mostrem o 'todo' de forma gráfica.\n"
        "4. Adicione perguntas ao final das seções para que o aluno reflita individualmente sobre como as partes formam o todo.",

    ('Global', 'Sensorial', 'Verbal', 'Ativo'): 
        "1. Comece a explicação pela visão macro do problema e as conexões principais.\n"
        "2. Sustente essa visão macro com exemplos práticos, dados concretos e procedimentos.\n"
        "3. Explique todas as interconexões através de uma narrativa textual fluida e discursiva (sem gráficos).\n"
        "4. Crie dinâmicas orais e simulações focadas em fatos para debater em equipe.",

    ('Global', 'Sensorial', 'Verbal', 'Reflexivo'): 
        "1. Apresente o cenário completo e a utilidade macro do conteúdo logo no primeiro parágrafo.\n"
        "2. Detalhe os fatos e dados práticos que compõem esse cenário.\n"
        "3. Use um texto rico, descritivo e bem escrito para formar imagens mentais sem usar fotos reais.\n"
        "4. Insira momentos de pausa e leitura silenciosa para absorção e introspecção das informações.",

    # --- GRUPO 4: GLOBAL E INTUITIVO (Focados em visão geral e teoria pura) ---
    ('Global', 'Intuitivo', 'Visual', 'Ativo'): 
        "1. Inicie apresentando a teoria de forma panorâmica, destacando saltos conceituais e a visão holística.\n"
        "2. Concentre-se nos modelos teóricos, abstrações e conceitos de alto nível.\n"
        "3. Utilize infográficos teóricos, quadros abstratos e diagramas de intersecção.\n"
        "4. Encerre sugerindo um *brainstorming* em grupo para discutir as teorias apresentadas.",

    ('Global', 'Intuitivo', 'Visual', 'Reflexivo'): 
        "1. Dê ênfase à compreensão holística e ao entendimento do cenário teórico completo.\n"
        "2. Explore os significados conceituais profundos e abstrações complexas.\n"
        "3. Peça a inserção de representações visuais abstratas e mapas conceituais abrangentes.\n"
        "4. Sugira fortes questionamentos filosóficos ou teóricos para reflexão puramente individual e profunda.",

    ('Global', 'Intuitivo', 'Verbal', 'Ativo'): 
        "1. Apresente a 'big picture' (o panorama geral) focando no significado final daquele estudo.\n"
        "2. Explore teorias de forma abrangente, focando em ideias e inovações.\n"
        "3. Discorra longamente em texto; a argumentação textual é a chave para este aluno.\n"
        "4. Proponha cenários teóricos para que o aluno discuta os conceitos ativamente com outros.",

    ('Global', 'Intuitivo', 'Verbal', 'Reflexivo'): 
        "1. Comece resumindo o conceito geral e como ele se liga a outras teorias e matérias.\n"
        "2. Fique estritamente no campo conceitual, teórico e abstrato.\n"
        "3. Escreva blocos de texto profundos, focados em semântica e argumentação lógica (sem recursos visuais).\n"
        "4. Conclua com perguntas reflexivas e teóricas para meditação e resolução solitária."
}

def construir_prompts() -> Dict[Tuple[str, str, str, str], str]:
    """
    Constrói a lista final de prompts juntando as regras fixas (DIRETRIZES_FSLSM)
    dentro do template mestre do Design Instrucional.
    """
    prompts_prontos = {}
    
    for (comp, perc, ent, proc), diretriz in DIRETRIZES_FSLSM.items():
        template_mestre = f"""# Role: Especialista em Design Instrucional e Teoria de Felder-Silverman

## Contexto
Sou um professor universitário e preciso adaptar um conteúdo técnico para um aluno com um perfil de aprendizagem específico, baseado no Index of Learning Styles (ILS).

## Dados do Aluno (Perfil FSLM)
- **Compreensão:** {comp}
- **Percepção:** {perc}
- **Entrada:** {ent}
- **Processamento:** {proc}

## Instruções de Adaptação (Diretrizes Teóricas)
Utilize as seguintes restrições baseadas nos polos de Felder e Silverman para formatar a explicação:

{diretriz}

## Formato de Saída
Gere o conteúdo estruturado em Markdown. Use blocos de código para exemplos técnicos e fórmulas matemáticas em texto simples ou notação Markdown padrão (ex: `O(n^2)` ou `2^n`).

## Conteúdo a ser Adaptado
{{conteudo_bruto}}
"""
        chave = (comp, perc, ent, proc)
        prompts_prontos[chave] = template_mestre.strip()
        
    return prompts_prontos

# Exporta o dicionário completo de prompts prontos para uso no rewrite.py
PROMPTS_ESPECIFICOS = construir_prompts()

if __name__ == "__main__":
    print(f"Total de prompts estruturados: {len(PROMPTS_ESPECIFICOS)}")
