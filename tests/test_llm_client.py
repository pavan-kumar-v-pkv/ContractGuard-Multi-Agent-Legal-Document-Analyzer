"""
Tests for LLM Client
Run with: pytest tests/test_llm_client.py
"""

import pytest
import asyncio
from agents.llm_client import LLMClient, LLMConfig, SyncLLMClient

@pytest.mark.asyncio
async def test_basic_generation():
    """
    Test basic text generation
    """
    client = LLMClient()

    response = await client.generate(
        prompt="What is 2+2? Answer in one word.",
        system_prompt="You are a math assistant."
    )

    assert response is not None
    assert len(response) > 0
    print(f"\nLLM said: {response}")

    await client.close()

@pytest.mark.asyncio
async def test_json_generation():
    """
    Test structured JSON output
    """
    client = LLMClient()

    prompt = """
Analyze this contract clause and return JSON:

Claude: "Either party may terminate with 24 hours notice."

Return:
{
    "clause_type": "termination",
    "risk_level": "high|medium|low",
    "issues": ["list", "of", "issues"],
    "fairness_score": 1-10
}
"""

    result = await client.generate_json(prompt)

    assert isinstance(result, dict)
    assert "clause_type" in result
    assert "risk_level" in result
    assert "fairness_score" in result

    print(f"\nJSON output: {result}")

    await client.close()

@pytest.mark.asyncio
async def test_batch_generation():
    """
    Test parallel generation
    """
    client = LLMClient()

    prompts = [
        "What is the capital of Sri Lanka?",
        "what is the colour of ocean?",
        "Who is the CEO of Tesla?",
        "what is 7 multiplied by 64?"
    ]

    responses = await client.batch_generate(prompts)

    assert len(responses) == 4
    assert all(len(r) > 0 for r in responses)

    print("\nBatch responses:")
    for i, r in enumerate(responses):
        print(f"{i+1}. {r}")

    await client.close()

def test_sync_client():
    """
    Test synchronous wrapper
    """
    client = SyncLLMClient()

    response = client.generate("Say hello in one word.")

    assert response is not None
    print(f"\nSync response: {response}")

if __name__ == "__main__":
    # Run tests manually
    print("Testing LLM Client...\n")

    asyncio.run(test_basic_generation())
    asyncio.run(test_json_generation())
    asyncio.run(test_batch_generation())
    test_sync_client()

    print("\nAll tests passed!")