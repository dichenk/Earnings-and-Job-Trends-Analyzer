from app.core.config import settings
from together import Together

MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
client = Together(api_key=settings.together_api_key)


async def ask_llm(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """
    Отправляет запрос в LLM и возвращает ответ.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    import asyncio
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=512,
            temperature=0.7
        )
    )
    return response.choices[0].message.content


def explain_result(user_question: str, sql: str, table_text: str, is_empty: bool) -> str:
    """
    Объясняет результат SQL-запроса в человеческом языке.
    """
    if is_empty:
        prompt = (
            f"Пользователь спросил: \"{user_question}\"\n"
            f"Был выполнен SQL-запрос:\n{sql}\n"
            "Результат запроса — пустой (нет данных по заданному условию).\n"
            "Объясни человеческим языком, почему не найдено данных, и что это значит для пользователя. "
            "Пример: 'Нет регионов, где средний рейтинг клиентов выше 4.5. Возможно, средний рейтинг по всем регионам меньше 4.5.'"
        )
    else:
        prompt = (
            f"Пользователь спросил: \"{user_question}\"\n\n"
            f"Результат запроса (таблица):\n{table_text}\n\n"
            "Выведи данные кратко, но в приятной для чтения форме, добавь emoji."
        )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.6,
    )
    return response.choices[0].message.content.strip()


def explain_impossible(user_question: str) -> str:
    prompt = (
        f"Пользователь спросил: \"{user_question}\"\n"
        "Структура таблицы:\n"
        "- Freelancer_ID (integer)\n"
        "- Job_Category (string), только: 'App Development', 'Content Writing', 'Customer Support', 'Data Entry', 'Digital Marketing', 'Graphic Design', 'SEO', 'Web Development'\n"
        "- Platform (string), только: 'Fiverr', 'Freelancer', 'PeoplePerHour', 'Toptal', 'Upwork'\n"
        "- Experience_Level (string), только: 'Beginner', 'Expert', 'Intermediate'\n"
        "- Client_Region (string), только: 'Asia', 'Australia', 'Canada', 'Europe', 'Middle East', 'UK', 'USA'\n"
        "- Payment_Method (string), только: 'Bank Transfer', 'Crypto', 'Mobile Banking', 'PayPal'\n"
        "- Project_Type (string), только: 'Fixed', 'Hourly'\n"
        "- Job_Completed (integer)\n"
        "- Earnings_USD (float)\n"
        "- Hourly_Rate (float)\n"
        "- Job_Success_Rate (float)\n"
        "- Client_Rating (float)\n"
        "- Job_Duration_Days (integer)\n"
        "- Rehire_Rate (float)\n"
        "- Marketing_Spend (float)\n"
        "В таблице нет таких данных (например, отсутствует указанный регион или категория или вообще тупой запрос).\n"
        "Объясни кратко на человеческом языке, почему невозможно ответить на этот вопрос по текущим данным. Не выдумывай ничего."
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=128,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
