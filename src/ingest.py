from requests import exceptions
import sqlite3

def load_and_split(filepath, source, author):
    # 第1步：讀取檔案內容
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 第2步：統一換行符號（\r\n → \n）
    text = text.replace('\r\n', '\n')

    # 第3步：用空行切成段落 list
    paragraphs = text.split('\n\n')

    # 第4步：清理——去掉頭尾多餘空白，濾掉太短的段落
    chunks = []
    for i,p in enumerate(paragraphs):
        p = p.strip()          # 去掉這段文字前後的空白
        if i==0:
            continue
        if len(p) < 10:     # 太短的段落（例如只有標題）就跳過
            continue
        chunks.append(p)

    return chunks



conn = sqlite3.connect('db/story.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    author TEXT,
    chunk_index INTEGER,
    content TEXT,
    char_count INTEGER
)
''')

try:
    cursor.execute("ALTER TABLE chunks ADD COLUMN embedding TEXT")
except sqlite3.OperationalError:
    pass


files = [
    ('raw_texts/郁達夫_沉淪.txt', '沉淪'),
    ('raw_texts/郁達夫_春風沉醉的晚上.txt', '春風沉醉的晚上'),
    ('raw_texts/郁達夫_薄奠.txt', '薄奠'),
    ('raw_texts/測試文本.txt', '測試文本'),
]

author = '郁達夫'

for filepath, source in files:
    chunks = load_and_split(filepath, source, author)

    for chunk_index, content in enumerate(chunks):
        char_count = len(content)
        cursor.execute('''
            INSERT INTO chunks (source, author, chunk_index, content, char_count)
            VALUES (?, ?, ?, ?, ?)
        ''', (source, author, chunk_index, content, char_count))

    print(f'{source}：存入 {len(chunks)} 個段落')

conn.commit()
conn.close()