"""
Sistema Adaptativo de Materiais Educacionais
Baseado no modelo Felder-Silverman + LLM + Prompt Engineering.
"""

import os

from dotenv import load_dotenv
import google.generativeai as genai


# --- Perfil Felder-Silverman (ILS - Index of Learning Styles) ---
# Cada dimensão tem dois polos. O perfil do aluno é definido por um polo em cada dimensão.
DIMENSOES_ILS = {
    "ativo_reflexivo": {
        "Ativo": "aprendem melhor fazendo, experimentando, discutindo; preferem atividades práticas e em grupo.",
        "Reflexivo": "aprendem melhor pensando e analisando antes; preferem tempo para processar e refletir sozinhos.",
    },
    "sensorial_intuitivo": {
        "Sensorial": "preferem fatos concretos, exemplos práticos, procedimentos e aplicações; gostam de detalhes.",
        "Intuitivo": "preferem conceitos, teorias, inovações e relações; gostam de abstrações e possibilidades.",
    },
    "visual_verbal": {
        "Visual": "aprendem melhor com figuras, diagramas, esquemas, mapas conceituais e representações visuais.",
        "Verbal": "aprendem melhor com texto e explicações orais; preferem leitura e discussão em palavras.",
    },
    "sequencial_global": {
        "Sequencial": "aprendem em passos lineares e lógicos; preferem seguir uma ordem clara do mais simples ao complexo.",
        "Global": "aprendem em grandes blocos e precisam ver o quadro geral; preferem visão holística antes dos detalhes.",
    },
}

# --- Questionário Felder-Silverman (versão reduzida) - Etapa 1: Diagnóstico ---
# Uma pergunta por dimensão; opção (a) mapeia para polo_a, opção (b) para polo_b.
QUESTIONARIO_REDUZIDO = [
    {
        "dimensao": "sequencial_global",
        "titulo": "Compreensão (Sequencial/Global)",
        "a": "Quando estudo um novo assunto, prefiro aprender o conteúdo em etapas claras e permanecer focado.",
        "b": "Ter uma visão geral das conexões entre esse assunto e outros relacionados.",
        "polo_a": "Sequencial",
        "polo_b": "Global",
    },
    {
        "dimensao": "sensorial_intuitivo",
        "titulo": "Percepção (Sensorial/Intuitivo)",
        "a": "Prefiro aulas que enfatizem material concreto, como dados e fatos.",
        "b": "Material teórico e conceitual, como teorias e conceitos.",
        "polo_a": "Sensorial",
        "polo_b": "Intuitivo",
    },
    {
        "dimensao": "visual_verbal",
        "titulo": "Entrada (Visual/Verbal)",
        "a": "Quando recebo dados e informações, prefiro concentrar-me em figuras, gráficos e tabelas.",
        "b": "Prestar atenção em explicações orais ou textos escritos que resumam os resultados.",
        "polo_a": "Visual",
        "polo_b": "Verbal",
    },
    {
        "dimensao": "ativo_reflexivo",
        "titulo": "Processamento (Ativo/Reflexivo)",
        "a": "Prefiro aprender em grupo, discutindo o conteúdo com outras pessoas.",
        "b": "Sozinho, refletindo sobre o conteúdo individualmente.",
        "polo_a": "Ativo",
        "polo_b": "Reflexivo",
    },
]


def get_api_key() -> str:
    """
    Obtém a API key do Gemini a partir de:
    - um arquivo .env na pasta do projeto, ou
    - da variável de ambiente GEMINI_API_KEY já exportada no sistema.
    """
    # Carrega variáveis definidas em .env, se o arquivo existir
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Variável de ambiente GEMINI_API_KEY não definida. "
            "Defina sua chave da API do Gemini antes de executar."
        )
    return api_key


def criar_modelo() -> genai.GenerativeModel:
    """
    Configura a SDK e retorna um modelo Gemini disponível para uso.

    Em vez de fixar o nome do modelo (como "gemini-pro" ou "gemini-1.5-flash"),
    fazemos uma listagem dos modelos suportados pela API e escolhemos um que
    tenha o método "generateContent" habilitado.
    """
    api_key = get_api_key()
    genai.configure(api_key=api_key)

    # Descobre dinamicamente um modelo que suporte generateContent
    modelos_disponiveis = []
    for m in genai.list_models():
        if "generateContent" in getattr(m, "supported_generation_methods", []):
            modelos_disponiveis.append(m.name)

    if not modelos_disponiveis:
        raise RuntimeError(
            "Nenhum modelo com suporte a 'generateContent' foi encontrado para esta API key. "
            "Verifique se sua conta tem acesso aos modelos do Gemini."
        )

    nome_modelo = modelos_disponiveis[0]
    print(f"Usando modelo: {nome_modelo}")
    return genai.GenerativeModel(nome_modelo)


# --- Parte de adaptação de conteúdo (comentada por enquanto; ativar após o questionário) ---
# def montar_prompt_adaptacao(perfil: dict[str, str], conteudo: str) -> str:
#     """
#     Monta o prompt de Prompt Engineering para a LLM adaptar o conteúdo
#     ao perfil de aprendizagem Felder-Silverman (Etapa 4 do fluxograma).
#     """
#     descricoes = []
#     for dimensao, polo in perfil.items():
#         if dimensao in DIMENSOES_ILS and polo in DIMENSOES_ILS[dimensao]:
#             descricoes.append(f"- {dimensao.replace('_', ' ').title()}: {polo} ({DIMENSOES_ILS[dimensao][polo]})")
#
#     perfil_texto = "\n".join(descricoes) if descricoes else "Perfil não especificado; adapte de forma equilibrada."
#
#     return f"""Você é um especialista em educação que adapta materiais didáticos ao perfil de aprendizagem do aluno.
#
# ## Perfil do aluno (Felder-Silverman - ILS)
# {perfil_texto}
#
# ## Sua tarefa
# Reescreva e reformate o CONTEÚDO DA DISCIPLINA abaixo para que este aluno aprenda melhor, de acordo com esse perfil. Mantenha a precisão e o rigor do conteúdo, mas:
# - use a linguagem e o formato mais adequados (ex.: mais exemplos concretos, analogias visuais, resumos objetivos, mapas conceituais, perguntas reflexivas, narrativas ou passos sequenciais, conforme o perfil);
# - organize e destaque as ideias de forma que favoreça o estilo de aprendizagem indicado;
# - ao final, inclua uma breve seção "Sugestões de estudo" com 2 ou 3 dicas específicas para esse perfil.
#
# ## Conteúdo da disciplina
# ---
# {conteudo}
# ---
# Responda apenas com o material adaptado (sem meta-comentários sobre o que você fez)."""
#
#
# def adaptar_conteudo(modelo: genai.GenerativeModel, perfil: dict[str, str], conteudo: str) -> str:
#     """
#     Envia conteúdo e perfil à LLM e retorna o material educacional adaptado (saída do fluxograma).
#     """
#     prompt = montar_prompt_adaptacao(perfil, conteudo)
#     resposta = modelo.generate_content(prompt)
#     return resposta.text if resposta.text else ""


def obter_perfil_interativo() -> dict[str, str]:
    """
    Aplica o questionário reduzido Felder-Silverman (Etapa 1) e define o perfil (Etapa 2).
    O aluno responde (a) ou (b) em cada pergunta; o resultado é um dicionário
    dimensão -> polo (ex.: sequencial_global -> "Sequencial" ou "Global").
    """
    perfil = {}
    print("\n--- Questionário Felder-Silverman (versão reduzida) - Etapa 1: Diagnóstico ---")
    print("Para cada pergunta, escolha a opção que mais se aproxima do seu estilo de aprendizagem.")
    print("Digite 'a' ou 'b' e pressione Enter.\n")

    for item in QUESTIONARIO_REDUZIDO:
        print(f"  {item['titulo']}")
        print(f"    (a) {item['a']}")
        print(f"    (b) {item['b']}")
        while True:
            escolha = input("  Sua resposta (a/b): ").strip().lower()
            if escolha in ("a", "b"):
                perfil[item["dimensao"]] = item["polo_a"] if escolha == "a" else item["polo_b"]
                break
            print("  Digite apenas 'a' ou 'b'.")
        print()

    return perfil


# def obter_conteudo_interativo() -> str:
#     """Obtém o conteúdo da disciplina: caminho de arquivo ou texto colado (múltiplas linhas)."""
#     print("\n--- Conteúdo da disciplina ---")
#     print("Digite o caminho de um arquivo .txt (ex: material.txt) ou cole o texto abaixo.")
#     print("Para texto colado, digite uma linha só com 'FIM' para encerrar.\n")
#     primeira = input("Arquivo ou primeira linha do texto: ").strip()
#
#     if primeira.upper() == "FIM":
#         return ""
#
#     if os.path.isfile(primeira):
#         with open(primeira, "r", encoding="utf-8") as f:
#             return f.read()
#
#     linhas = [primeira]
#     while True:
#         linha = input()
#         if linha.strip().upper() == "FIM":
#             break
#         linhas.append(linha)
#     return "\n".join(linhas)


def fluxo_adaptacao_material() -> None:
    """
    Fluxo principal: por enquanto apenas questionário (perfil).
    Após montar o questionário reduzido, reativar: seleção de conteúdo -> adaptação via LLM.
    """
    print("\n=== Sistema Adaptativo de Materiais Educacionais ===")
    print("(Felder-Silverman - Questionário reduzido)\n")

    perfil = obter_perfil_interativo()

    print("\n" + "=" * 60)
    print("PERFIL DE APRENDIZAGEM (Etapa 2 - Classificação)")
    print("=" * 60)
    for dim, polo in perfil.items():
        nome = dim.replace("_", " ").title()
        print(f"  {nome}: {polo}")
    print("=" * 60)

    # --- Adaptação de conteúdo (comentada; reativar após questionário e conteúdo) ---
    # modelo = criar_modelo()
    # conteudo = obter_conteudo_interativo()
    # if not conteudo.strip():
    #     print("Nenhum conteúdo informado. Encerrando.")
    #     return
    # print("\nAdaptando conteúdo ao perfil via LLM...")
    # try:
    #     material_adaptado = adaptar_conteudo(modelo, perfil, conteudo)
    #     print("\n" + "=" * 60)
    #     print("MATERIAL EDUCACIONAL ADAPTADO AO ALUNO")
    #     print("=" * 60 + "\n")
    #     print(material_adaptado)
    #     print("\n" + "=" * 60)
    # except Exception as exc:
    #     print(f"Erro ao adaptar conteúdo: {exc}")


def chat_interativo() -> None:
    """
    Abre um chat simples no terminal com o modelo Gemini.

    - Digite uma pergunta e pressione Enter.
    - Pressione Enter em branco para sair.
    """
    modelo = criar_modelo()

    print("Chat com Gemini iniciado.")
    print("Digite sua pergunta e pressione Enter.")
    print("Pressione Enter em branco para sair.\n")

    while True:
        try:
            prompt = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando chat.")
            break

        if not prompt:
            print("Encerrando chat.")
            break

        try:
            resposta = modelo.generate_content(prompt)
            print("\nGemini:\n")
            print(resposta.text)
            print("\n" + "-" * 60 + "\n")
        except Exception as exc:
            print(f"Ocorreu um erro ao chamar a API do Gemini: {exc}")
            break


def main() -> None:
    """Ponto de entrada do script."""
    print("Sistema Adaptativo de Materiais Educacionais")
    print("1. Adaptar material ao perfil (fluxo Felder-Silverman + LLM)")
    print("2. Chat livre com o Gemini")
    print()
    opcao = input("Escolha (1 ou 2) [1]: ").strip() or "1"
    if opcao == "2":
        chat_interativo()
    else:
        fluxo_adaptacao_material()


if __name__ == "__main__":
    main()

