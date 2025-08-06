from openai import OpenAI


# noinspection PyTypeChecker
def query(client: OpenAI, text: str) -> str:
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
            "vector_store_ids": ["vs_6875d5e70b9881919c06d7e078279292"],
            "max_num_results": 1,
        }],
        tool_choice="auto",
        text={"format": {"type": "json_object"}},
    )
