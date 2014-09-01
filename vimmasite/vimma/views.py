from django.shortcuts import render
from rest_framework import viewsets, routers, filters, serializers
from rest_framework.permissions import (
    SAFE_METHODS, BasePermission, IsAuthenticated
)

from vimma.models import (
    Schedule, TimeZone, Project, Provider, DummyProvider, AWSProvider,
    VMConfig, DummyVMConfig, AWSVMConfig
)
from vimma.actions import Actions
from vimma.util import can_do, login_required_or_forbidden


class TimeZoneViewSet(viewsets.ReadOnlyModelViewSet):
    model = TimeZone
    filter_backends = (filters.OrderingFilter,)
    ordering = ('name',)


class SchedulePermission(BasePermission):
    """
    Everyone can read Schedules, only users with permissions may write them.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return can_do(request.user, Actions.WRITE_SCHEDULES)

class ScheduleViewSet(viewsets.ModelViewSet):
    model = Schedule
    permission_classes = (IsAuthenticated, SchedulePermission,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('name',)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    model = Project
    filter_backends = (filters.OrderingFilter,)
    ordering = ('name',)

    def get_queryset(self):
        user = self.request.user
        if can_do(user, Actions.READ_ANY_PROJECT):
            return Project.objects.filter()
        return user.profile.projects


class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    model = Provider
    filter_backends = (filters.OrderingFilter,)
    ordering = ('name',)

class DummyProviderViewSet(viewsets.ReadOnlyModelViewSet):
    model = DummyProvider

class AWSProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AWSProvider
        fields = ('id', 'visible_field',)

class AWSProviderViewSet(viewsets.ReadOnlyModelViewSet):
    model = AWSProvider
    serializer_class = AWSProviderSerializer


class VMConfigViewSet(viewsets.ReadOnlyModelViewSet):
    model = VMConfig
    filter_backends = (filters.OrderingFilter,)
    ordering = ('name',)

class DummyVMConfigViewSet(viewsets.ReadOnlyModelViewSet):
    model = DummyVMConfig

class AWSVMConfigViewSet(viewsets.ReadOnlyModelViewSet):
    model = AWSVMConfig


@login_required_or_forbidden
def index(request):
    """
    Homepage.
    """
    return render(request, 'vimma/index.html')


@login_required_or_forbidden
def test(request):
    """
    JavaScript Unit Tests.
    """
    return render(request, 'vimma/test.html')
