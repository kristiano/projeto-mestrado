import os

# main.py
from questionario import aplicar_questionario, mapear_dimensoes, exibir_resultado
from profiler import get_student_profile
from leitor_pdf import converter_pdf_para_md
from rewrite import adaptar_material
from gerador_pdf import gerar_pdf
from gerador_imagens import substituir_placeholders_por_imagens

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PDF = os.path.join(BASE_DIR, "disciplina.pdf")  # <--- Apontando para o PDF NOVO!


if __name__ == "__main__":
    

    # A API é configurada automaticamente no gemini_config.py

    
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

    # Etapa 3 - Gerar imagens personalizadas com Gemini
    print("\nGerando imagens detalhadas personalizadas para seu estilo de aprendizado...")
    material_com_imagens, lista_imagens = substituir_placeholders_por_imagens(
        texto=material_adaptado,
        dimensoes=dimensoes,
        pasta_imagens="imagens_geradas",
        max_imagens=5  # Limite de imagens por questão de quota
    )
    
    # Usa o material com imagens para gerar o PDF
    material_final = material_com_imagens

    # Etapa 4 - Gerar PDF
    caminho_pdf = gerar_pdf(
        material_adaptado=material_final,
        assunto=assunto_escolhido,
        dimensoes=dimensoes,
    )

    print("\n" + "="*60)
    print("   MATERIAL PERSONALIZADO GERADO COM SUCESSO!")
    print("="*60)
    print(f"\n  Arquivo salvo em: {caminho_pdf}\n")
    if lista_imagens:
        print(f"  Imagens geradas: {len(lista_imagens)}")
        for img in lista_imagens:
            print(f"    - {img}")
    print("="*60)


