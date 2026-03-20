# llm_config.py
# Módulo de roteamento entre LLMs (Gemini e GPT)
# A sessão atual é definida pelo usuário na inicialização do main.py.

import os
from typing import Optional

# ------------------------------------------------------------------
# Estado da sessão — definido uma única vez em main.py
# ------------------------------------------------------------------
_LLM_PROVIDER: Optional[str] = None   # "gemini" | "gpt"


def set_provider(provider: str) -> None:
    """Define o provedor de LLM para a sessão atual."""
    global _LLM_PROVIDER
    provider = provider.strip().lower()
    if provider not in ("gemini", "gpt"):
        raise ValueError(f"Provedor inválido: '{provider}'. Use 'gemini' ou 'gpt'.")
    _LLM_PROVIDER = provider


def get_provider() -> str:
    """Retorna o provedor atual; lança erro se ainda não foi definido."""
    if _LLM_PROVIDER is None:
        raise RuntimeError(
            "Provedor de LLM não definido. Chame set_provider() antes de criar modelos."
        )
    return _LLM_PROVIDER


# ------------------------------------------------------------------
# Wrapper de modelo GPT (interface compatível com criar_modelo do Gemini)
# ------------------------------------------------------------------
class _GPTModel:
    """
    Wrapper leve sobre a API da OpenAI para expor a mesma interface
    que o genai.GenerativeModel usado no Gemini:

        model = criar_modelo(system_instruction="...")
        response = model.generate_content("mensagem do usuário")
        text = response.text
    """

    def __init__(self, system_instruction: Optional[str] = None, model_name: str = "gpt-4o-mini"):
        self.system_instruction = system_instruction
        self.model_name = model_name

    def generate_content(self, user_message: str) -> "_GPTResponse":
        from openai import OpenAI
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY não encontrada no arquivo .env. "
                "Verifique se a chave está configurada corretamente."
            )

        client = OpenAI(api_key=api_key)

        messages = []
        if self.system_instruction:
            messages.append({"role": "system", "content": self.system_instruction})
        messages.append({"role": "user", "content": user_message})

        completion = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )

        text = completion.choices[0].message.content or ""
        return _GPTResponse(text)


class _GPTResponse:
    """Resposta simples com atributo .text, compatível com a resposta do Gemini."""

    def __init__(self, text: str):
        self.text = text


# ------------------------------------------------------------------
# Função pública principal — use no lugar de gemini_config.criar_modelo
# ------------------------------------------------------------------
def criar_modelo(system_instruction: Optional[str] = None):
    """
    Cria e retorna um modelo de LLM com base no provedor da sessão atual.
    A interface retornada expõe sempre:
        response = model.generate_content(user_message: str)
        print(response.text)
    """
    provider = get_provider()

    if provider == "gemini":
        # Importação tardia para não carregar SDK do Gemini se o usuário escolheu GPT
        from gemini_config import criar_modelo as _criar_modelo_gemini
        return _criar_modelo_gemini(system_instruction=system_instruction)

    elif provider == "gpt":
        print(f"Usando modelo: gpt-4o-mini")
        return _GPTModel(system_instruction=system_instruction, model_name="gpt-4o-mini")


# ------------------------------------------------------------------
# Re-exporta QuotaExceededError do Gemini para manter compatibilidade
# com módulos que importam de llm_config
# ------------------------------------------------------------------
class QuotaExceededError(Exception):
    """Erro de cota da API (Gemini). Re-exportado para compatibilidade."""
    pass
