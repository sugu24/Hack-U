from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect
from .models import PostDataModel, ThreadModel
from django.http import JsonResponse
import subprocess

# Create your views here.
def SelectThreadView(request):
    if request.method == 'POST':
        if 'create_thread_btn' in request.POST:
            group_name = request.POST.get('thread_name')
            thread_object = ThreadModel.objects.create(
                name = group_name
            )
            thread_object.save()
            return redirect('bulletinBoard', thread_object.pk)
    else:
        thread_all = ThreadModel.objects.all()
        return render(request, 'selectThread.html', {'thread_all': thread_all})


def BulletinBoardView(request, pk):
    post_count = PostDataModel.objects.all().count()
    if request.method == 'POST':
        request_type = request.POST.get('type')
        if request_type == 'getPostsData':
            thread = ThreadModel.objects.get(pk=pk)
            after = int(request.POST.get('after'))
            post_datas = PostDataModel.objects.filter(thread=thread).order_by('post_id')[after: min(after+100,post_count)]
            post_datas = list(post_datas.values())
            d = {"post_datas": post_datas}
            return JsonResponse(d)
        elif request_type == 'setPostData':
            thread_object = ThreadModel.objects.get(pk=pk)
            name = request.POST.get('name')
            time = request.POST.get('time')
            content = request.POST.get('content')
            process = subprocess.Popen(['python3', './/bert/bert.py', '{}'.format(content)], encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result, error = process.communicate()
            if result[:8] == "negative":
                return JsonResponse({"error":"ネガティブな投稿なので投稿文を確認してください"})
            postdata_object = PostDataModel.objects.create(
                thread = thread_object,
                post_id = thread_object.next_id,
                name = name,
                postdate = time,
                content = content
            )
            response = request.POST.get('response')
            if response != "":
                try:
                    response_object = PostDataModel.objects.filter(thread=thread_object).get(post_id=int(response))
                    postdata_object.response = response_object
                    postdata_object.response_post_id = response_object.post_id
                except ObjectDoesNotExist:
                    postdata_object.delete()
                    return JsonResponse({"error":"既に削除されたか、存在しない投稿に返信しています"})
                except ValueError:
                    postdata_object.delete()
                    return JsonResponse({"error": "送信相手を見直してください"})
            thread_object.next_id += 1
            thread_object.save()
            postdata_object.save()
            return JsonResponse({"error":""})
        elif request_type == 'good_action':
            post_id = request.POST.get('post_id')
            thread_object = ThreadModel.objects.get(pk=pk)
            post_object = PostDataModel.objects.filter(thread=thread_object).get(post_id=post_id)
            if request.POST.get('action') == 'plus':
                post_object.good += 1
            elif request.POST.get('action') == 'minus':
                post_object.good -= 1
            post_object.save()

            channel_layer = get_channel_layer()
            channel_name = thread_object.name
            async_to_sync(channel_layer.group_send)(
                channel_name, {
                    'type' : 'send_message',
                    'flag' : 'good_action',
                    'post_id': post_id,
                    'number': post_object.good
                }
            )
            return JsonResponse({"":""})
        elif request_type == 'bad_action':
            post_id = request.POST.get('post_id')
            thread_object = ThreadModel.objects.get(pk=pk)
            try:
                post_object = PostDataModel.objects.filter(thread=thread_object).get(post_id=post_id)
            except ObjectDoesNotExist:
                return JsonResponse({})
            if request.POST.get('action') == 'plus':
                post_object.bad += 1
            elif request.POST.get('action') == 'minus':
                post_object.bad -= 1
            
            post_object.save()

            channel_layer = get_channel_layer()
            channel_name = thread_object.name
            async_to_sync(channel_layer.group_send)(
                channel_name, {
                    'type': 'send_message',
                    'flag': 'bad_action',
                    'post_id': post_id,
                    'number': post_object.bad
                }
            )

            if post_object.bad >= 4:
                from collections import deque
                channel_layer = get_channel_layer()
                channel_name = thread_object.name
                delete_id = deque([post_object.post_id])
                response_id = []
                while len(delete_id) > 0:
                    frm_post_id = delete_id.popleft()
                    to_objects = PostDataModel.objects.filter(thread=thread_object).filter(response_post_id=frm_post_id)
                    for to_object in to_objects:
                        delete_id.append(to_object.post_id)
                    response_id.append(frm_post_id)
                
                async_to_sync(channel_layer.group_send)(
                    channel_name, {
                        'type' : 'delete_message',
                        'flag' : 'delete_action',
                        'delete': response_id
                    }
                )
                post_object.delete()

            return JsonResponse({})
    else:
        thread = ThreadModel.objects.get(pk=pk)
        post_datas = PostDataModel.objects.filter(thread=thread).order_by('post_id')[0:min(100, post_count)]
        return render(request, 'bulletinBoard.html', {'post_datas': post_datas, "thread_name": thread.name})