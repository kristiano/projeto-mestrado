import fitz  # PyMuPDF

def extrair_texto_pagina(pagina) -> str:
    """Extrai texto de uma página de forma genérica para qualquer PDF."""
    texto = pagina.get_text()
    if not texto:
        return ""
    # Apenas retorna o texto extraído preservando as quebras de linha
    return texto.strip()


def converter_pdf_para_md(caminho_pdf: str, caminho_md: str) -> str:
    """
    Lê todo o conteúdo de um PDF página por página, sem procurar por sumários,
    e salva o texto completo documentado em um arquivo Markdown (.md).
    Retorna o caminho do arquivo gerado para que possa ser lido pela LLM.
    """
    print(f"\nExtraindo todo o conteúdo de: {caminho_pdf} usando PyMuPDF (fitz)")
    texto_completo = []

    doc = fitz.open(caminho_pdf)
    total_paginas = len(doc)
    print(f"Lendo um total de {total_paginas} páginas...")
    
    for pagina in doc:
        texto = extrair_texto_pagina(pagina)
        if texto:
            texto_completo.append(texto)
            
    doc.close()
            
    # Une todo o texto extraído com quebras de linha duplas para organizar os parágrafos
    conteudo_final = "\n\n".join(texto_completo)
    
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(conteudo_final)
        
    print(f"Arquivo MD gerado com sucesso em: {caminho_md}")
    return caminho_md