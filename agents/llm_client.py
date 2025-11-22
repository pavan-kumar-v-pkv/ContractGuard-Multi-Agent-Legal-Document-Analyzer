"""
LLM CLient for Ollama
Handles all LLM interactions with retry logic and structured outputs.
"""

import httpx
import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import asyncio
from tenacity import retry, wait_fixed, stop_after_attempt, wait_exponential

class LLMConfig(BaseModel):
    """Configuration for LLM"""
    model: str = "qwen2.5:3b"  # Change to your installed model
    base_url: str = "http://localhost:11434"
    temperature: float = 0.1
    max_tokens: int = 4000
    timeout: int = 120

class LLMClient:
    """
    Client for interacting with Ollama LLM
    Handles retries, timeouts, and structured JSON outputs
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.client = httpx.AsyncClient(timeout=self.config.timeout)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        format_json: bool = False
    ) -> str:
        """
        Generate text from LLM
        Args:
            prompt: User prompt
            system_prompt: System instruction (optional)
            format_json: Force JSON output

        Returns:
            Generated text ot JSON string
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.config.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }

        if format_json:
            payload["format"] = "json"

        try:
            response = await self.client.post(
                f"{self.config.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            return result['message']['content']
        
        except httpx.HTTPError as e:
            print(f"LLM Error: {e}")
            raise

    async def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None    
    ) -> Dict[str, Any]:
        """
        Generate structured JSON output
        Args:
            prompt: Must instruct model to output JSON
            system_prompt: Optional system instruction

        Returns:
            Parsed JSON dict
        """

        response = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            format_json=True
        )
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # sometimes model adds markdown, strip it
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            return json.loads(cleaned.strip())
        
    async def batch_generate(
        self,
        prompts: List[str],
        system_prompt: Optional[str] = None
    ) -> List[str]:
        """
        Generate multiple responses in parallel

        Args:
            prompts: List of prompts
            system_prompt: Shared system prompt

        Returns:
            List of responses (same order as prompts)
        """

        tasks = [
            self.generate(prompt, system_prompt)
            for prompt in prompts
        ]

        return await asyncio.gather(*tasks)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_typr, exc_val, exc_tb):
        asyncio.run(self.close())

# Sync wrapper for easier testing
class SyncLLMClient:
    """
    Synchronous wrapper around async LLM client
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.async_client = LLMClient(config)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return asyncio.run(
            self.async_client.generate(prompt, system_prompt)
        )
    
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict:
        return asyncio.run(
            self.async_client.generate_json(prompt, system_prompt)
        )
    
if __name__ == "__main__":
    async def test():
        client = LLMClient()
        response = await client.generate(
            prompt="Analyze this clause: 'Either party may terminate with 24 hours notice.'",
            system_prompt="You are a legal contract analyst."
        )

        print("LLM Response:")
        print(response)

        await client.close()

    asyncio.run(test())