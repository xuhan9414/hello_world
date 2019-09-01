from django.shortcuts import render , redirect
import ldap3

user_list = [
    {"user":"xuhan","pwd":"123"},
    {"user":"meifangqian","pwd":"123"},
]

def log_page(request):
    return render(request, "login.html")

def index(request):
    # if request.session.has_key('user_id'):
        return render(request,'index.html')
    # else:
    #     return redirect('/login/')

def login_hw(request):
    s3 = ldap3.Server('china.huawei.com',port=389,use_ssl = False , get_info = ldap3.SCHEMA)
    user = request.POST.get("user_id")
    pwd = request.POST.get("pass_word")
    try:
        conn = ldap3.Connection([s3],auto_bind = True,client_strategy = ldap3.SYNC,user = 'china\%s'%user,password = pwd,authentication = ldap3.SIMPLE)
        if conn.bind():
            request.session['user_id'] = user
            return redirect('/index/')
        else:
            return render(request, 'login_hw.html', {'error': '密码错误'})
    except:
        return render(request, 'login_hw.html', {'error': '密码错误'})

def login(request):
    user = request.POST.get("user_id")
    pwd = request.POST.get("pass_word")
    user_list = [
        {'xh':'123456'},
        {'mfq':'123456'},
                 ]
    temp = {user:pwd}
    try:
        if temp in user_list:
            request.session['user_id'] = user
            return redirect('/index/')
        else:
            return render(request, 'login.html', {'error': '密码错误'})
    except:
        return render(request, 'login_hw.html', {'error': '密码错误'})