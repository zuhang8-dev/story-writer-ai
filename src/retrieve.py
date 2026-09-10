import sqlite3
import requests
import json
import numpy as np
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'story.db')
print('資料庫路徑：', os.path.abspath(DB_PATH))
def get_embedding(text):
    """把一段文字轉成向量"""
    response = requests.post(
        'http://127.0.0.1:1234/v1/embeddings',
        json={
            'model': 'text-embedding-bge-m3',
            'input': text
        }
    )
    return response.json()['data'][0]['embedding']

def cosine_similarity(vec1, vec2):
    """計算兩個向量的餘弦相似度"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search(query, top_k=3):
    """輸入一句話，找出資料庫裡最相近的段落"""
    # 第1步：把查詢句子轉成向量
    query_vector = get_embedding(query)

    # 第2步：撈出資料庫裡所有段落的向量
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute('SELECT chunk_id, source, content, embedding FROM chunks').fetchall()
    conn.close()

    # 第3步：計算每一筆的相似度
    results = []
    for chunk_id, source, content, embedding_json in rows:
        chunk_vector = json.loads(embedding_json)
        similarity = cosine_similarity(query_vector, chunk_vector)
        results.append((similarity, source, content))

    # 第4步：依相似度排序，取前 top_k 筆
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_k]

if __name__ == '__main__':
    query = input('請輸入一句話：')
    results = search(query)

    for similarity, source, content in results:
        print(f'\n相似度：{similarity:.4f}（出自《{source}》）')
        print(content[:100])