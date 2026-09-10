import requests
from retrieve import search, get_embedding

def generate_story(prompt_request, top_k=3):
    # 第1步：檢索相關範例
    results = search(prompt_request, top_k=top_k)

    # 第2步：組成範例文字區塊
    examples = ''
    for i, (similarity, source, content) in enumerate(results, 1):
        examples += f'\n【範例{i}】\n{content}\n'

    # 第3步：組成完整 prompt
    full_prompt = f'''你是一位擅長寫細膩內心獨白、感官敘事的小說家。以下是幾段參考文字，僅供風格參考：
{examples}
請注意：以上範例只用來學習敘事語氣、用詞習慣與意象經營方式，不要直接挪用範例中的具體對話、人名或情節內容。

請參考以上文字的敘事風格，寫一段全新的故事內容，主題是：
{prompt_request}

/no_think'''

    # 第4步：丟給 Qwen3 生成
    response = requests.post(
        'http://127.0.0.1:1234/v1/chat/completions',
        json={
            'model': 'qwen3-8b',
            'messages': [
                {'role': 'user', 'content': full_prompt}
            ]
        }
    )

    return response.json()['choices'][0]['message']['content']

if __name__ == '__main__':
    prompt_request = input('請輸入你想寫的場景：')
    story = generate_story(prompt_request)
    print('\n--- 生成結果 ---\n')
    print(story)