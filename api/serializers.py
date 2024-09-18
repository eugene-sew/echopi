from rest_framework import serializers
from .models import Device, Deployment, Alert
from django.utils.duration import duration_string
from datetime import timedelta
import re

from django.db import IntegrityError

class DeviceSerializer(serializers.ModelSerializer):
    power_level = serializers.FloatField(min_value=0, max_value=100, default=0, allow_null=True)
    uptime = serializers.DurationField(required=False)

    class Meta:
        model = Device
        fields = '__all__'

    def to_internal_value(self, data):
        # Handle 'N/A' for power_level
        if 'power_level' in data and data['power_level'] == 'N/A':
            data['power_level'] = None

        # Convert uptime to a duration
        if 'uptime' in data:
            uptime = data['uptime']
            if isinstance(uptime, (int, float)):
                # Convert seconds to timedelta
                data['uptime'] = timedelta(seconds=uptime)
            elif isinstance(uptime, str):
                if re.match(r'^\d{2}:\d{2}:\d{2}$', uptime):
                    # Convert HH:MM:SS to timedelta
                    hours, minutes, seconds = map(int, uptime.split(':'))
                    data['uptime'] = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                elif uptime.startswith('P'):
                    # Already in ISO 8601 format, let Django handle it
                    pass
                else:
                    try:
                        # Try to convert string to float and then to timedelta
                        data['uptime'] = timedelta(seconds=float(uptime))
                    except ValueError:
                        raise serializers.ValidationError({'uptime': 'Invalid format. Use HH:MM:SS, ISO 8601 duration, or number of seconds.'})
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance.uptime, timedelta):
            representation['uptime'] = duration_string(instance.uptime)
        if instance.power_level is None:
            representation['power_level'] = 'N/A'
        return representation

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"mac_address": "A device with this MAC address already exists."})

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
