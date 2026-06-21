from django.contrib.auth.models import User
from rest_framework import generics


from .serializers import SensorReadingSerializer,PhotoSerializer,UserSerializer, NoteSerializer,UploadedImageSerializer
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
from .models import  StockMarketReading

class ChartDataView2(APIView):
    def get(self,request):
        readings=StockMarketReading.objects.all().order_by('timestamp')
        x = [r.timestamp.strftime('%Y-%m-%d %H:%M:%S') for r in readings]
        y = [r.value for r in readings]
        chart_data = {
            "data": [
                {
                    "x": x,
                    "y": y,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Sensor",                }
            ],
            "layout": {
                "title": "Sensor Data",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Value"},
            }
        }
        return Response(chart_data)
    
    
        

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
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)   # required for file uploads
    # If you want public access (remove auth 401):
    permission_classes = [AllowAny]




from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Public search endpoint

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')
        
        # Extract the search term from URL query parameters (?q=iphone)
        query = self.request.query_params.get('q', None)
        
        if query:
            # icontains handles case-insensitive substring matching
            queryset = queryset.filter(title__icontains=query) | queryset.filter(description__icontains=query)
            
        return queryset
