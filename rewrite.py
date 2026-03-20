# rewrite.py
# Adaptação do material didático ao perfil de aprendizagem do aluno
# Adaptado de Vaccaro et al. (2025)

import time
from llm_config import criar_modelo


def adaptar_material(perfil: str, dimensoes: dict, assunto: str, texto: str) -> str:
    """
    Adapta o material didático ao perfil de aprendizagem do aluno.

    Parâmetros:
    perfil   : descrição textual do perfil gerado pelo Profiler
    dimensoes: dicionário com as 4 dimensões do Felder-Silverman
    assunto  : nome do capítulo/assunto escolhido pelo aluno
    texto    : conteúdo extraído do PDF

    Retorna:
    material_adaptado: string com o material personalizado
    """

    print("\n***\nInicializando Rewrite:")
    start_time = time.time()

    # System message do Rewrite
    rewrite_sys_msg = (
        "Você é um professor universitário experiente e didático, "
        "especialista em adaptar materiais de ensino para diferentes "
        "estilos de aprendizagem com base no modelo de Felder-Silverman.\n\n"

        "Você receberá:\n"
        "- O perfil de aprendizagem do aluno\n"
        "- As dimensões do estilo de aprendizagem identificadas\n"
        "- O conteúdo original de um capítulo\n\n"

        "Sua tarefa é reescrever o conteúdo original adaptando-o "
        "ao estilo de aprendizagem do aluno, seguindo estas diretrizes "
        "para cada dimensão:\n\n"

        "COMPREENSÃO:\n"
        "- Sequencial: organize o conteúdo em etapas progressivas e "
        "lógicas, com transições claras entre os tópicos.\n"
        "- Global: comece com uma visão geral do assunto antes dos "
        "detalhes, mostrando como os conceitos se conectam.\n\n"

        "PERCEPÇÃO:\n"
        "- Sensorial: use fatos concretos, dados, exemplos práticos "
        "e aplicações do mundo real.\n"
        "- Intuitivo: enfatize conceitos abstratos, teorias, padrões "
        "e relações entre ideias.\n\n"

        "ENTRADA:\n"
        "- Visual: descreva gráficos, diagramas e tabelas com detalhes; "
        "use analogias visuais e representações espaciais.\n"
        "- Verbal: use explicações textuais detalhadas, listas e "
        "descrições escritas claras.\n\n"

        "PROCESSAMENTO:\n"
        "- Ativo: inclua exemplos práticos, exercícios, situações para "
        "aplicar o conhecimento e discussões em grupo.\n"
        "- Reflexivo: inclua momentos de síntese, resumos, reflexões "
        "e conexões com conhecimentos anteriores.\n\n"

        "Instruções importantes:\n"
        "- Mantenha a precisão e completude do conteúdo original\n"
        "- Não invente informações que não estejam no texto original\n"
        "- Use linguagem clara e adequada ao nível universitário\n"
        "- O material adaptado deve ter estrutura organizada com "
        "títulos e subtítulos\n"
        "- Ao final, inclua um resumo dos pontos principais"
    )

    # User message com o perfil e o conteúdo
    rewrite_user_msg = (
        f"PERFIL DO ALUNO:\n{perfil}\n\n"
        f"DIMENSÕES DE APRENDIZAGEM:\n"
        f"- Compreensão  : {dimensoes['compreensao']}\n"
        f"- Percepção    : {dimensoes['percepcao']}\n"
        f"- Entrada      : {dimensoes['entrada']}\n"
        f"- Processamento: {dimensoes['processamento']}\n\n"
        f"ASSUNTO: {assunto}\n\n"
        f"CONTEÚDO ORIGINAL:\n{texto[:8000]}\n\n"
        f"Reescreva o conteúdo acima adaptado ao perfil de "
        f"aprendizagem deste aluno."
    )

    # Cria o modelo com o system message
    model = criar_modelo(system_instruction=rewrite_sys_msg)

    # Gera o material adaptado
    response = model.generate_content(rewrite_user_msg)
    material_adaptado = response.text

    stop_time = time.time()
    print(f"Tempo de execução do Rewrite: {(stop_time - start_time):.2f} s\n***\n")

    return material_adaptado