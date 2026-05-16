from django.contrib.auth.models import User
from rest_framework import generics


from .serializers import SensorReadingSerializer,UserSerializer, NoteSerializer,UploadedImageSerializer
from .models import Note,UploadedImage,SensorReading
from rest_framework.permissions import IsAuthenticated, AllowAny


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)  # Add this line for debugging


class UploadCreateImage(generics.ListCreateAPIView):
    serializer_class=UploadedImageSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        
        return UploadedImage.objects.all()
    def perform_create(self,serializer):
        if serializer.is_valid():
            serializer.save()
        else: 
            print("errors")




class NoteDelete(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



from rest_framework.views import APIView
from rest_framework.response import Response

class ChartDataView(APIView):
    def get(self, request):
        readings = SensorReading.objects.all().order_by('timestamp')
        x = [r.timestamp.strftime('%Y-%m-%d %H:%M:%S') for r in readings]
        y = [r.value for r in readings]

        chart_data = {
            "data": [
                {
                    "x": x,
                    "y": y,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Sensor",
                }
            ],
            "layout": {
                "title": "Sensor Data",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Value"},
            }
        }
        return Response(chart_data)
    
    
    
    
    

from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedImage
from .serializers import UploadedImageSerializer


class ImageListView(generics.ListAPIView):
    queryset = UploadedImage.objects.all().order_by('-uploaded_at')
    serializer_class = UploadedImageSerializer
    permission_classes = [AllowAny]   #
    
    
    


class ImageUploadView(generics.CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    parser_classes = (MultiPartParser, FormParser)   # required for file uploads
    # If you want public access (remove auth 401):
    permission_classes = [AllowAny]



