from django.shortcuts import render
from django.http import Http404,StreamingHttpResponse
import os
from utility.FileOperating import FileOperating

input_dir = r"D:\emf_testing_data\input_data"
output_dir = r"D:\emf_testing_data\output_data"

def date_searching(request):
    user_id = request.session.get('user_id')
    f = FileOperating(output_dir + '\\' +user_id,user_id)
    result = f.file_searching()
    return render(request,'subject/emf_searching_reslut.html',{'result':result})

def emf_time_searching(request):
    date = request.GET.get('date')
    user_id = request.session.get('user_id')
    f = FileOperating(output_dir + '\\' +user_id + '\\' + date,user_id)
    result = f.file_searching()
    return render(request,'subject/emf_searching_reslut1.html',{'result':result,'date':date})

def emf_result_searching(request):
    user_id = request.session.get('user_id')
    date = request.GET.get('date')
    time = request.GET.get('time')
    names = os.listdir(output_dir + '\\' + user_id + '\\' + date + '\\' +time)
    for i in names:
        if '.xlsx' in i:
            name = i
    results = {"rank_mcs":"result.png","date":date,'time':time,'user':user_id,
               'name':name}
    return render(request,'subject/emf_searching_reslut2.html',{'results':results})

def emf_download(request):
    user = request.session.get('user_id')
    date = request.GET.get('date')
    time = request.GET.get('time')
    pictures = request.GET.get('pictures')
    path = output_dir + '\\' + user + '\\' +date +'\\' + time + '\\' + pictures
    try:
        response = StreamingHttpResponse(open(path,'rb'))
        response['content_type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
        return response
    except Exception:
        raise Http404