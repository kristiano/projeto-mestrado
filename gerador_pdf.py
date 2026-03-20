# gerador_pdf.py
# Geração do material adaptado em PDF formatado
# Usando fpdf2 com fonte Unicode (DejaVu) para suporte completo ao português

import os
import re
from fpdf import FPDF
from datetime import datetime

# Caminhos das fontes DejaVu (via matplotlib)
FONTS_DIR = "/opt/anaconda3/lib/python3.12/site-packages/matplotlib/mpl-data/fonts/ttf"
FONT_REGULAR = f"{FONTS_DIR}/DejaVuSans.ttf"
FONT_BOLD    = f"{FONTS_DIR}/DejaVuSans-Bold.ttf"
FONT_ITALIC  = f"{FONTS_DIR}/DejaVuSans-Oblique.ttf"


class PDFMaterial(FPDF):

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        # Registra a fonte Unicode
        self.add_font("DejaVu", "",  FONT_REGULAR, uni=True)
        self.add_font("DejaVu", "B", FONT_BOLD,    uni=True)
        self.add_font("DejaVu", "I", FONT_ITALIC,  uni=True)

    def header(self):
        self.set_font("DejaVu", "I", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, "Material Didático Personalizado - Felder-Silverman", align="R")
        self.ln(2)
        self.set_draw_color(74, 144, 217)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def limpar_markdown(texto: str) -> str:
    """Remove símbolos Markdown mantendo o texto."""
    texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
    texto = re.sub(r'\*(.+?)\*',     r'\1', texto)
    texto = re.sub(r'`(.+?)`',       r'\1', texto)
    texto = re.sub(r'^#{1,6}\s+', '', texto, flags=re.MULTILINE)
    
    # Limpa Emojis e Ícones: A biblioteca FPDF tem muita dificuldade de renderizar emojis 
    # ou ícones malucos das IAs (mesmo usando a fonte DejaVu).
    # Filtro: qualquer caractere com código acima de U+2500 (emojis, hieróglifos, shapes matemáticos)
    texto = "".join(c for c in texto if ord(c) < 0x2500)
    
    # Previne o FPDFException ("Not enough horizontal space") injetando espaços em 
    # palavras/textos massivos e ininterruptos maiores que 45 caracteres (URLs longas, 
    # ou linhas formatadas com "----" largas construídas pela LLM)
    texto = re.sub(r'([^\s]{45})', r'\1 ', texto)
    
    return texto


def gerar_pdf(
    material_adaptado: str,
    assunto: str,
    dimensoes: dict,
    pasta_saida: str = "materiais_gerados"
) -> str:

    print("\n***\nGerando PDF do material adaptado...")

    os.makedirs(pasta_saida, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_pdf = os.path.join(pasta_saida, f"material_{timestamp}.pdf")

    perfil_texto = (
        f"{dimensoes['compreensao']} | "
        f"{dimensoes['percepcao']} | "
        f"{dimensoes['entrada']} | "
        f"{dimensoes['processamento']}"
    )

    titulo_curto = assunto[:60] + "..." if len(assunto) > 60 else assunto

    pdf = PDFMaterial()

    # ── Capa ──────────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(30)

    pdf.set_font("DejaVu", "B", 22)
    pdf.set_text_color(26, 26, 46)
    pdf.multi_cell(0, 12, "Material Didático Personalizado", align="C")
    pdf.ln(6)

    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(74, 144, 217)
    pdf.multi_cell(0, 10, titulo_curto, align="C")
    pdf.ln(20)

    # Caixa do perfil
    pdf.set_fill_color(240, 244, 255)
    pdf.set_draw_color(74, 144, 217)
    pdf.set_line_width(0.5)
    pdf.rect(30, pdf.get_y(), 150, 28, style="FD")
    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 8, "Perfil de Aprendizagem:", align="C")
    pdf.ln(7)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(74, 144, 217)
    pdf.cell(0, 8, perfil_texto, align="C")
    pdf.ln(20)

    pdf.set_font("DejaVu", "I", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(
        0, 8,
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        align="C"
    )

    # ── Conteúdo ──────────────────────────────────────────────
    pdf.add_page()

    for linha in material_adaptado.split("\n"):
        linha_strip = linha.strip()

        if not linha_strip:
            pdf.ln(4)
            continue

        # H1
        if linha_strip.startswith("# "):
            texto = limpar_markdown(linha_strip[2:].strip())
            pdf.set_font("DejaVu", "B", 16)
            pdf.set_text_color(26, 26, 46)
            pdf.ln(4)
            pdf.multi_cell(0, 9, texto)
            pdf.set_draw_color(74, 144, 217)
            pdf.set_line_width(0.4)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(4)

        # H2
        elif linha_strip.startswith("## "):
            texto = limpar_markdown(linha_strip[3:].strip())
            pdf.set_font("DejaVu", "B", 13)
            pdf.set_text_color(74, 144, 217)
            pdf.ln(3)
            pdf.multi_cell(0, 8, texto)
            pdf.ln(2)

        # H3
        elif linha_strip.startswith("### "):
            texto = limpar_markdown(linha_strip[4:].strip())
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_text_color(51, 51, 51)
            pdf.ln(2)
            pdf.multi_cell(0, 7, texto)
            pdf.ln(1)

        # Lista com marcador
        elif linha_strip.startswith("- ") or linha_strip.startswith("* "):
            texto = limpar_markdown(linha_strip[2:].strip())
            pdf.set_font("DejaVu", "", 11)
            pdf.set_text_color(45, 45, 45)
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_xy(10, y)
            pdf.cell(8, 7, "•")
            pdf.set_xy(18, y)
            pdf.multi_cell(0, 7, texto)

        # Lista numerada
        elif re.match(r'^\d+\.\s', linha_strip):
            texto = limpar_markdown(re.sub(r'^\d+\.\s', '', linha_strip))
            numero = re.match(r'^(\d+)\.', linha_strip).group(1)
            pdf.set_font("DejaVu", "", 11)
            pdf.set_text_color(45, 45, 45)
            y = pdf.get_y()
            pdf.set_xy(10, y)
            pdf.cell(8, 7, f"{numero}.")
            pdf.set_xy(18, y)
            pdf.multi_cell(0, 7, texto)

        # Blockquote
        elif linha_strip.startswith("> "):
            texto = limpar_markdown(linha_strip[2:].strip())
            pdf.set_fill_color(240, 244, 255)
            pdf.set_font("DejaVu", "I", 11)
            pdf.set_text_color(74, 144, 217)
            pdf.multi_cell(0, 7, f"  {texto}", fill=True)
            pdf.ln(1)

        # Parágrafo normal
        else:
            texto = limpar_markdown(linha_strip)
            pdf.set_font("DejaVu", "", 11)
            pdf.set_text_color(45, 45, 45)
            try:
                pdf.multi_cell(0, 7, texto)
            except Exception as e:
                print(f"[DEBUG FPDF ERROR] X: {pdf.get_x()}, MargemL: {pdf.l_margin}, MargemR: {pdf.r_margin}")
                print(f"[DEBUG FPDF TEXTO] {repr(texto)}")
                # Força retorno do cursor para reiniciar margem X caso tenha estourado
                pdf.set_x(pdf.l_margin)
                pdf.ln(4)
                
            pdf.ln(1)

    pdf.output(caminho_pdf)
    print(f"PDF gerado com sucesso: {caminho_pdf}\n***\n")
    return caminho_pdf