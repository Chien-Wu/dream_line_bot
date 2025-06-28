import numpy as np, openai, json

with open("data/faq.json", "r", encoding="utf-8") as f:
    FAQ_LIST = json.load(f)
FAQ_EMB = np.load("data/faq_embeddings.npy")

def find_top_faqs(user_question, topn=3):
    q_emb = openai.embeddings.create(
        model="text-embedding-3-small", input=user_question
    ).data[0].embedding
    sims = FAQ_EMB @ np.array(q_emb) / (
        np.linalg.norm(FAQ_EMB, axis=1) * np.linalg.norm(q_emb) + 1e-9)
    idx = sims.argsort()[-topn:][::-1]
    return [FAQ_LIST[i] for i in idx]