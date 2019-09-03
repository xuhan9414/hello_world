from django.shortcuts import render , redirect
import ldap3
from django.shortcuts import HttpResponse

user_list = [
    {'xh': '123456'},
    {'mfq': '123456'},
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
    if len(user) == 0:
        return render(request, 'login.html', {'error1': '请输入账号'})
    if len(pwd) == 0:
        return render(request, 'login.html', {'error2': '请输入密码'})

    temp = {user:pwd}
    try:
        if temp in user_list:
            request.session['user_id'] = user
            return redirect('/index/')
        else:
            return render(request, 'login.html', {'error2': '密码错误'})
    except:
        return render(request, 'login_hw.html', {'error2': '密码错误'})

def registered_page(request):
    return render(request, "registered.html")

def registered(request):
    user1 = request.POST.get("new_user_id")
    pwd1 = request.POST.get("pass_word1")
    pwd2 = request.POST.get("pass_word2")
    icode = request.POST.get("Invite_code")
    if type(user1) == 'NoneType':
        return render(request, 'registered.html')
    elif len(user1) == 0:
        return render(request, 'registered.html', {'error': '请输入账号'})
    elif len(pwd1) == 0:
        return render(request, 'registered.html', {'error': '请输入密码'})
    elif pwd1 != pwd2:
        return render(request, 'registered.html', {'error': '两次输入的密码不一致'})
    elif len(icode) == 0:
        return render(request, 'registered.html', {'error': '请输入邀请码'})