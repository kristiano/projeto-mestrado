# gerador_imagens.py
# Geração de imagens personalizadas baseadas no estilo de aprendizado do aluno
# Usando a API do Gemini para geração de imagens

import os
import re
import time
from typing import List, Tuple, Optional
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from gemini_config import get_api_key


def extrair_descricoes_imagens(texto: str) -> List[Tuple[str, int]]:
    """
    Extrai descrições de imagens/diagramas do texto adaptado.
    
    Procura por padrões como:
    - [INSERIR IMAGEM: descrição]
    - [INSERIR DIAGRAMA: descrição]
    - [INSERIR GRÁFICO: descrição]
    - [INSERIR INFOGRÁFICO: descrição]
    - [INSERIR FLUXOGRAMA: descrição]
    - [IMAGEM: descrição]
    - [DIAGRAMA: descrição]
    
    Retorna uma lista de tuplas (descrição, posição_no_texto)
    """
    padroes = [
        r'\[INSERIR\s+IMAGEM:\s*(.+?)\]',
        r'\[INSERIR\s+DIAGRAMA:\s*(.+?)\]',
        r'\[INSERIR\s+GRÁFICO:\s*(.+?)\]',
        r'\[INSERIR\s+INFOGRÁFICO:\s*(.+?)\]',
        r'\[INSERIR\s+FLUXOGRAMA:\s*(.+?)\]',
        r'\[INSERIR\s+ESQUEMA:\s*(.+?)\]',
        r'\[INSERIR\s+MAPA\s+CONCEITUAL:\s*(.+?)\]',
        r'\[INSERIR\s+MAPA\s+VISUAL:\s*(.+?)\]',
        r'\[INSERIR\s+PAINEL:\s*(.+?)\]',
        r'\[INSERIR\s+QUADRO:\s*(.+?)\]',
    ]
    
    descricoes_encontradas = []
    
    for padrao in padroes:
        matches = re.finditer(padrao, texto, re.IGNORECASE)
        for match in matches:
            descricao = match.group(1).strip()
            posicao = match.start()
            
            # Remove colchetes e marcações internas se houver
            descricao = re.sub(r'\[.*?\]', '', descricao).strip()
            
            if descricao and (descricao, posicao) not in descricoes_encontradas:
                descricoes_encontradas.append((descricao, posicao))
    
    # Ordena por posição no texto
    descricoes_encontradas.sort(key=lambda x: x[1])
    
    return descricoes_encontradas


def criar_prompt_imagem(descricao: str, dimensoes: dict, contexto: str = "") -> str:
    """
    Cria um prompt enriquecido para geração de imagem baseado no estilo de aprendizado.
    
    Parâmetros:
    - descricao: descrição original da imagem extraída do texto
    - dimensoes: dicionário com as dimensões de Felder-Silverman do aluno
    - contexto: contexto adicional do conteúdo
    
    Retorna: prompt otimizado em inglês para melhor geração de imagens
    """
    
    # Mapeia estilos visuais baseados nas dimensões
    estilo_visual = ""
    nivel_detalhe = ""
    tipo_imagem = "educational illustration"
    
    # Baseado na dimensão de Percepção (Sensorial vs Intuitivo)
    if dimensoes.get('percepcao', '').lower() == 'sensorial':
        estilo_visual = "realistic, concrete examples from daily life, practical applications, clear and tangible elements"
        nivel_detalhe = "highly detailed with real-world textures and familiar objects"
    else:  # Intuitivo
        estilo_visual = "abstract, conceptual, theoretical diagrams, symbolic representations, innovative visual metaphors"
        nivel_detalhe = "focus on concepts and relationships rather than concrete details"
    
    # Baseado na dimensão de Entrada (Visual já é assumido, mas refinamos)
    if dimensoes.get('entrada', '').lower() == 'visual':
        tipo_imagem = "detailed educational infographic"
    
    # Baseado na dimensão de Processamento (Ativo vs Reflexivo)
    if dimensoes.get('processamento', '').lower() == 'ativo':
        estilo_visual += ", dynamic composition, engaging colors, elements that suggest interaction"
    else:  # Reflexivo
        estilo_visual += ", clean layout, contemplative design, space for mental processing"
    
    # Baseado na dimensão de Compreensão (Global vs Sequencial)
    if dimensoes.get('compreensao', '').lower() == 'global':
        tipo_imagem = "holistic overview diagram showing connections between all elements"
        estilo_visual += ", big picture view, interconnected elements, comprehensive visualization"
    else:  # Sequencial
        tipo_imagem = "step-by-step sequential diagram showing logical progression"
        estilo_visual += ", linear flow, numbered steps, incremental building of concepts"
    
    # Traduz termos comuns para inglês (API funciona melhor em inglês)
    traducoes = {
        'diagrama': 'diagram',
        'gráfico': 'chart',
        'fluxograma': 'flowchart',
        'infográfico': 'infographic',
        'esquema': 'scheme',
        'tabela': 'table',
        'mapa conceitual': 'concept map',
        'mapa mental': 'mind map',
        'mapa visual': 'visual map',
        'painel': 'panel',
        'quadro': 'framework',
    }
    
    descricao_en = descricao
    for pt, en in traducoes.items():
        descricao_en = re.sub(rf'\b{pt}\b', en, descricao_en, flags=re.IGNORECASE)
    
    # Constrói o prompt final
    prompt_final = (
        f"{tipo_imagem}, {descricao_en}. "
        f"Style: {estilo_visual}. "
        f"Detail level: {nivel_detalhe}. "
        f"Educational material for university student. "
        f"Professional quality, high resolution, clear and pedagogical. "
        f"Portuguese labels and text if needed. "
        f"White or light background for clarity."
    )
    
    return prompt_final


def gerar_imagem_gemini(prompt: str, pasta_saida: str = "imagens_geradas") -> Optional[str]:
    """
    Gera uma imagem usando a API do Gemini (modelo Imagen via Gemini).
    
    Parâmetros:
    - prompt: prompt para geração da imagem
    - pasta_saida: pasta onde a imagem será salva
    
    Retorna: caminho da imagem gerada ou None se falhar
    """
    try:
        print(f"  → Gerando imagem com Gemini (Imagen)...")
        
        api_key = get_api_key()
        genai.configure(api_key=api_key)
        
        # Usa o modelo Gemini 2.0 Flash com geração de imagens (Imagen)
        model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        
        # Configurações para geração de imagem
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Processa a resposta para extrair a imagem
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            content = candidate.content
            
            # Procura por dados de imagem na resposta
            imagem_data = None
            
            # Tenta encontrar a imagem em diferentes formatos
            if hasattr(content, 'parts'):
                for part in content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        imagem_data = part.inline_data
                        break
                    elif hasattr(part, 'data') and part.data:
                        imagem_data = part.data
                        break
            
            # Se não encontrou inline_data, tenta acessar diretamente
            if not imagem_data and hasattr(response, 'images'):
                imagem_data = response.images[0] if response.images else None
            
            if imagem_data:
                # Salva a imagem
                os.makedirs(pasta_saida, exist_ok=True)
                timestamp = int(time.time() * 1000)
                nome_arquivo = f"imagem_{timestamp}.png"
                caminho_completo = os.path.join(pasta_saida, nome_arquivo)
                
                # Converte e salva
                if isinstance(imagem_data, Image.Image):
                    imagem_data.save(caminho_completo)
                elif isinstance(imagem_data, bytes):
                    with open(caminho_completo, 'wb') as f:
                        f.write(imagem_data)
                elif hasattr(imagem_data, 'mime_type') and hasattr(imagem_data, 'data'):
                    # É um objeto InlineData
                    with open(caminho_completo, 'wb') as f:
                        f.write(imagem_data.data)
                elif hasattr(imagem_data, 'read'):
                    with open(caminho_completo, 'wb') as f:
                        f.write(imagem_data.read())
                else:
                    print(f"  ⚠ Formato de imagem não suportado: {type(imagem_data)}")
                    print(f"  Conteúdo da resposta: {response}")
                    return None
                
                print(f"  ✓ Imagem gerada: {caminho_completo}")
                return caminho_completo
        
        # Tenta abordagem alternativa com resposta direta
        if hasattr(response, 'text') and response.text:
            print(f"  ⚠ Resposta em texto recebida em vez de imagem: {response.text[:200]}...")
        
        print(f"  ⚠ Nenhuma imagem retornada pela API")
        print(f"  Resposta completa: {response}")
        return None
            
    except Exception as e:
        print(f"  ✗ Erro ao gerar imagem: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def gerar_imagem_fallback(prompt: str, pasta_saida: str = "imagens_geradas") -> Optional[str]:
    """
    Método fallback para geração de imagem usando APIs alternativas.
    Pode ser implementado com DALL-E, Stable Diffusion, etc.
    """
    print(f"  → Tentando método fallback para geração de imagem...")
    # Implementação futura para outras APIs
    return None


def substituir_placeholders_por_imagens(
    texto: str, 
    dimensoes: dict,
    pasta_imagens: str = "imagens_geradas",
    max_imagens: int = 5
) -> Tuple[str, List[str]]:
    """
    Substitui placeholders de imagens no texto por imagens reais geradas.
    
    Parâmetros:
    - texto: texto adaptado contendo placeholders
    - dimensoes: dimensões de Felder-Silverman do aluno
    - pasta_imagens: pasta para salvar imagens geradas
    - max_imagens: número máximo de imagens a gerar
    
    Retorna:
    - texto_modificado: texto com caminhos das imagens inseridos
    - lista_imagens: lista de caminhos das imagens geradas
    """
    print("\n***\nIniciando geração de imagens personalizadas...")
    start_time = time.time()
    
    # Extrai todas as descrições de imagens
    descricoes = extrair_descricoes_imagens(texto)
    
    if not descricoes:
        print("Nenhuma descrição de imagem encontrada no texto.")
        print("Dica: Os prompts de adaptação devem incluir sugestões como [INSERIR DIAGRAMA: ...]")
        return texto, []
    
    print(f"Encontradas {len(descricoes)} descrições de imagens no texto.")
    
    imagens_geradas = []
    texto_modificado = texto
    
    # Limita o número de imagens para não exceder quotas
    descricoes_para_gerar = descricoes[:max_imagens]
    
    for idx, (descricao, posicao) in enumerate(descricoes_para_gerar, 1):
        print(f"\nImagem {idx}/{len(descricoes_para_gerar)}:")
        print(f"  Descrição: {descricao[:100]}...")
        
        # Cria prompt enriquecido baseado no perfil do aluno
        prompt_enriquecido = criar_prompt_imagem(descricao, dimensoes)
        
        # Tenta gerar imagem com Gemini
        caminho_imagem = gerar_imagem_gemini(prompt_enriquecido, pasta_imagens)
        
        # Fallback se necessário
        if not caminho_imagem:
            caminho_imagem = gerar_imagem_fallback(prompt_enriquecido, pasta_imagens)
        
        if caminho_imagem:
            imagens_geradas.append(caminho_imagem)
            
            # Substitui o placeholder no texto pelo caminho da imagem
            placeholder_padrao = re.escape("[INSERIR") + r".*?" + re.escape(descricao) + re.escape("]")
            marcador_imagem = f"[IMAGEM_GERADA:{caminho_imagem}]"
            texto_modificado = re.sub(placeholder_padrao, marcador_imagem, texto_modificado, count=1, flags=re.IGNORECASE)
            
            print(f"  ✓ Imagem inserida no texto")
        else:
            print(f"  ✗ Não foi possível gerar esta imagem")
            # Mantém o placeholder original ou marca como falha
            marcador_falha = f"[IMAGEM_NAO_GERADA:{descricao}]"
            placeholder_padrao = re.escape("[INSERIR") + r".*?" + re.escape(descricao) + re.escape("]")
            texto_modificado = re.sub(placeholder_padrao, marcador_falha, texto_modificado, count=1, flags=re.IGNORECASE)
    
    stop_time = time.time()
    print(f"\nTempo total de geração de imagens: {(stop_time - start_time):.2f} s")
    print(f"Imagens geradas com sucesso: {len(imagens_geradas)}/{len(descricoes_para_gerar)}")
    print("***\n")
    
    return texto_modificado, imagens_geradas


if __name__ == "__main__":
    # Teste básico
    texto_teste = """
    Este é um exemplo de conteúdo.
    [INSERIR DIAGRAMA: Fluxo do processo de aprendizagem mostrando entrada, processamento e saída]
    Mais texto aqui.
    [INSERIR GRÁFICO: Comparação entre estilos ativo e reflexivo]
    """
    
    dimensoes_teste = {
        'compreensao': 'Sequencial',
        'percepcao': 'Sensorial',
        'entrada': 'Visual',
        'processamento': 'Ativo'
    }
    
    descricoes = extrair_descricoes_imagens(texto_teste)
    print(f"Descrições encontradas: {descricoes}")
    
    for descricao, _ in descricoes:
        prompt = criar_prompt_imagem(descricao, dimensoes_teste)
        print(f"\nPrompt gerado: {prompt}")
