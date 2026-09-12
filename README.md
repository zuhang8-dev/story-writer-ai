# story-writer-ai

## 專案目標
地端離線 AI 故事寫作助手——透過 RAG（檢索增強生成）技術，讓 AI 模仿指定文本的敘事風格生成新內容，全程不需連網。

## 技術架構
- **推論引擎**：LM Studio（本地端）
- **對話生成模型**：Qwen3 8B（Q4_K_M 量化）
- **Embedding 模型**：bge-m3（Q8_0 量化）
- **資料庫**：SQLite
- **檢索方式**：向量語意檢索（cosine similarity）
- **API 層**：FastAPI + Uvicorn

## 系統流程
1. 收集公版權文本，依段落切塊，存入 SQLite（`ingest.py`）
2. 對每個段落計算 embedding 向量，存入資料庫（`embed.py`）
3. 使用者輸入場景描述 → 計算查詢向量 → 找出資料庫中語意最相近的段落（`retrieve.py`）
4. 將檢索出的段落作為風格範例，組成 prompt，交由 Qwen3 生成新內容（`generate.py`）
5. 包裝成 REST API，供外部程式呼叫（`api.py`）

## 如何執行

### 1. 環境準備
- 安裝 [LM Studio](https://lmstudio.ai)
- 下載並載入模型：`Qwen3 8B`（Q4_K_M）與 `bge-m3`（Q8_0）
- 啟動 Local Server（預設 `http://127.0.0.1:1234`）

### 2. 安裝 Python 套件
```powershell
pip install requests numpy fastapi uvicorn
```

### 3. 建立語料庫
將公版權文本（.txt，UTF-8 編碼）放入 `raw_texts/`，執行：
```powershell
python src/ingest.py
python src/embed.py
```

### 4. 啟動 API
```powershell
cd src
python -m uvicorn api:app --reload
```
開啟 `http://127.0.0.1:8000/docs` 進行測試。

## 測試語料
選定郁達夫（公版權，1945 年逝世）作品，風格特徵：第一人稱內省獨白、感官細節細膩。收錄《沉淪》《春風沉醉的晚上》《薄奠》，切塊後共 362 段落。

## 已驗證的能力
- ✅ 語意檢索：輸入現代白話能撈出用詞不同、語意相符的段落（相似度 0.6+）
- ✅ 風格一致性：多主題測試皆呈現一致的文風特徵
- ✅ API 化：`/generate` 端點可正常回傳生成結果（HTTP 200）

## 開發過程中解決的問題
- **資料清理**：文章標題與作者行因段落切分規則誤判被存入資料庫，透過位置過濾修正
- **敘事斷裂**：生成結果曾將檢索範例中的對話片段生硬嫁接進新場景，透過明確的 prompt 指示（僅參考風格、不挪用內容）修正
- **生成效率與品質**：發現關閉 Qwen3 思考模式（`/no_think`）可同時提升生成速度與風格貼合度
- **多重 Python 環境衝突**：排查並解決 Anaconda 自動啟動、PATH 未即時載入等環境問題
- **相對路徑問題**：改用 `os.path.dirname(__file__)` 計算絕對路徑，避免因執行位置不同導致資料庫連線失敗

## 未來優化方向
- 檢索層過濾對話比重過高的段落，進一步降低敘事斷裂風險
- 擴充語料規模，測試更多元的風格與主題組合
- 加入檢索品質的量化評估（如 Recall@K）