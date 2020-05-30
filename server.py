# -*- coding: utf-8 -*-
import sys
import os
import logging
import logzero
from logzero import logger
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, IntegerField
from wtforms.validators import Required

LOG_DIR = 'log' + os.sep
LOG_FILE = LOG_DIR + 'application.log'

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
    dlfmt = RadioField('ダウンロードフォーマット', validators=[Required()], choices = [('1', 'MP4'), ('0', 'MP3')], default='1')
    thumb_second = IntegerField('MP3にアルバムアートとして埋め込むサムネイル画像を動画から取得する際の秒数', default='1')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    youtube_id = None
    dlfmt = None
    thumb_second = None
    form = YoutubeDownloadForm()
    if form.validate_on_submit():
        youtube_id = form.youtube_id.data
        dlfmt = form.dlfmt.data
        thumb_second = form.thumb_second.data

        logger.info("""
動画ID or 動画URL：{0}
ダウンロードフォーマット：{1}
MP3にアルバムアートとして埋め込むサムネイル画像を動画から取得する際の秒数：{2}
--------------------------------------------------
""".format(youtube_id, dlfmt, thumb_second))

        # form.youtube_id.data = ''
        # form.dlfmt.data = ''
    return render_template('index.html', form=form, youtube_id=youtube_id, dlfmt=dlfmt, thumb_second=thumb_second)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()