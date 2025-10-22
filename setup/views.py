from rest_framework import generics
from .models import SetupInfo, ProcessWiseControl
from .serializers import SetupInfoSerializer, ProcessWiseControlSerializer


# -------------------------
# SetupInfo Views
# -------------------------
class SetupInfoListCreateView(generics.ListCreateAPIView):
    queryset = SetupInfo.objects.all()
    serializer_class = SetupInfoSerializer


class SetupInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SetupInfo.objects.all()
    serializer_class = SetupInfoSerializer


# -------------------------
# ProcessWiseControl Views
# -------------------------
class ProcessWiseControlListCreateView(generics.ListCreateAPIView):
    queryset = ProcessWiseControl.objects.all()
    serializer_class = ProcessWiseControlSerializer


class ProcessWiseControlDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProcessWiseControl.objects.all()
    serializer_class = ProcessWiseControlSerializer
