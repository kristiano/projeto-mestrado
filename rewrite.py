# rewrite.py
# Adaptação do material didático ao perfil de aprendizagem do aluno

import time
from gemini_config import criar_modelo
from prompts_adaptacao import PROMPTS_ESPECIFICOS

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

    # Identifica a chave correta baseada no perfil gerado para recuperar o prompt específico
    # Ordem: (Compreensão, Percepção, Entrada, Processamento)
    chave_perfil = (
        dimensoes["compreensao"],
        dimensoes["percepcao"], 
        dimensoes["entrada"], 
        dimensoes["processamento"]
    )
    
    # Resgata o prompt de sistema exclusivo para as configurações neurais deste usuário
    prompt_base = PROMPTS_ESPECIFICOS.get(chave_perfil)
    if not prompt_base:
        raise ValueError(f"Prompt não encontrado para o perfil: {chave_perfil}")

    # Injeta o texto na variável {conteudo_bruto} descrita no template do prompt
    prompt_final = prompt_base.replace("{conteudo_bruto}", texto[:8000])

    # Como o novo prompt já é muito forte e abrange as instruções de papel (Role),
    # podemos usar uma instrução de sistema mais direta focada em como o assistente deve se portar:
    system_message = (
        "Você é um Especialista em Inteligência Artificial para Educação "
        "e Design Instrucional.\n\n"
        "Sua tarefa é seguir ESTRITAMENTE o metaprompt fornecido pelo usuário, "
        "modificando a estrutura e os argumentos do texto base apenas conforme "
        "as restrições do modelo Felder-Silverman injetadas."
    )

    # Cria o modelo
    model = criar_modelo(system_instruction=system_message)

    # Executa a geração de inteligência artificial
    response = model.generate_content(prompt_final)
    material_adaptado = response.text

    stop_time = time.time()
    print(f"Tempo de execução do Rewrite: {(stop_time - start_time):.2f} s\n***\n")

    return material_adaptado