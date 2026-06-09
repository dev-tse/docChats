# dochat.py
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import sys

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer('all-MiniLM-L6-v2')

# Все твои функции сюда:
def split_into_chunks(text, chunk_size=50): 
    text_result = []
    text_temp = []
    text_array = text.split()
    for word in text_array:
        text_temp.append(word)
        if len(text_temp) == chunk_size:
            text_result.append(' '.join(text_temp))
            text_temp = []
    text_result.append(' '.join(text_temp))
    text_temp = []
    return text_result
    

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def vector_search(query, knowledge_base, kb_embeddings, top_k=2):
    vector_query = model.encode(query)
    results = []
    for i, chunk in enumerate(knowledge_base):
        score = cosine_similarity(vector_query, kb_embeddings[i])
        results.append((score, chunk))
    results = sorted(results, key=lambda x:x[0], reverse=True)
    results = [chunk for score, chunk in results]
    return results[:top_k]

def ask_with_context(question, knowledge_base, kb_embeddings):
    query = vector_search(question, knowledge_base, kb_embeddings)
    context = "\n".join(query)
    prompt = f"""Контекст:
{context}

Вопрос: {question}

Отвечай только на основе контекста. Если ответа нет в контексте — скажи об этом."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    
    

# Новое — чтение файла:
def load_document(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        return content

# Новое — главный цикл:
def main():
    filepath = sys.argv[1]
    doc = load_document(filepath)
    chunk = split_into_chunks(doc)
    kb_embeddings = model.encode(chunk)
    print(f"📄 Документ загружен: {filepath}")
    print(f"📦 Чанков: {len(chunk)}")
    print("🤖 Задавай вопросы (введи 'выход' чтобы закончить)\n")
    
    while True:
        question = input("Ты: ")
        if question == "выход":
            print("👋 Пока!")
            break
        answer = ask_with_context(question, chunk, kb_embeddings)
        print(f"Бот: {answer}\n")
    pass

main()