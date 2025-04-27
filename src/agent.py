import os
from openai import OpenAI

class OpenAIChatAgent:
    def __init__(self, api_key: str = None, model: str = "gpt-4o-2024-08-06"):
        """
        Initializes the chat agent with an OpenAI client and model.

        Args:
            api_key (str, optional): OpenAI API key. If None, reads from environment variable.
            model (str): Default model to use for completions.
        """
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model
        self.rate_in = 2.5   # $ per 1M input tokens
        self.rate_out = 10.0 # $ per 1M output tokens

    def list_models(self):
        """Lists available models."""
        models = self.client.models.list()
        print("=== MODELOS DISPONIBLES ===")
        for model in models.data:
            print(model.id)

    def chat(self, prompt: str, system_prompt: str = "Eres un asistente útil para responder preguntas complejas con razonamiento, recordá que si las salidas incluyen fórmulas debes incluir un formato compatible con Latex o Markdown (ejemplo: usando $ o $$ para fórmulas).", temperature: float = 0.7, max_tokens: int = 10000):
        """
        Sends a chat completion request.

        Args:
            prompt (str): The user's prompt.
            system_prompt (str): System role description.
            temperature (float): Sampling temperature.
            max_tokens (int): Maximum tokens for the response.

        Returns:
            dict: Contains response text, token usage, and cost.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        usage = response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        cost_in = prompt_tokens * (self.rate_in / 1_000_000)
        cost_out = completion_tokens * (self.rate_out / 1_000_000)
        cost_total = cost_in + cost_out

        return {
            "response": response.choices[0].message.content.strip(),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_in": cost_in,
            "cost_out": cost_out,
            "cost_total": cost_total,
        }

# Example usage
if __name__ == "__main__":
    agent = OpenAIChatAgent()

    agent.list_models()

    prompt = '''Calcula el contenido total de azúcar en un lote de vino a partir de los siguientes datos:
        1. Volumen total del lote: 850 litros
        2. Concentración promedio de azúcar residual: 4.5 gramos por litro
        3. Se deben considerar pérdidas del 2% por evaporación durante el embotellado
        4. Además, aplica un ajuste de +0.5 gramos por litro para corregir mediciones instrumentales

        Razona paso por paso, genera los resultados parciales y luego suma para llegar al resultado total.'''

    result = agent.chat(prompt)

    print("=== RESPUESTA DEL MODELO ===")
    print(result["response"], "\n")

    print("=== USO DE TOKENS ===")
    print(f"Tokens de entrada : {result['prompt_tokens']}")
    print(f"Tokens de salida  : {result['completion_tokens']}")
    print(f"Total tokens      : {result['total_tokens']}\n")

    print("=== COSTO (USD) ===")
    print(f"Costo entrada : ${result['cost_in']:.6f}")
    print(f"Costo salida  : ${result['cost_out']:.6f}")
    print(f"Costo total   : ${result['cost_total']:.6f}")
