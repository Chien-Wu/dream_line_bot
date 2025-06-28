# tools/embed_faq.py (新版 openai 寫法)
import json, numpy as np, openai, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("data/faq.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

faq_questions = [x["q"] for x in faqs]
faq_embeddings = []

for question in faq_questions:
    # 新版 SDK 寫法
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )
    emb = response.data[0].embedding
    faq_embeddings.append(emb)

faq_embeddings = np.array(faq_embeddings)
np.save("data/faq_embeddings.npy", faq_embeddings)
print("FAQ embedding 檔案已建立，共", len(faq_embeddings), "筆。")