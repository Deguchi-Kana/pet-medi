## 🐶 ペットの薬管理アプリ 😼
更新日：2025/08/06
### 📝 概要

ペットの服薬スケジュールを登録・可視化できるWebアプリです。
薬の名前や投薬タイミング、開始日・服薬期間などを登録すると、カレンダー上に表示されます。

---

### 📦 技術スタック

| 項目      | 内容                          |
|---------|-----------------------------|
| フロントエンド | Vue 3 + Vite + FullCalendar |
| バックエンド  | FastAPI + SQLAlchemy        |
| DB      | SQLite（開発環境）                |
| その他     | Docker / Docker Compose     |

---

### 🔧 機能一覧

* ペットの薬の登録・更新・削除
* 通知設定のON/OFF（※準備中）
* 薬のスケジュールをカレンダー表示（FullCalendar）
* 期間・服薬タイミング（朝・昼・夜など）の管理

---

### 🚀 セットアップ方法（開発環境）

#### 1. リポジトリをクローン

```bash
git clone https://github.com/your-name/pet-medi-app.git
cd pet-medi-app
```

#### 2. Docker起動

```bash
docker compose up --build
```

#### 3. APIドキュメント確認

[http://localhost:8000/docs](http://localhost:8000/docs) でFastAPIのSwaggerが開けます。

---

### 📅 カレンダー表示について

薬の服薬スケジュールは `/medicines/schedule` API から取得し、Vueの FullCalendar に反映されます。

#### APIレスポンス例：

```json
[
  {
    "date": "2025-08-10",
    "medicine_name": "フィラリア薬",
    "timing": ["朝"]
  },
  {
    "date": "2025-08-11",
    "medicine_name": "アモキシシリン",
    "timing": ["夜"]
  }
]
```

---

### 📁 ディレクトリ構成（簡略）

```
pet-medi-app/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── database.py
├── frontend/
│   └── src/
│       └── components/
│       └── views/
│       └── App.vue
├── docker-compose.yml
```

---

### ✍️ 今後の予定

* [ ] 通知機能（Slack or LINE連携など）
* [ ] ユーザーごとの認証機能
* [ ] ペット情報の管理機能
* [ ] AIによる薬情報の提供

---
