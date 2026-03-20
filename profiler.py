# profiler.py
# Profiler de Estilo de Aprendizagem
# Adaptado de Vaccaro et al. (2025)
# pegar as 4 dimensões identificadas pelo questionário e transforma em uma 
# descrição humanizada do perfil do aluno.

import time
from llm_config import criar_modelo, QuotaExceededError


def get_student_profile(respostas, dimensoes):
    print("\n***\nInicializando Profiler:")
    start_time = time.time()

    profiler_sys_msg = (
        "Você é um professor universitário experiente, "
        "especialista no modelo de estilos de aprendizagem "
        "de Felder-Silverman. Com base nas respostas do aluno "
        "ao questionário, gere uma descrição do perfil de "
        "aprendizagem deste aluno.\n\n"
        "Instruções importantes:\n"
        "- Não mencione as respostas do aluno diretamente\n"
        "- Não justifique o perfil pelas respostas dadas\n"
        "- Use linguagem clara e acessível\n"
        "- Dirija-se ao aluno usando 'você'\n"
        "- Limite o perfil a 3 ou 4 frases curtas\n"
        "- O perfil deve ser usado para personalizar "
        "materiais didáticos universitários\n\n"
        "As dimensões do modelo Felder-Silverman são:\n"
        "- Compreensão: Sequencial (aprende em etapas) ou "
        "Global (aprende de forma holística)\n"
        "- Percepção: Sensorial (prefere fatos concretos) ou "
        "Intuitivo (prefere conceitos abstratos)\n"
        "- Entrada: Visual (prefere imagens e gráficos) ou "
        "Verbal (prefere textos e explicações)\n"
        "- Processamento: Ativo (aprende fazendo) ou "
        "Reflexivo (aprende pensando)\n\n"
        "Exemplo de perfil gerado:\n"
        "[Você é um estudante que aprende melhor quando o "
        "conteúdo é apresentado de forma organizada e em "
        "etapas progressivas. Você prefere trabalhar com "
        "fatos concretos e exemplos práticos do que com "
        "conceitos abstratos. Textos e explicações escritas "
        "são seus meios preferidos de aprendizagem. Você "
        "gosta de refletir sobre o conteúdo antes de "
        "discuti-lo com outros.]"
    )

    profiler_user_msg = (
        f"O aluno respondeu ao questionário da seguinte forma:\n\n"
        f"1. Dimensão Compreensão  : {dimensoes['compreensao']}\n"
        f"2. Dimensão Percepção    : {dimensoes['percepcao']}\n"
        f"3. Dimensão Entrada      : {dimensoes['entrada']}\n"
        f"4. Dimensão Processamento: {dimensoes['processamento']}\n\n"
        f"Gere o perfil de aprendizagem deste aluno."
    )

    # Cria o modelo dinamicamente com o system message
    model = criar_modelo(system_instruction=profiler_sys_msg)

    # Gera o perfil do aluno com tratamento de quota
    try:
        response = model.generate_content(profiler_user_msg)
        perfil = response.text
    except QuotaExceededError as e:
        print(f"[!] Erro de quota ao gerar o perfil: {e}")
        perfil = "[Perfil não disponível devido a limites de quota]"
        # Opcional: pode implementar fallback ou retry manual aqui

    print(f"Perfil gerado: {perfil}")

    stop_time = time.time()
    print(f"Tempo de execução do Profiler: {(stop_time - start_time):.2f} s\n***\n")

    return perfil
