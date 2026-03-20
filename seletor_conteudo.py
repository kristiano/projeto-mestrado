# seletor_conteudo.py
import json
from typing import List, Dict
from llm_config import criar_modelo

def buscar_assuntos_com_llm(texto_completo: str) -> List[Dict]:
    """
    Usa a LLM para sugerir possíveis assuntos/tópicos com base em todo o conteúdo em Markdown.
    """
    if not texto_completo.strip():
        return []

    system_msg = (
        "Você é um especialista em organização de conteúdo didático. "
        "Leia o material fornecido e proponha possíveis assuntos ou capítulos "
        "principais que o aluno possa escolher para estudar.\n\n"
        "IMPORTANTE: responda ESTRITAMENTE em JSON válido, sem texto adicional. O formato deve ser:\n"
        "[\n"
        "  {\n"
        '    "id": 1,\n'
        '    "titulo": "Título do assunto",\n'
        '    "descricao": "Breve descrição"\n'
        "  },\n"
        "  ...\n"
        "]\n"
    )

    user_msg = (
        "Com base em todo o material a seguir, identifique de 3 a 10 possíveis "
        "assuntos principais.\n\n"
        "MATERIAL:\n\n"
        f"{texto_completo}\n"
    )

    model = criar_modelo(system_instruction=system_msg)
    resposta = model.generate_content(user_msg)
    raw = (resposta.text or "").strip()

    # Previne que a LLM adicione as tags e formatação ```json
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    try:
        dados = json.loads(raw)
        if isinstance(dados, list):
            return [item for item in dados if isinstance(item, dict) and "titulo" in item]
    except Exception as e:
        print("\nErro ao interpretar a resposta da LLM como JSON:", e)

    return []


def selecionar_assunto_llm(texto_completo: str) -> str:
    """
    Aciona a LLM para ler o arquivo Markdown, listar os assuntos e
    pedir para o usuário escolher um no terminal.
    Retorna o título do assunto escolhido.
    """
    print("\nA LLM está lendo o arquivo Markdown para identificar os possíveis assuntos...")
    topicos = buscar_assuntos_com_llm(texto_completo)

    if not topicos:
        print("\nA LLM não conseguiu extrair tópicos do documento. Retornando ao modo completo.")
        return "Conteúdo Completo da Disciplina"

    print("\n" + "="*60)
    print("   ASSUNTOS IDENTIFICADOS PELA LLM NO ARQUIVO .MD")
    print("="*60)
    for t in topicos:
        tid = t.get("id", "-")
        titulo = t.get("titulo", "")
        desc = t.get("descricao", "")
        print(f"\n  {tid}. {titulo}")
        if desc:
            print(f"     - {desc}")

    print("\n" + "="*60)
    while True:
        escolha = input("\n  Digite o número do assunto que deseja estudar: ").strip()
        try:
            num = int(escolha)
            for t in topicos:
                if t.get("id") == num:
                    assunto = t.get("titulo", "")
                    print(f"\n  ✔ Assunto selecionado: {assunto}")
                    return assunto
            print("  ⚠ Número não encontrado na lista.")
        except ValueError:
            print("  ⚠ Digite apenas o número correspondente.")
            
    return "Conteúdo Completo da Disciplina"