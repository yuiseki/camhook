# -*- coding: utf-8 -*-
import Image, ImageFilter
import os
from cStringIO import StringIO

from datetime import datetime
from django.db import models
from django.contrib import admin

from django.conf import settings
media = settings.MEDIA_ROOT

from django.core.files.storage import FileSystemStorage

class Thread(models.Model):
    """
    各写真が所属するスレ。
    スレtitleごとにwebhookでPOSTするためのURLが生成される。titleは一意な文字列で、早い者勝ちになる。
    webhook POSTの際には、スレ登録時に決めたphraseが一致していなければならない。
    phraseを忘れると更新できなくなるので、cookieに作ったスレtitleとphraseを保存しておく。
    URLをGETすればそこに投稿されてきた写真の過去ログが得られる。
    GETの際にcookieのtitleに保存されたphraseが一致した場合は、phraseを表示。作った人だけ変更できる。
    URLとphraseを他の人に教えればスレを複数人で更新できる。
    """
    created_at  = models.DateTimeField(u'作成日時', default=datetime.now, editable=False)
    modified_at = models.DateTimeField(u'変更日時', default=datetime.now, editable=False)
    title = models.CharField(u"Title", max_length=128, null=False, unique=True)
    phrase = models.CharField(u"Passphrase", max_length=15, null=False)

class Photo(models.Model):
    """webhookで投稿されてきた写真などを表すモデル"""

    created_at  = models.DateTimeField(u'作成日時', default=datetime.now)
    modified_at = models.DateTimeField(u'変更日時', default=datetime.now)
    shooting_at = models.DateTimeField(u'撮影日',   null=True)
    name = models.CharField(u'ID', max_length=15, null=False)
    # 所属するスレ。POSTがきたURLで決定される
    thread = models.ForeignKey(Thread, null=False)

    image = models.ImageField(u'Image', upload_to='photos')
    thumb = models.ImageField(u'Thumb', upload_to='thumbs')

    def save(self):
        if self.thumb == "":
            self._create_thumb()
        super(Photo, self).save()

    # 横幅300pxのサムネイルを生成
    def _create_thumb(self):
        img = Image.open(self.image)
        zoom = min( float(300) / max(img.size[0],img.size[1]), 1.0 )
        size = int(img.size[0]*zoom), int(img.size[1]*zoom)
        img.thumbnail(size, Image.ANTIALIAS)
        img.filter(ImageFilter.DETAIL)
        img.save('media_root/thumbs/%s.jpg' % self.name)
        self.thumb = 'thumbs/%s.jpg' % self.name
        self.save()

try:
    admin.site.register(Photo)
    admin.site.register(Thread)
except:
    pass
