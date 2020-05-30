# youtube-downloader2-flask
youtube-downloader2をWeb上で動かすためのFlaskリポジトリ

## 環境構築
サブモジュールを含むリポジトリのクローンを行う
```
git clone --recursive https://github.com/imo-tikuwa/youtube-downloader2-flask.git
cd youtube-downloader2-flask
```

---
venv環境を構築＆起動し、requirements.txtに記載されている必要なライブラリをインストール、Flaskのサーバーを起動する
```
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
server.py
```
