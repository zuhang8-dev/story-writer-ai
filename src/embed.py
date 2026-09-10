import sqlite3
import requests
import json

conn = sqlite3.connect('db/story.db')
cursor = conn.cursor()

# 第1步：撈出所有段落
rows = cursor.execute('SELECT chunk_id, content FROM chunks').fetchall()

print(f'總共 {len(rows)} 筆段落，開始轉換向量...')

for chunk_id, content in rows:
    # 第2步：呼叫 embedding API
    response = requests.post(
        'http://127.0.0.1:1234/v1/embeddings',
        json={
            'model': 'text-embedding-bge-m3',
            'input': content
        }
    )
    vector = response.json()['data'][0]['embedding']

    # 第3步：轉成 JSON 字串
    vector_json = json.dumps(vector)

    # 第4步：寫回資料庫
    cursor.execute(
        'UPDATE chunks SET embedding = ? WHERE chunk_id = ?',
        (vector_json, chunk_id)
    )

    if chunk_id % 50 == 0:
        print(f'已處理 {chunk_id} / {len(rows)}')

conn.commit()
conn.close()
print('全部完成！')