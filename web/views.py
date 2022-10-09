from django.shortcuts import render

# Create your views here.
def auth(request):
    return render(request, 'web/auth.html', {})

def dashboard(request):
    return render(request, 'web/dashboard.html', {})

def pointcloud(request):
    return render(request, 'web/pointcloud.html', {})
