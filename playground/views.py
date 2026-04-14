from django.shortcuts import render

# Create your views here.
def say_hello(request):
    # 用 render 工具，直接把刚才写好的 hello.html 渲染并发送给用户
    return render(request, 'hello.html', {'name': 'Zheng Yang'})