import json

from openai import OpenAI

from fact_fetch.bot.openai_client import get_openai_client


# noinspection PyTypeChecker
def query(client: OpenAI, text: str):
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
        temperature=0,
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["vs_6893d8d854208191b38588df803cd8e9"],
            "max_num_results": 1,
        }],
        tool_choice="auto",
        text={"format": {"type": "json_object"}},
    )

    return json.loads(response.output_text)


if __name__ == "__main__":
    client = get_openai_client()
    message = "Vegans cant get necessary nutrients"

    result = query(client, message)
    print(result)