# OpenAI api를 호출해서 대화하는 기능

from openai import OpenAI

def ask_llm(prompt: str, openai_key: str, model: str = "gpt-4") -> str: #LLM호출 메인함수
    """
        prompt (str): 사용자 입력 프롬프트.
        openai_key (str): OpenAI API 키.
        model (str): 사용할 모델명. 기본값은 gpt-4.
    Returns:
        str: 응답 메시지 본문.
    """
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def ask_with_history(openai_key: str, messages: list, model: str = "gpt-4") -> str: #messages 리스트전체를 히스토리로 남기기우한함수
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content