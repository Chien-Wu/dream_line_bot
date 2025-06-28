from services.faq_retriever import find_top_faqs
import openai
import os

print("TEST KEY:", os.getenv("OPENAI_API_KEY"))


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(user_id, user_text, user_history=None):
    top_faqs = find_top_faqs(user_text, topn=3)
    faq_block = "\n".join([f"Q: {f['q']}\nA: {f['a']}" for f in top_faqs])

    system_prompt = (
        "你是台灣一起夢想公益協會的智能助理。根據以下FAQ資料，並參考上下文對話，請以親切且專業的語氣回答問題。\n"
        + faq_block
    )

    messages = [{"role": "system", "content": system_prompt}]
    if user_history:
        messages += user_history
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content