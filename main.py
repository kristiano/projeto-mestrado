import os

# main.py
import llm_config  # Deve ser importado ANTES dos módulos que usam criar_modelo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PDF = os.path.join(BASE_DIR, "disciplina.pdf")


def _selecionar_llm() -> str:
    """
    Exibe o menu de seleção de LLM e retorna o provedor escolhido ('gemini' ou 'gpt').
    """
    opcoes = {
        "a": "gpt",
        "1": "gpt",
        "b": "gemini",
        "2": "gemini",
    }

    print("\n" + "="*60)
    print("   SISTEMA DE PERSONALIZAÇÃO DE MATERIAIS DIDÁTICOS")
    print("="*60)
    print("\n  Qual LLM você prefere nesta sessão?")
    print("    a. GPT   (OpenAI)")
    print("    b. GEMINI (Google)")
    print()

    while True:
        escolha = input("  Sua escolha (a/b): ").strip().lower()
        if escolha in opcoes:
            provider = opcoes[escolha]
            nome = "GPT (OpenAI)" if provider == "gpt" else "GEMINI (Google)"
            print(f"\n  ✔ LLM selecionada: {nome}")
            print("="*60)
            return provider
        print("  ⚠ Opção inválida. Digite 'a' para GPT ou 'b' para GEMINI.")


if __name__ == "__main__":

    # ── Etapa 0: Seleção da LLM ──────────────────────────────────
    # provider = _selecionar_llm()
    # Para usar somente Gemini por enquanto
    provider = "gemini"
    print("\n  ✔ LLM selecionada: GEMINI (Google) - Padrão temporário")
    llm_config.set_provider(provider)

    # Importações tardias: só após definir o provedor
    from questionario import aplicar_questionario, mapear_dimensoes, exibir_resultado
    from profiler import get_student_profile
    from leitor_pdf import converter_pdf_para_md
    from rewrite import adaptar_material
    from gerador_pdf import gerar_pdf

    # ── Etapa 1: Questionário JÁ TESTADO
    respostas = aplicar_questionario()
    dimensoes = mapear_dimensoes(respostas)
    exibir_resultado(dimensoes)


    # Etapa 1 - Profiler JÁ TESTADO
    print("\nGerando seu perfil de aprendizagem...")
    perfil = get_student_profile(respostas, dimensoes)
    print(f"\n{perfil}\n")

    # Etapa 2 - Leitura Completa do PDF (VERIFICANDO AINDA)
    print("\nLendo todo o PDF e convertendo para Markdown...")
    caminho_conteudo_md = os.path.join(BASE_DIR, "conteudo.md")
    converter_pdf_para_md(CAMINHO_PDF, caminho_conteudo_md)

    
    # Carrega todo o texto lido em memória para passar para a LLM
    with open(caminho_conteudo_md, "r", encoding="utf-8") as f_md:
        texto_completo = f_md.read()
        
    # A LLM analisa o .md completo e o usuário escolhe o assunto que deseja estudar
    from seletor_conteudo import selecionar_assunto_llm
    assunto_escolhido = selecionar_assunto_llm(texto_completo)
    
    # Passamos o texto de todo o documento e o assunto escolhido para adaptação
    texto_assunto = texto_completo

    # Etapa 2 - Adaptação do material
    print("\nAdaptando o material ao seu perfil de aprendizagem...")
    material_adaptado = adaptar_material(
        perfil=perfil,
        dimensoes=dimensoes,
        assunto=assunto_escolhido,
        texto=texto_assunto,
    )

    # Etapa 2 - Gerar PDF
    caminho_pdf = gerar_pdf(
        material_adaptado=material_adaptado,
        assunto=assunto_escolhido,
        dimensoes=dimensoes,
    )

    print("\n" + "="*60)
    print("   MATERIAL PERSONALIZADO GERADO COM SUCESSO!")
    print("="*60)
    print(f"\n  Arquivo salvo em: {caminho_pdf}\n")
    print("="*60)


