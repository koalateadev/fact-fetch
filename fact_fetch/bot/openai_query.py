import json

from openai import OpenAI

from fact_fetch.bot.openai_client import get_openai_client


# noinspection PyTypeChecker
def query(client: OpenAI, text: str):
    """
    Analyze text for misinformation using OpenAI's GPT-4 with file search capabilities.
    
    This function uses a specialized AI model to evaluate the factual accuracy of text
    against a curated database of scientific research papers. The AI is instructed to
    only use evidence from the provided research documents.
    
    Args:
        client (OpenAI): Authenticated OpenAI client instance
        text (str): The text to analyze for factual accuracy
        
    Returns:
        dict: A JSON object containing:
            - result (str): Classification as "misinformation", "unverifiable", or "verified"
            - rationale (str): Explanation of the AI's reasoning
            - counterargument (str): Evidence-based correction if misinformation detected
            
    Note:
        The function uses a specific vector store ID that contains research papers
        on plant-based diets, sustainability, and related topics. The AI is configured
        to return responses in strict JSON format for consistent parsing.
    """
    # Create the AI response with specialized system prompt and file search
    response = client.responses.create(
        input=[
            {"role": "system", "content":
                """
                    You are a factual assistant. Use only the documents provided via file_search.
                    Evaluate the user's message for factual accuracy. Respond only using the following valid JSON format:
                    {
                        "result": "misinformation | unverifiable | verified",
                        "rationale": "reasoning behind your decision",
                        "counterargument": "persuasive correction if misinformation; otherwise empty string"
                    }
                    Do not include any explanation or text outside the JSON object.
                """
            },
            {"role": "user", "content": text}
        ],
        model="gpt-4-turbo",
        temperature=0,  # Use deterministic responses for consistency
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["vs_6893d8d854208191b38588df803cd8e9"],  # Research papers database
            "max_num_results": 1,  # Limit to most relevant result
        }],
        tool_choice="auto",
        text={"format": {"type": "json_object"}},  # Ensure JSON response format
    )

    return json.loads(response.output_text)


if __name__ == "__main__":
    """
    Test function to verify OpenAI query functionality.
    
    Tests the query function with a sample message about vegan nutrition
    to ensure the AI can properly analyze and classify content.
    """
    client = get_openai_client()
    
    message = "Vegans cant get necessary nutrients"

    result = query(client, message)
    print(result)