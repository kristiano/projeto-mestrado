from typing import Dict, Tuple

# Dicionário contendo as diretrizes explícitas para os 16 perfis de Felder-Silverman.
# Organizado na ordem: (Compreensão, Percepção, Entrada, Processamento)
DIRETRIZES_FSLSM = {
    # --- GRUPO 1: SEQUENCIAL E SENSORIAL (Focados em passo a passo e vida real) ---
    ('Sequencial', 'Sensorial', 'Visual', 'Ativo'): 
        "1. Estruture o texto de forma linear, em passos lógicos e incrementais (1, 2, 3...).\\n"
        "2. Ancore a teoria em dados concretos, fatos e exemplos práticos do mundo real.\\n"
        "3. Substitua longos parágrafos por sugestões de infográficos, tabelas ou listas visuais. Use marcadores como [INSERIR DIAGRAMA: descrição EXTREMAMENTE DETALHADA mostrando elementos concretos com cores específicas (ex: azul #0066CC para entradas, verde #00AA44 para saídas), formas geométricas definidas (retângulos arredondados para processos, losangos para decisões), rótulos claros em português fonte Arial 14pt, setas grossas indicando fluxo]. Exemplo: [INSERIR INFOGRÁFICO: fluxograma horizontal com 5 etapas, cada etapa em caixa retangular colorida (laranja, verde, azul, amarelo, roxo), ícones representativos à esquerda de cada caixa, setas pretas grossas conectando as etapas, título em destaque no topo].\\n"
        "4. Termine com um desafio prático ou estudo de caso para ser resolvido em grupo.\\n"
        "5. Para alunos Visuais, SEMPRE sugira pelo menos 2-3 elementos visuais ricos com descrições detalhadas incluindo paleta de cores, disposição espacial (topo/base, esquerda/direita), tamanhos relativos dos elementos, e conteúdo textual exato dos rótulos.",
    
    ('Sequencial', 'Sensorial', 'Visual', 'Reflexivo'): 
        "1. Estruture o texto de forma linear, em passos lógicos e incrementais.\\n"
        "2. Ancore a teoria em dados concretos, fatos e procedimentos detalhados.\\n"
        "3. Priorize o uso de esquemas visuais, gráficos e listas no lugar de texto denso. Use [INSERIR GRÁFICO: descrição rica em detalhes especificando tipo de gráfico (barras verticais, linhas, pizza), eixos claramente rotulados com unidades de medida, legenda explicativa posicionada à direita, dados concretos com valores numéricos exatos, cores diferenciadas para cada série de dados (ex: série A em vermelho #CC0000, série B em azul #0066CC)]. Exemplo: [INSERIR GRÁFICO DE BARRAS: 6 barras verticais de largura 40px, espaçamento 20px, alturas proporcionais aos valores (10, 25, 40, 60, 80, 95), gradiente de cor do azul claro ao escuro, eixo Y rotulado 'Percentual (%)' de 0 a 100, eixo X com categorias em negrito].\\n"
        "4. Insira 'Pausas para Reflexão' ao longo do texto com perguntas para análise introspectiva e individual.\\n"
        "5. Sugira diagramas sequenciais detalhados: [INSERIR FLUXOGRAMA: sequência vertical de 4 passos, cada passo em caixa branca com borda preta 3px, número do passo em círculo colorido no canto superior esquerdo, seta para baixo entre as caixas, descrição objetiva de 2-3 linhas dentro de cada caixa, fundo branco limpo].",
    
    ('Sequencial', 'Sensorial', 'Verbal', 'Ativo'): 
        "1. Estruture o texto de forma linear, explicando o conteúdo passo a passo.\\n"
        "2. Utilize exemplos da vida real, dados e fatos práticos.\\n"
        "3. Evite sugerir gráficos ou diagramas; explique tudo exaustivamente em formato de texto discursivo.\\n"
        "4. Inclua perguntas instigantes voltadas para debate em grupo e experimentação prática.",
    
    ('Sequencial', 'Sensorial', 'Verbal', 'Reflexivo'): 
        "1. Estruture o texto de forma linear, em etapas lógicas e bem explicadas.\\n"
        "2. Foque na aplicação prática, utilizando fatos e resolução de problemas reais.\\n"
        "3. Forneça explicações textuais ricas e detalhadas, sem depender de recursos visuais.\\n"
        "4. Insira momentos de introspecção no texto, pedindo para o aluno refletir sozinho sobre o procedimento.",
    
    # --- GRUPO 2: SEQUENCIAL E INTUITIVO (Focados em passo a passo e teoria) ---
    ('Sequencial', 'Intuitivo', 'Visual', 'Ativo'): 
        "1. Construa o raciocínio de forma lógica, incremental e contínua.\\n"
        "2. Foque nos conceitos, ideias inovadoras e formulações matemáticas, removendo exemplos rotineiros.\\n"
        "3. Utilize diagramas conceituais, mapas mentais ou fluxogramas teóricos no lugar de texto. Use [INSERIR MAPA CONCEITUAL: descrição abstrata mostrando relações entre teorias com conexões simbolizadas por linhas coloridas (vermelho para oposição, verde para complementaridade, azul para hierarquia), nós conceituais em círculos de tamanhos proporcionais à importância, rótulos com nomes das teorias em fonte sans-serif, estrutura radial ou hierárquica clara]. Exemplo: [INSERIR DIAGRAMA TEÓRICO: conceito central em círculo grande (diâmetro 120px) no centro, 6 conceitos secundários em círculos médios (diâmetro 60px) ao redor, linhas curvas conectando conceitos relacionados, código de cores por categoria teórica, fundo gradiente suave].\\n"
        "4. Proponha um problema aberto ou inovador para o aluno discutir e resolver com colegas.\\n"
        "5. Para Visual-Intuitivo: [INSERIR DIAGRAMA TEÓRICO: representação visual de conceitos abstratos usando símbolos matemáticos (∑, ∫, ∂, ∞), equações-chave em destaque, interconexões teóricas mostradas por sobreposição de camadas translúcidas, cores diferenciando categorias (teoria pura em roxo, aplicações em laranja, exceções em cinza)].",
    
    ('Sequencial', 'Intuitivo', 'Visual', 'Reflexivo'): 
        "1. Avance o conteúdo de forma linear, conectando um conceito ao próximo logicamente.\\n"
        "2. Aprofunde-se nas teorias, abstrações e significados ocultos do tema.\\n"
        "3. Sugira fortemente o uso de gráficos estruturais e diagramas teóricos: [INSERIR ESQUEMA CONCEITUAL: estrutura teórica detalhada em camadas horizontais, cada camada representando um nível de abstração (base concreta → intermediário → abstrato puro), setas verticais bidirecionais mostrando influência mútua, legendas explicativas em caixas laterais, paleta monocromática com variações de tom]. Exemplo: [INSERIR PIRÂMIDE CONCEITUAL: 4 níveis empilhados, base larga (fundamentos) estreitando até o topo (teoria avançada), cada nível com cor sólida diferente (verde, amarelo, laranja, vermelho), textos descritivos curtos dentro de cada nível, título geral acima da pirâmide].\\n"
        "4. Proponha pausas silenciosas e perguntas retóricas para que o aluno processe a teoria sozinho.",
    
    ('Sequencial', 'Intuitivo', 'Verbal', 'Ativo'): 
        "1. Organize a explicação passo a passo, construindo a teoria gradualmente.\\n"
        "2. Foque em conceitos abstratos, significados e teorias fundamentais.\\n"
        "3. Desenvolva o conteúdo inteiramente através de texto discursivo rico e argumentativo.\\n"
        "4. Sugira tópicos de debate conceitual para serem explorados em um grupo de estudo.",
    
    ('Sequencial', 'Intuitivo', 'Verbal', 'Reflexivo'): 
        "1. Desenvolva o texto de forma linear e rigidamente estruturada.\\n"
        "2. Priorize a explicação de teorias complexas e ideias abstratas.\\n"
        "3. Use explicações narrativas longas e detalhadas, evitando imagens ou resumos esquemáticos.\\n"
        "4. Crie seções de reflexão teórica para que o aluno pondere profundamente sobre os conceitos de forma isolada.",
    
    # --- GRUPO 3: GLOBAL E SENSORIAL (Focados em visão geral e vida real) ---
    ('Global', 'Sensorial', 'Visual', 'Ativo'): 
        "1. Inicie com um grande resumo holístico conectando o tema ao panorama geral da disciplina. Evite focar em micro-passos.\\n"
        "2. Explique esse panorama geral usando fatos tangíveis e exemplos práticos do dia a dia.\\n"
        "3. Sugira mapas visuais da disciplina e diagramas que mostrem a interligação das partes. Use [INSERIR MAPA VISUAL HOLÍSTICO: visão geral completa ocupando toda a área visual, todas as partes interconectadas por linhas de relacionamento, exemplos reais rotulados com ícones representativos, cores vibrantes e contrastantes (paleta: #FF6B35, #004E89, #FFD23F, #32936F) para diferenciar domínios, disposição em rede ou circular]. Exemplo: [INSERIR DIAGRAMA DE ECOSSISTEMA: conceito central como sol no meio, 8 elementos satélites orbitando, cada um conectado ao centro e entre si por linhas tracejadas, ícones pictóricos em cada elemento, fundo azul gradiente, título em arco no topo].\\n"
        "4. Proponha atividades práticas e experimentações baseadas na visão geral para fazer em grupo.\\n"
        "5. Para Visual-Global: [INSERIR INFOGRÁFICO PANORÂMICO: layout horizontal dividido em 3 colunas (Entrada → Processamento → Saída), setas largas bidirecionais entre colunas mostrando fluxo contínuo, exemplos práticos em caixas destacadas dentro de cada coluna, dados numéricos em badges circulares, rodapé com timeline de aplicação].",
    
    ('Global', 'Sensorial', 'Visual', 'Reflexivo'): 
        "1. Forneça primeiro o contexto geral e a conclusão, para depois entrar nos detalhes tangíveis.\\n"
        "2. Mostre como esse conhecimento se aplica a cenários reais, usando dados concretos.\\n"
        "3. Utilize painéis visuais, infográficos e esquemas que mostrem o 'todo' de forma gráfica: [INSERIR PAINEL INTEGRADO: grid 2x2 mostrando múltiplas perspectivas do mesmo conceito (canto superior esquerdo: teoria, superior direito: prática, inferior esquerdo: vantagens, inferior direito: limitações), comparações lado a lado com divisórias claras, dados empíricos em tabelas miniatura dentro de cada quadrante, cabeçalhos coloridos por quadrante]. Exemplo: [INSERIR QUADRO COMPARATIVO: tabela 4x3 com bordas arredondadas, cabeçalhos em gradiente, células alternando cores claras (zebrado), ícones de check/cruz para comparação rápida, legenda abaixo].\\n"
        "4. Adicione perguntas ao final das seções para que o aluno reflita individualmente sobre como as partes formam o todo.",
    
    ('Global', 'Sensorial', 'Verbal', 'Ativo'): 
        "1. Comece a explicação pela visão macro do problema e as conexões principais.\\n"
        "2. Sustente essa visão macro com exemplos práticos, dados concretos e procedimentos.\\n"
        "3. Explique todas as interconexões através de uma narrativa textual fluida e discursiva (sem gráficos).\\n"
        "4. Crie dinâmicas orais e simulações focadas em fatos para debater em equipe.",
    
    ('Global', 'Sensorial', 'Verbal', 'Reflexivo'): 
        "1. Apresente o cenário completo e a utilidade macro do conteúdo logo no primeiro parágrafo.\\n"
        "2. Detalhe os fatos e dados práticos que compõem esse cenário.\\n"
        "3. Use um texto rico, descritivo e bem escrito para formar imagens mentais sem usar fotos reais.\\n"
        "4. Insira momentos de pausa e leitura silenciosa para absorção e introspecção das informações.",
    
    # --- GRUPO 4: GLOBAL E INTUITIVO (Focados em visão geral e teoria pura) ---
    ('Global', 'Intuitivo', 'Visual', 'Ativo'): 
        "1. Inicie apresentando a teoria de forma panorâmica, destacando saltos conceituais e a visão holística.\\n"
        "2. Concentre-se nos modelos teóricos, abstrações e conceitos de alto nível.\\n"
        "3. Utilize infográficos teóricos, quadros abstratos e diagramas de intersecção: [INSERIR QUADRO TEÓRICO ABSTRATO: diagrama de Venn com 4 círculos sobrepostos (transparência 50%), cada círculo representando uma teoria maior, zonas de intersecção destacadas com cores mistas e rótulos explicando sinergias, símbolos conceituais (lâmpada para ideias, engrenagem para mecanismos, nuvem para abstrações) distribuídos estrategicamente, estrutura não-linear orgânica]. Exemplo: [INSERIR REDE TEÓRICA: 12 nós conceituais distribuídos em padrão hexagonal, conexões por linhas curvas de espessura variável (grossa = forte correlação, fina = fraca correlação), nós coloridos por escola teórica, tamanho do nó proporcional à relevância atual, fundo escuro com elementos em neon].\\n"
        "4. Encerre sugerindo um *brainstorming* em grupo para discutir as teorias apresentadas.\\n"
        "5. Para Visual-Global-Intuitivo: [INSERIR DIAGRAMA DE REDE CONCEITUAL: visualização estilo 'constelação' com todas as teorias como estrelas conectadas, padrões emergentes destacados por áreas sombreadas, metáforas visuais inovadoras (ex: teoria como árvore com raízes/tronco/galhos, ou como edifício com fundação/andares/cobertura), paleta futurista (roxos, azuis elétricos, magenta)].",
    
    ('Global', 'Intuitivo', 'Visual', 'Reflexivo'): 
        "1. Dê ênfase à compreensão holística e ao entendimento do cenário teórico completo.\\n"
        "2. Explore os significados conceituais profundos e abstrações complexas.\\n"
        "3. Peça a inserção de representações visuais abstratas e mapas conceituais abrangentes: [INSERIR MAPA CONCEITUAL ABSTRATO: estrutura fractal ou recursiva começando do centro e expandindo em camadas concêntricas, cada camada representando um nível de profundidade teórica, camadas de significado diferenciadas por texturas (pontilhado, hachurado, gradiente), relações profundas entre teorias mostradas por túneis ou pontes entre camadas, paleta sóbria e contemplativa (tons de azul profundo, cinza, branco)]. Exemplo: [INSERIR MANDALA TEÓRICA: círculo central com princípio fundamental, 6 pétalas ao redor com teorias derivadas, anel externo com aplicações e críticas, linhas sutis conectando elementos opostos, fundo degradê radial].\\n"
        "4. Sugira fortes questionamentos filosóficos ou teóricos para reflexão puramente individual e profunda.",
    
    ('Global', 'Intuitivo', 'Verbal', 'Ativo'): 
        "1. Apresente a 'big picture' (o panorama geral) focando no significado final daquele estudo.\\n"
        "2. Explore teorias de forma abrangente, focando em ideias e inovações.\\n"
        "3. Discorra longamente em texto; a argumentação textual é a chave para este aluno.\\n"
        "4. Proponha cenários teóricos para que o aluno discuta os conceitos ativamente com outros.",
    
    ('Global', 'Intuitivo', 'Verbal', 'Reflexivo'): 
        "1. Comece resumindo o conceito geral e como ele se liga a outras teorias e matérias.\\n"
        "2. Fique estritamente no campo conceitual, teórico e abstrato.\\n"
        "3. Escreva blocos de texto profundos, focados em semântica e argumentação lógica (sem recursos visuais).\\n"
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

**IMPORTANTE PARA ALUNOS VISUAIS:** Sempre inclua descrições ricas e detalhadas para elementos visuais usando o formato [INSERIR TIPO: descrição completa]. Quanto mais detalhes visuais você fornecer (cores, formas, rótulos, disposição espacial), melhor será a imagem gerada posteriormente.

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
