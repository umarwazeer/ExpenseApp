from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Expense, ExpenseGroup, Category, Budget, UserSettings
from django.contrib.auth.hashers import check_password
from .serializers import (
    ExpenseSerializer, ExpenseGroupSerializer, 
    CategorySerializer, BudgetSerializer, UserSettingsSerializer, UserSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(
            Q(user=self.request.user) |
            Q(group__members=self.request.user)
        ).distinct()

        # Group filter
        group_id = self.request.query_params.get('group')
        if group_id:
            queryset = queryset.filter(group_id=group_id)

        # Date range filter
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        # Type filter (income / expense)
        expense_type = self.request.query_params.get('type')
        if expense_type in ['income', 'expense']:
            queryset = queryset.filter(expense_type=expense_type)

        # Category filter
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name__iexact=category)

        # Search filter
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )

        return queryset


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Get date range from query params
        period = request.query_params.get('period', 'monthly')
        group_id = request.query_params.get('group')
        
        # Calculate date range
        end_date = timezone.now().date()
        if period == 'daily':
            start_date = end_date
        elif period == 'weekly':
            start_date = end_date - timedelta(days=7)
        elif period == 'yearly':
            start_date = end_date - timedelta(days=365)
        else:  # monthly
            start_date = end_date - timedelta(days=30)
        
        # Build query
        query = Q(user=request.user)
        if group_id:
            query = Q(group_id=group_id)
        
        expenses = Expense.objects.filter(
            query,
            date__range=[start_date, end_date]
        )
        
        # Calculate statistics
        total_income = expenses.filter(expense_type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        total_expenses = expenses.filter(expense_type='expense').aggregate(
            total=Sum('amount'))['total'] or 0
        
        # Category breakdown
        category_breakdown = expenses.filter(expense_type='expense').values(
            'category__name').annotate(total=Sum('amount')).order_by('-total')
        
        return Response({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': total_income - total_expenses,
            'category_breakdown': category_breakdown,
            'period': period,
            'start_date': start_date,
            'end_date': end_date
        })

class ExpenseGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseGroup.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)
        group.members.add(self.request.user)

    @action(detail=False, methods=['post'])
    def join(self, request):
        invite_code = request.data.get('invite_code')
        try:
            group = ExpenseGroup.objects.get(invite_code=invite_code)
            group.members.add(request.user)
            serializer = ExpenseGroupSerializer(group)
            return Response(serializer.data)
        except ExpenseGroup.DoesNotExist:
            return Response(
                {'error': 'Invalid invite code'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        group = self.get_object()
        group.members.remove(request.user)
        return Response({'message': 'Left group successfully'})

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(
            Q(user=self.request.user) | Q(is_default=True)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSettingsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Return current user's settings
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings_obj)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        # Accepts partial fields. pk unused (we use current user).
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def upload_avatar(self, request):
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        settings_obj.avatar = avatar_file
        settings_obj.save()
        serializer = UserSettingsSerializer(settings_obj)
        return Response(serializer.data)
