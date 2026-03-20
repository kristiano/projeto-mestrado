import json
from typing import List, Dict, Tuple, Optional

import pdfplumber

from llm_config import criar_modelo
from leitor_pdf import extrair_texto_pagina


def _extrair_amostras_pdf(
    caminho_pdf: str,
    max_paginas: int = 40,
    linhas_por_pagina: int = 12,
    max_chars: int = 12000,
) -> str:
    """
    Extrai uma amostra textual do PDF para a LLM:
    - percorre até max_paginas
    - pega as primeiras linhas_por_pagina de cada página
    - limita max_chars para não ficar pesado.
    """
    partes: List[str] = []
    total_chars = 0

    with pdfplumber.open(caminho_pdf) as pdf:
        total_paginas = len(pdf.pages)
        limite = min(max_paginas, total_paginas)

        for i in range(limite):
            texto_pag = extrair_texto_pagina(pdf.pages[i])
            if not texto_pag:
                continue
            linhas = texto_pag.split("\n")[:linhas_por_pagina]
            bloco = "\n".join(linhas).strip()
            if not bloco:
                continue

            if total_chars + len(bloco) > max_chars:
                break

            partes.append(f"[PÁGINA {i + 1}]\n{bloco}")
            total_chars += len(bloco)

    return "\n\n".join(partes)


def _sugerir_assuntos_com_llm(
    texto_amostra: str,
) -> List[Dict]:
    """
    Usa a LLM para sugerir possíveis assuntos/tópicos da disciplina
    com base em uma amostra do PDF.

    Retorna uma lista de dicionários no formato:
    {
        "id": 1,
        "titulo": "...",
        "descricao": "...",
        "palavras_chave": ["...", "..."]
    }
    """
    if not texto_amostra.strip():
        return []

    system_msg = (
        "Você é um especialista em organização de conteúdo de disciplinas "
        "universitárias. Seu trabalho é ler uma amostra de um material em PDF "
        "e propor possíveis assuntos/tópicos principais dessa disciplina.\n\n"
        "IMPORTANTE: responda ESTRITAMENTE em JSON válido, sem comentários, "
        "sem texto antes ou depois. O formato deve ser:\n"
        "[\n"
        "  {\n"
        '    \"id\": 1,\n'
        '    \"titulo\": \"Título curto do assunto\",\n'
        '    \"descricao\": \"Breve descrição do que é abordado\",\n'
        '    \"palavras_chave\": [\"palavra1\", \"palavra2\"]\n'
        "  },\n"
        "  ...\n"
        "]\n"
    )

    user_msg = (
        "A seguir está uma amostra do conteúdo de uma disciplina.\n"
        "Com base nessa amostra, identifique de 3 a 8 possíveis assuntos/tópicos "
        "principais da disciplina.\n\n"
        "Use palavras-chave que provavelmente aparecem no texto para ajudar a "
        "localizar o assunto depois.\n\n"
        "AMOSTRA DO CONTEÚDO:\n\n"
        f"{texto_amostra}\n"
    )

    model = criar_modelo(system_instruction=system_msg)
    resposta = model.generate_content(user_msg)
    raw = (resposta.text or "").strip()

    try:
        dados = json.loads(raw)
        if isinstance(dados, list):
            # Filtra apenas itens bem formados
            topicos = []
            for item in dados:
                if not isinstance(item, dict):
                    continue
                if "titulo" not in item:
                    continue
                if "id" not in item:
                    continue
                if "palavras_chave" not in item:
                    item["palavras_chave"] = []
                topicos.append(item)
            return topicos
    except Exception:
        print("\nNão foi possível interpretar a resposta da LLM como JSON válido.")

    return []


def _extrair_trecho_por_palavras_chave(
    caminho_pdf: str,
    palavras_chave: List[str],
    max_paginas: int = 80,
) -> str:
    """
    Procura páginas que contenham pelo menos uma das palavras-chave
    (ignorando maiúsculas/minúsculas) e concatena o texto dessas páginas.
    """
    if not palavras_chave:
        return ""

    palavras_norm = [p.lower() for p in palavras_chave if p.strip()]
    if not palavras_norm:
        return ""

    trechos: List[str] = []

    with pdfplumber.open(caminho_pdf) as pdf:
        total_paginas = len(pdf.pages)
        limite = min(max_paginas, total_paginas)

        for i in range(limite):
            texto_pag = extrair_texto_pagina(pdf.pages[i])
            if not texto_pag:
                continue
            texto_lower = texto_pag.lower()
            if any(p in texto_lower for p in palavras_norm):
                trechos.append(texto_pag)

    return "\n\n".join(trechos).strip()


def localizar_assunto_com_llm(
    caminho_pdf: str,
) -> Optional[Tuple[str, str]]:
    """
    Fallback quando não foi possível identificar capítulos com Python.

    Estratégia:
    1. Extrai uma amostra do PDF.
    2. Usa a LLM para sugerir assuntos (título + palavras-chave).
    3. Mostra a lista de assuntos e deixa o usuário escolher.
    4. Usa as palavras-chave do assunto escolhido para extrair,
       via Python, o trecho relevante do PDF.

    Retorna (assunto_escolhido, texto_assunto) ou None em caso de falha/cancelamento.
    """
    print(
        "\nTentando localizar assuntos na disciplina com apoio da LLM "
        "(sem adaptar o conteúdo ainda)..."
    )

    texto_amostra = _extrair_amostras_pdf(caminho_pdf)
    if not texto_amostra.strip():
        print("\nNão foi possível extrair amostras textuais do PDF.")
        return None

    topicos = _sugerir_assuntos_com_llm(texto_amostra)
    if not topicos:
        print(
            "\nA LLM não conseguiu sugerir assuntos de forma confiável. "
            "Operação cancelada."
        )
        return None

    print("\n" + "=" * 60)
    print("   ASSUNTOS SUGERIDOS PELA LLM")
    print("=" * 60)
    for item in topicos:
        tid = item.get("id")
        titulo = item.get("titulo", "").strip()
        desc = item.get("descricao", "").strip()
        print(f"\n  {tid}. {titulo}")
        if desc:
            print(f"     - {desc}")

    print("\nDigite o número do assunto que deseja adaptar.")
    print("Ou pressione Enter em branco para cancelar.")

    escolhido = None
    while True:
        resp = input("\n  Sua escolha: ").strip()
        if not resp:
            print("\nOperação cancelada pelo usuário.")
            return None
        try:
            num = int(resp)
        except ValueError:
            print("  ⚠ Entrada inválida. Digite apenas o número do assunto.")
            continue

        for item in topicos:
            if int(item.get("id")) == num:
                escolhido = item
                break
        if escolhido is None:
            print("  ⚠ ID não encontrado na lista. Tente novamente.")
        else:
            break

    titulo = str(escolhido.get("titulo", "")).strip() or f"Assunto {escolhido['id']}"
    palavras_chave = escolhido.get("palavras_chave") or []

    texto_assunto = _extrair_trecho_por_palavras_chave(
        caminho_pdf, palavras_chave
    )

    # Se não achar nada com as palavras-chave, tenta usar termos do título
    if not texto_assunto.strip():
        extras = [p.strip() for p in titulo.split() if len(p.strip()) > 3]
        texto_assunto = _extrair_trecho_por_palavras_chave(
            caminho_pdf, extras
        )

    if not texto_assunto.strip():
        print(
            "\nNão foi possível localizar no PDF um trecho consistente com "
            "o assunto escolhido. Operação cancelada."
        )
        return None

    print(f"\nAssunto selecionado: {titulo}")
    return titulo, texto_assunto

