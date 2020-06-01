# youtube-downloader2-flask
youtube-downloader2をWeb上で動かすためのFlaskリポジトリ

## Windows環境構築
サブモジュールを含むリポジトリのクローンを行う　　
Pythonのバージョンは3.8
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


## Linux環境構築
サブモジュールを含むリポジトリのクローンを行う(uwsgiの設定内で/usr/localにクローンすることを想定しています)  
Pythonのバージョンは3.6
```
cd /usr/local
git clone --recursive https://github.com/imo-tikuwa/youtube-downloader2-flask.git
cd youtube-downloader2-flask
```

---
venv環境を構築＆起動し、requirements.txtに記載されている必要なライブラリをインストール、別途uwsgiもインストール  
Windows環境と同様にuwsgiを使わずに起動できることを確認
```
python3.6 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/pip install uwsgi

venv/bin/python server.py
curl http://127.0.0.1:5000/
```

---
sockファイルやpidファイルが置かれるディレクトリを作成
```
mkdir -p /var/run/uwsgi
chown root:nginx /var/run/uwsgi
chmod +w /var/run/uwsgi
```

---
uwsgiを--iniオプションを指定して起動
```
uwsgi --ini /usr/local/youtube-downloader2-flask/venv/bin/uwsgi --ini /usr/local/youtube-downloader2-flask/uwsgi.ini
```

起動スクリプトやnginxの設定は各自で。
