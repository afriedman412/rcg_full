from django.shortcuts import render
from .models import Weekly_Count, Gender
import random

def index(request):
	latest_count = Weekly_Count.objects.order_by('-date_created')[0]
	rando = random.randint(1,10)
	context = {'latest_count': latest_count, 'rando':rando}
	return render(request, 'rcg_app/index.html', context)