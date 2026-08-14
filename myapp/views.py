# Open your local project ──> myapp/views.py
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import generics, viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Unified local model and serializer imports
from .models import Note, SensorReading, Photo, StockMarketReading, Product, PaymentTransaction
from .serializers import (
    SensorReadingSerializer, 
    UserSerializer, 
    NoteSerializer, 
    PhotoSerializer,
    ProductSerializer,
    PaymentTransactionSerializer
)

# =====================================================================
# 🌟 1. CORE MARKETPLACE API VIEWSETS (MODERN ROUTERS)
# =====================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    Handles listing, creating, retrieving, updating, and deleting products.
    Prioritises paid promotional listings at the top and limits the feed to 200 items.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        # 🧠 THE LOGIC: Paid listings (-is_featured) first, newest (-created_at) second, capped at 200 items.
        return Product.objects.all().order_by('-is_featured', '-created_at')[:200]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class PhotoViewSet(viewsets.ModelViewSet):
    """
    Handles uploading images via React binaries and linking them cleanly to specific products.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                serializer.save(product=product)
            except Product.DoesNotExist:
                serializer.save()
        else:
            serializer.save()


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    """
    Handles initiating mobile money tracking requests and checks transaction statuses.
    """
    queryset = PaymentTransaction.objects.all().order_by('-created_at')
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        payload = request.data
        product_id = payload.get('product')
        phone = payload.get('phone_number') # Expected format: 256770000000
        fixed_promo_fee = 20000.00          # 20,000 UGX fixed fee
        
        try:
            # Enforce safety check: Vendor can only promote items they actually own
            product = Product.objects.get(id=product_id, seller=request.user)
            unique_ref = f"GULU-B2B-PROMO-{uuid.uuid4().hex[:8].upper()}"
            
            transaction = PaymentTransaction.objects.create(
                product=product,
                amount=fixed_promo_fee,
                phone_number=phone,
                tx_ref=unique_ref,
                status='PENDING'
            )
            
            serializer = self.get_serializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            return Response({"error": "Product not found or unauthorized access."}, status=404)

    @action(detail=False, methods=['get'], url_path='check-status/(?P<tx_ref>[^/.]+)')
    def check_status(self, request, tx_ref=None):
        """
        React calls this route recursively to verify when a payment prompt changes status.
        URL pattern: GET /api/payments/check-status/GULU-B2B-PROMO-XXXXX/
        """
        try:
            transaction = PaymentTransaction.objects.get(tx_ref=tx_ref, product__seller=request.user)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        except PaymentTransaction.DoesNotExist:
            return Response({"error": "Transaction trace reference not found."}, status=404)


# =====================================================================
# 📝 2. LEGACY GENERICS & AUTHENTICATION ENDPOINTS
# =====================================================================

class CreateUserView(generics.CreateAPIView):
    """Handles frontend public user account registration."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDelete(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


# =====================================================================
# 📊 3. ANALYTICS & SENSOR GRAPH DATA ENDPOINTS
# =====================================================================

class ChartDataView2(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        readings = StockMarketReading.objects.all().order_by('timestamp')
        x = [r.timestamp.strftime('%Y-%m-%d %H:%M:%S') for r in readings]
        y1 = [r.value1 for r in readings]
        y2 = [r.value2 for r in readings]
        chart_data = {
            "data": [
                {"x": x, "y": y1, "type": "scatter", "mode": "lines+markers", "name": "Stock Value 1"},
                {"x": x, "y": y2, "type": "scatter", "mode": "lines+markers", "name": "Stock Value 2"}
            ],
            "layout": {"title": "Stock Market Reading", "xaxis": {"title": "Time"}, "yaxis": {"title": "Value"}}
        }
        return Response(chart_data)


class ChartDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        readings = SensorReading.objects.all().order_by('timestamp')
        x = [r.timestamp.strftime('%Y-%m-%d %H:%M:%S') for r in readings]
        y = [r.value for r in readings]
        chart_data = {
            "data": [{"x": x, "y": y, "type": "scatter", "mode": "lines+markers", "name": "Sensor"}],
            "layout": {"title": "Sensor Data", "xaxis": {"title": "Time"}, "yaxis": {"title": "Value"}}
        }
        return Response(chart_data)
