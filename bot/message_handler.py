from services.faq_retriever import find_top_faqs
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(user_id, user_text, user_history=None):
    top_faqs = find_top_faqs(user_text, topn=3)
    faq_block = "\n".join([f"Q: {f['q']}\nA: {f['a']}" for f in top_faqs])

    system_prompt = (
        "你是台灣一起夢想公益協會的服務大使，以熱情公益與親切的語氣回答問題。參考以下FAQ資料與上下文。\n"
        + faq_block
    )

    messages = [{"role": "system", "content": system_prompt}]
    if user_history:
        messages += user_history
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    return response.choices[0].message.content