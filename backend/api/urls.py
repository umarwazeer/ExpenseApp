from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('expenses', views.ExpenseViewSet, basename='expense')
router.register('groups', views.ExpenseGroupViewSet, basename='group')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('budgets', views.BudgetViewSet, basename='budget')

router.register('settings', views.UserSettingsViewSet, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    # path("chat/", AiChatAPIView.as_view(), name="ai-chat"),

]
