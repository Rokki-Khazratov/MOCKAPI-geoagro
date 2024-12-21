from api.plantation_models import *
from api.plantations import *
from rest_framework import generics

# Subsidy CRUD
class SubsidyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subsidy.objects.all()
    serializer_class = SubsidySerializer


class SubsidyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subsidy.objects.all()
    serializer_class = SubsidySerializer



# Reservoir CRUD
class ReservoirListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reservoir.objects.all()
    serializer_class = ReservoirSerializer


class ReservoirRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservoir.objects.all()
    serializer_class = ReservoirSerializer


# Trellis CRUD
class TrellisListCreateAPIView(generics.ListCreateAPIView):
    queryset = Trellis.objects.all()
    serializer_class = TrellisSerializer


class TrellisRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trellis.objects.all()
    serializer_class = TrellisSerializer



# Investment CRUD
class InvestmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class InvestmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


# Farmer CRUD
class FarmerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer


class FarmerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
