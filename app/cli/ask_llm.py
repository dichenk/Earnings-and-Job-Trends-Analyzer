import asyncio
import sys
from app.llm.together_llm import ask_llm, explain_result, explain_impossible
from app.utils.check_sql import check_sql_valid
from app.core.database import AsyncSessionLocal
from sqlalchemy import text
from app.utils.db_exec import exec_sql_and_print
from sqlalchemy.exc import SQLAlchemyError

system_prompt = """
Ты — ассистент для генерации SQL-запросов по базе данных с таблицей freelancer_earnings_bd.
Отвечай только валидным SQL-запросом на стандартном синтаксисе SQL для SQLite.
Не добавляй никакого текста, комментариев, пояснений, только один SQL-запрос.
Если вопрос нельзя решить по данным таблицы, напиши: -- Не могу ответить: нет нужных данных
Используй только перечисленные значения для полей со списком вариантов. Не выдумывай новые значения.
Всегда включай в SQL все ограничения, которые есть в вопросе (например, фильтр по доходу), не упускай ни одно!
Если фильтр не может быть применён, честно возвращай -- Не могу ответить: нет нужных данных.
Структура таблицы:
- Freelancer_ID (integer)
- Job_Category (string), только: 'App Development', 'Content Writing', 'Customer Support', 'Data Entry', 'Digital Marketing', 'Graphic Design', 'SEO', 'Web Development'
- Platform (string), только: 'Fiverr', 'Freelancer', 'PeoplePerHour', 'Toptal', 'Upwork'
- Experience_Level (string), только: 'Beginner', 'Expert', 'Intermediate'
- Client_Region (string), только: 'Asia', 'Australia', 'Canada', 'Europe', 'Middle East', 'UK', 'USA'
- Payment_Method (string), только: 'Bank Transfer', 'Crypto', 'Mobile Banking', 'PayPal'
- Project_Type (string), только: 'Fixed', 'Hourly'
- Job_Completed (integer)
- Earnings_USD (float)
- Hourly_Rate (float)
- Job_Success_Rate (float)
- Client_Rating (float)
- Job_Duration_Days (integer)
- Rehire_Rate (float)
- Marketing_Spend (float)
""".strip()


async def main():
    if len(sys.argv) < 2:
        print("Использование: python -m app.cli.ask_llm \"Ваш вопрос\"")
        return
    prompt = sys.argv[1]
    response = await ask_llm(prompt, system=system_prompt)
    sql = response.strip()
    print(sql)
    is_valid = await check_sql_valid(sql)
    if is_valid:
        table_text = ""
        is_empty = False

        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(text(sql))
                rows = result.fetchall()
                columns = result.keys()
                if not rows:
                    is_empty = True
                else:
                    from tabulate import tabulate
                    table_text = tabulate(rows, headers=columns, tablefmt="github")
            except SQLAlchemyError as e:
                is_empty = True

        summary = explain_result(prompt, sql, table_text, is_empty)
        print(summary)
    else:
        summary = explain_impossible(prompt)
        print(summary)

if __name__ == "__main__":
    asyncio.run(main())
