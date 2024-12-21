from django.urls import path
from .views import *
from .subplantations_crud import *

urlpatterns = [
    # USER, AUTH
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),  # Use custom refresh view
    path('user_info/', UserInfoAPIView.as_view(), name='user-info'),  # Новый путь для получения информации о пользователе
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'), 
    path('users/create/', create_user, name='create-user'),

    # PLANTATION
    path('plantations/', PlantationListAPIView.as_view(), name='plantation-list'),
    path('plantations/full/', PlantationFullListAPIView.as_view(), name='plantation-fulllist-create'),
    path('plantations/map/', MapPlantationListAPIView.as_view(), name='plantation-map-list'),
    path('plantations/create/', PlantationCreateAPIView.as_view(), name='plantation-create'),
    path('plantations/<int:pk>/', PlantationRetrieveUpdateDestroyAPIView.as_view(), name='plantation-retrieve-update-destroy'),
        # subplantations 
    path('subsidies/', SubsidyListCreateAPIView.as_view(), name='subsidy-list-create'),
    path('subsidies/<int:pk>/', SubsidyRetrieveUpdateDestroyAPIView.as_view(), name='subsidy-detail'),
    path('trellises/', TrellisListCreateAPIView.as_view(), name='trellis-list-create'),
    path('trellises/<int:pk>/', TrellisRetrieveUpdateDestroyAPIView.as_view(), name='trellis-detail'),
    path('reservoirs/', ReservoirListCreateAPIView.as_view(), name='reservoir-list-create'),
    path('reservoirs/<int:pk>/', ReservoirRetrieveUpdateDestroyAPIView.as_view(), name='reservoir-detail'),
    path('investments/', InvestmentListCreateAPIView.as_view(), name='investment-list-create'),
    path('investments/<int:pk>/', InvestmentRetrieveUpdateDestroyAPIView.as_view(), name='investment-detail'),
    path('rootstocks/', RootstockListCreateAPIView.as_view(), name='rootstock-list-create'),
    path('rootstocks/<int:pk>/', RootstockRetrieveUpdateDestroyAPIView.as_view(), name='rootstock-detail'),
    path('farmers/', FarmerListCreateAPIView.as_view(), name='farmer-list-create'),
    path('farmers/<int:pk>/', FarmerRetrieveUpdateDestroyAPIView.as_view(), name='farmer-detail'),
    path('fruits/', get_fruits, name='get-fruits'),  

    # REGIONS
    path('districts/create/', create_district, name='create-district'),  # Путь для создания округа
    path('districts/', get_districts, name='get-districts'),  
    path('regions/', get_regions, name='get-regions'),  
    # OTHER
    path('statistics/', StatisticsAPIView.as_view(), name='statistics-for-admin'),
]

