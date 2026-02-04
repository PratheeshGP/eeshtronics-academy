from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Module, ModuleUnlock
from .serializers import ModuleSerializer, ModuleUnlockSerializer


class ModuleListView(generics.ListAPIView):
    """List all modules, optionally filtered by path."""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Module.objects.all()
        path_id = self.request.query_params.get('path', None)
        if path_id:
            queryset = queryset.filter(path_id=path_id)
        return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}


class ModuleDetailView(generics.RetrieveAPIView):
    """Get detailed module information."""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['POST'])
def unlock_module(request, module_id):
    """
    Unlock a module by spending Ether.
    POST /api/modules/<id>/unlock
    """
    try:
        module = Module.objects.get(id=module_id)
    except Module.DoesNotExist:
        return Response({'error': 'Module not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already unlocked
    if ModuleUnlock.objects.filter(user=request.user, module=module).exists():
        return Response({'error': 'Module already unlocked'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Spend Ether
    if request.user.spend_ether(module.ether_cost, f"Unlocked module: {module.title}"):
        unlock = ModuleUnlock.objects.create(
            user=request.user,
            module=module
        )
        serializer = ModuleUnlockSerializer(unlock)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {'error': 'Insufficient Ether balance'},
            status=status.HTTP_402_PAYMENT_REQUIRED
        )
