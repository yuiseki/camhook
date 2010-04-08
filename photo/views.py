# -*- coding: utf-8 -*-
from datetime import datetime
import urllib

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.views.generic.simple import direct_to_template

from photo.models import Photo, Thread
from photo.forms import ThreadForm

def top(request):
    # 過去につくったスレはcookieに保存されている
    y_threads = []
    cookie_threads = simplejson.loads(request.COOKIES.get('threads', '{}'))
    threads = Thread.objects.filter(title__in=cookie_threads.keys()).order_by('-modified_at').all()
    for thread in threads:
        if thread.phrase == cookie_threads[thread.title]:
            photos = thread.photo_set.order_by('-created_at')[:6]
            thread.photos = []
            for photo in photos:
                thread.photos.append(photo.thumb)
            y_threads.append(thread)
    # 最近更新されたスレ
    r_threads = []
    recent_threads = Thread.objects.order_by('-modified_at').all()
    for thread in recent_threads:
        # 自分がつくったスレは除外
        if not thread.title in cookie_threads.keys():
            photos = thread.photo_set.order_by('-created_at')[:6]
            thread.photos = []
            for photo in photos:
                thread.photos.append(photo.thumb)
            r_threads.append(thread)
    form = ThreadForm()
    ec = {
        'form'    : form,
        'recent_threads' : r_threads,
        'your_threads' : y_threads,
    }
    return direct_to_template(request, 'photo/top.html', extra_context=ec)


def create(request):
    # titleのスレがないか確認
    title = request.POST['title']
    phrase = request.POST['phrase']
    try:
        thread = Thread.objects.filter(title=title).get()
        return HttpResponseRedirect(title)
    except:
        # なかったら作る
        thread = Thread()
        form = ThreadForm(request.POST, instance=thread)
        new_thread = form.save()
        response = HttpResponseRedirect(title)
        # cookieに情報を保存
        threads = simplejson.loads(request.COOKIES.get('threads', '{}'))
        threads.update({title:phrase})
        response.set_cookie('threads', simplejson.dumps(threads))
        return response


def thread(request, title):
    if request.method == 'POST':
        # webhook POST receive action
        params = request.POST
        try:
            # titleなスレがなかったらエラーがおきるはず
            thread = Thread.objects.filter(title=title).get()
            try:
                # shooting_atがなかったら現在時刻
                shooting_at = datetime.strptime(params['shooting_at'], '%Y/%m/%d %H:%M:%S')
            except:
                shooting_at = datetime.now()
            # passphrase確認
            if thread.phrase == params['pass']:
                photo = Photo(name=params['photo_id'], shooting_at=shooting_at, thread=thread)
                photo.image.save('%s.jpg' % params['photo_id'], request.FILES['imagedata'])
                photo.save()
                thread.modified_at = datetime.now()
                thread.save()
        except:
            pass
        finally:
            # エラーや結果に関係なくレスポンスは返す
            return HttpResponse('hi')

    if request.method == 'GET':
        try:
            # titleスレがすでにある場合は写真一覧
            thread = Thread.objects.filter(title=title).get()
            photos = thread.photo_set.order_by('-created_at')[:40]
            thread.photos = []
            for photo in photos:
                thread.photos.append(photo)
            ec = {
                'thread' : thread
            }
            return direct_to_template(request, 'photo/thread.html', extra_context=ec)
        except:
            thread = Thread(title=title, phrase="")
            ec = {
                'thread' : thread
            }
            # スレがない場合はパスフレーズ入力フォーム
            return direct_to_template(request, 'photo/thread.html', extra_context=ec)


def update(request, title):
    # setinterval API
    params = request.GET['last_access']
    if not params == 'NaN':
        # unixtimeミリ秒（小数点無し表現）なので切り捨てる
        last_access = int(params)*1/1000
        before = datetime.fromtimestamp(last_access+1)
    else:
        now = datetime.now()
        if not now.second == 0:
            before = now.replace(second=now.second - 1)
        else:
            before = now

    thread = Thread.objects.filter(title=title).get()
    photos = thread.photo_set.order_by('-created_at').filter(created_at__gt=before)[:26]
    body_dic = {}
    for photo in photos:
        body_dic[photo.name] = {
            u'thumb':str(photo.thumb),
            u'timestamp': photo.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        }
    body = simplejson.dumps(body_dic)
    return HttpResponse(body)



