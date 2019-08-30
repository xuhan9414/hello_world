from django.shortcuts import render
from django.shortcuts import HttpResponse
import numpy as np

def emf_ajax(request):
    return render(request, 'subject/emf_analyse.html')

def emf_add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    a = 10**(a/100)
    c = a*b
    d = c/1000
    c = 100*np.log10(c)/10
    c = round(c, 2)
    d = round(d, 2)
    r = HttpResponse(str(c)+'dBm' + ' /'+str(d) + 'W')
    return r