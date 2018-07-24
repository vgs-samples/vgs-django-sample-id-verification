from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from .models import PiiData


def index(request):
    pii_data_list = PiiData.objects.order_by('-pub_date')[:5]
    host = getattr(settings, "VGS_REVERSE_PROXY", "")
    context = {
        'pii_data_list': pii_data_list,
        'server_uri': host + "/app/add"
    }
    return render(request, 'app/index.html', context)


def detail(request, data_id):
    pii_data = get_object_or_404(PiiData, pk=data_id)
    return render(request, 'app/detail.html', {'pii_data': pii_data})


@csrf_exempt
def add(request):
    snn = request.POST['SNN']
    national_id = request.POST['national_id']
    pii_data = PiiData(social_security_number=snn, national_id=national_id, pub_date=datetime.now())
    pii_data.save()
    return HttpResponse(str(pii_data.id))

