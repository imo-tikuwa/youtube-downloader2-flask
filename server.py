# -*- coding: utf-8 -*-
import sys
import os
# ロギング
import logging
import logzero
from logzero import logger
# FlaskForm
from flask import Flask, render_template, send_file
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, IntegerField, ValidationError
from wtforms.validators import Required
# 動画URLのパース
import urllib.parse
# 正規表現チェック
import re
# ハイフン付きのソースをインポートするには以下のようにする必要がある？
import importlib
downloader = importlib.import_module("youtube-downloader2.app")


# ffmpegチェック
check_result = downloader.check_ffmpeg()
if not check_result:
    logger.error('ffmpegの解決に失敗しました。')
    sys.exit(1)


# 定数
LOG_DIR = 'log' + os.sep
LOG_FILE = LOG_DIR + 'application.log'
DOWNLOADED_DIR = 'youtube-downloader2' + os.sep + 'downloaded' + os.sep


# ログファイル
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logzero.logfile(LOG_FILE, encoding = "utf-8")
logzero.loglevel(logging.INFO)


# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PsqgOAa1b2bC9Ygt8Vszb6z2n2Kq5R8O'
bootstrap = Bootstrap(app)


# FlaskForm
class YoutubeDownloadForm(FlaskForm):
    youtube_id = StringField('動画ID or 動画URL', validators=[Required()])
    dlfmt = RadioField('ダウンロードフォーマット', validators=[Required()], choices = [('mp4', 'MP4'), ('mp3', 'MP3')], default='mp4')
    thumb_second = IntegerField('MP3にアルバムアートとして埋め込むサムネイル画像を動画から取得する際の秒数', default='1')
    submit = SubmitField('ダウンロード')

    def validate_youtube_id(self, youtube_id):
        """
        動画ID or 動画URL
        入力値チェック
        """
        if youtube_id.data.startswith('https://www.youtube.com/'):
            return

        if re.fullmatch(r'[a-zA-Z0-9_-]+', youtube_id.data):
            return

        raise ValidationError("不正な値が入力されています")


@app.route('/', methods=['GET', 'POST'])
def index():
    youtube_id = None
    dlfmt = None
    thumb_second = None
    form = YoutubeDownloadForm()
    if form.validate_on_submit():

        # リクエストパラメータ取得
        youtube_id = form.youtube_id.data
        dlfmt = form.dlfmt.data
        thumb_second = form.thumb_second.data
        logger.info("動画ID or 動画URL：{0}".format(youtube_id))
        logger.info("ダウンロードフォーマット：{0}".format(dlfmt))
        logger.info("MP3にアルバムアートとして埋め込むサムネイル画像を動画から取得する際の秒数：{0}".format(thumb_second))
        if youtube_id.startswith('https://'):
            qs = urllib.parse.urlparse(youtube_id).query
            qs_d = urllib.parse.parse_qs(qs)
            youtube_id = qs_d['v'][0]
            logger.info("動画URLから抽出した動画ID：{0}".format(youtube_id))

        # 動画ダウンロード or ダウンロード済みの動画からタイトル取得
        if not downloader.is_exist_movie(youtube_id):
            download_result, stream_title = downloader.download_youtube_movie(youtube_id)
            if not download_result:
                logger.error('動画のダウンロードに失敗しました。')
                return render_template('index.html', form=form, youtube_id=youtube_id, dlfmt=dlfmt, thumb_second=thumb_second)
        else:
            stream_title = downloader.get_stream_title_by_download_history(youtube_id)

        # 動画タイトルが稀に「YouTube」となってしまうことがある模様
        # 動画の取得に失敗したとみなす
        if stream_title == 'YouTube':
            logger.error('動画タイトルの取得に失敗しました。')
            return render_template('index.html', form=form, youtube_id=youtube_id, dlfmt=dlfmt, thumb_second=thumb_second)

        # ダウンロード済みの動画情報をyoutube-downloader2/downloaded/.jsonに記録
        downloader.add_download_history(youtube_id, stream_title)

        # ダウンロードフォーマットで処理を切り分け
        if dlfmt == 'mp3':
            convert_result = downloader.convert_mp4_to_mp3(stream_title, thumb_second)
            if not convert_result:
                logger.error('動画のMP3変換に失敗しました。')
                return render_template('index.html', form=form, youtube_id=youtube_id, dlfmt=dlfmt, thumb_second=thumb_second)

        # ダウンロードレスポンス
        return send_file(DOWNLOADED_DIR + stream_title + '.' + dlfmt, as_attachment=True, attachment_filename = stream_title + '.' + dlfmt)

    return render_template('index.html', form=form, youtube_id=youtube_id, dlfmt=dlfmt, thumb_second=thumb_second)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()