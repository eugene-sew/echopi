from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Device, Deployment, Alert
from .serializers import DeviceSerializer, DeploymentSerializer, AlertSerializer



from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import DeviceSerializer
from .models import Device

@swagger_auto_schema(
    methods=['get'],
    responses={200: DeviceSerializer(many=True)},
    operation_description="List all devices"
)
@swagger_auto_schema(
    methods=['post'],
    request_body=DeviceSerializer,
    responses={201: DeviceSerializer},
    operation_description="Create a new device (no authentication required)"
)
@api_view(['GET', 'POST'])
def device_list(request):
    if request.method == 'GET':
        # Require authentication for GET requests
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['get'],
    responses={200: DeviceSerializer},
    operation_description="Retrieve a device"
)
@swagger_auto_schema(
    methods=['put'],
    request_body=DeviceSerializer,
    responses={200: DeviceSerializer},
    operation_description="Update a device"
)
@swagger_auto_schema(
    methods=['delete'],
    responses={204: "No content"},
    operation_description="Delete a device"
)
@api_view(['GET', 'PUT', 'DELETE'])
def device_detail(request, pk):
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={200: openapi.Response('Token', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))},
        operation_description="Obtain an authentication token"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

# Deployment views
@swagger_auto_schema(
    methods=['get'],
    responses={200: DeploymentSerializer(many=True)},
    operation_description="List all deployments"
)
@swagger_auto_schema(
    methods=['post'],
    request_body=DeploymentSerializer,
    responses={201: DeploymentSerializer},
    operation_description="Create a new deployment"
)
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deployment_list(request):
    if request.method == 'GET':
        deployments = Deployment.objects.all()
        serializer = DeploymentSerializer(deployments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DeploymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['get'],
    responses={200: DeploymentSerializer},
    operation_description="Retrieve a deployment"
)
@swagger_auto_schema(
    methods=['put'],
    request_body=DeploymentSerializer,
    responses={200: DeploymentSerializer},
    operation_description="Update a deployment"
)
@swagger_auto_schema(
    methods=['delete'],
    responses={204: "No content"},
    operation_description="Delete a deployment"
)
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deployment_detail(request, pk):
    try:
        deployment = Deployment.objects.get(pk=pk)
    except Deployment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeploymentSerializer(deployment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DeploymentSerializer(deployment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        deployment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Alert views
@swagger_auto_schema(
    methods=['get'],
    responses={200: AlertSerializer(many=True)},
    operation_description="List all alerts"
)
@swagger_auto_schema(
    methods=['post'],
    request_body=AlertSerializer,
    responses={201: AlertSerializer},
    operation_description="Create a new alert"
)
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def alert_list(request):
    if request.method == 'GET':
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['get'],
    responses={200: AlertSerializer},
    operation_description="Retrieve an alert"
)
@swagger_auto_schema(
    methods=['put'],
    request_body=AlertSerializer,
    responses={200: AlertSerializer},
    operation_description="Update an alert"
)
@swagger_auto_schema(
    methods=['delete'],
    responses={204: "No content"},
    operation_description="Delete an alert"
)
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def alert_detail(request, pk):
    try:
        alert = Alert.objects.get(pk=pk)
    except Alert.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlertSerializer(alert)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AlertSerializer(alert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        alert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
