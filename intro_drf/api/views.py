from django.views.decorators.cache import cache_page
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        institution_name = request.query_params.get('name', None)
        symbol = request.query_params.get('symbol', None)
        date = request.query_params.get('date', None)
        transaction_type = request.query_params.get('transaction_type', None)
        cache_key = f'institution-trade:{institution_name}:{symbol}:{date}:{transaction_type}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(institution_name, symbol, date, transaction_type)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
    
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self, institution_name=None, symbol=None, date=None, transaction_type=None):
        queryset = super().get_queryset()

        if institution_name:
            queryset = queryset.filter(
                Q(top_sellers__contains=[{'name': institution_name}]) |
                Q(top_buyers__contains=[{'name': institution_name}])
            )
    
        if symbol:
            queryset = queryset.filter(symbol__icontains=symbol)
    
        if date:
            queryset = queryset.filter(date=date)

        if transaction_type == 'positive':
            queryset = queryset.filter(net_transaction__gt=0)

        elif transaction_type == 'negative':
            queryset = queryset.filter(net_transaction__lt=0)

        return queryset

class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        sector_name = request.query_params.get('sector', None)
        cache_key = f'metadata:{sector_name}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(sector_name)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self, sector_name=None):
        queryset = super().get_queryset()
        if sector_name:
            queryset = queryset.filter(sector__icontains=sector_name)
        return queryset

    
class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        subsector_name = request.query_params.get('sub_sector', None)
        cache_key = f'reports:{subsector_name}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(subsector_name)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self, subsector_name=None):
        queryset = super().get_queryset()
        if subsector_name:
            queryset = queryset.filter(sub_sector__icontains=subsector_name)
        return queryset