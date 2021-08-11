from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request,'home.html')

def instructions(request):
    return render(request,'result.html')

def Eval(request):
    q = request.GET['query']
    try:

        ans = eval(q)
        mydictionary = {
            'q' : q,
            "ans" : ans,
            "error" : False
        }
        return render(request,'home.html',context=mydictionary)
    except Exception as e :
        mydictionary = {
            "error": True
        }
        return render(request, 'home.html', context=mydictionary)
