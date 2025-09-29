
from rest_framework import viewsets
from .models import Hoarding
from .serializers import HoardingSerializer

class HoardingViewSet(viewsets.ModelViewSet):
    queryset = Hoarding.objects.all()
    serializer_class = HoardingSerializer