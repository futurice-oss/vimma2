from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import json


class Permission(models.Model):
    """
    A Permission.

    There is a special omnipotent permission used to grant all permissions.
    """
    name = models.CharField(max_length=100, unique=True)


class Role(models.Model):
    """
    A role represents a set of Permissions.

    A user is assigned a set of Roles and has all permissions in those roles.
    """
    name = models.CharField(max_length=20, unique=True)
    permissions = models.ManyToManyField(Permission)


class Project(models.Model):
    """
    Projects group Users and VMs.
    """
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()


class Profile(models.Model):
    """
    An extension of the User model.
    """
    user = models.OneToOneField(User)
    projects = models.ManyToManyField(Project)
    roles = models.ManyToManyField(Role)


class TimeZone(models.Model):
    name = models.CharField(max_length=100, unique=True)


def schedule_matrix_validator(val):
    try:
        matrix = json.loads(val)
    except ValueError as e:
        raise ValidationError(e.args[0] if e.args else "Invalid JSON")
    if len(matrix) != 7:
        raise ValidationError('Schedule matrix has ' + str(len(matrix)) +
                ' rows instead of 7')
    for row in matrix:
        if len(row) != 48:
            raise ValidationError('Schedule matrix row has ' + str(len(row)) +
                    ' items instead of 48')
        for item in row:
            if type(item) != bool:
                raise ValidationError('Schedule matrix has non-bool element ' +
                        str(type(item)))

class Schedule(models.Model):
    """
    A schedule marks when the VM should be powered on or powered off.

    A 7×48 matrix with boolean values marks ON (true) or OFF (false).
    Each row is a day of the week (first row is Monday, last row is Sunday).
    Each column is a 30-min time interval. First column is [0:00, 0:30),
    second is [0:30, 1:00), last column is [23:30, 24:00).
    """
    name = models.CharField(max_length=50, unique=True)
    timezone = models.ForeignKey(TimeZone, on_delete=models.PROTECT)
    matrix = models.TextField(validators=[schedule_matrix_validator])
    # ‘special’ schedules can't be used by anyone. E.g. 24h turned on.
    # Users need the USE_SPECIAL_SCHEDULE permission to use them.
    is_special = models.BooleanField(default=False)


class Provider(models.Model):
    """
    A provider of virtual machines.

    This model holds fields common across all models. Additional data specific
    to this provider's type (e.g. Amazon Web Services) is held in a linked
    model via a one-to-one field.

    E.g. each account at Amazon Web Services is a different Provider.
    """
    TYPE_DUMMY = 'dummy'
    TYPE_AWS = 'aws'
    TYPE_CHOICES = (
        (TYPE_DUMMY, 'Dummy'),
        (TYPE_AWS, 'Amazon Web Services'),
    )
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)


class DummyProvider(models.Model):
    """
    Type-specific info for a Provider of type Provider.TYPE_DUMMY.
    """
    provider = models.OneToOneField(Provider, on_delete=models.PROTECT)


class AWSProvider(models.Model):
    """
    Type-specific info for a Provider of type Provider.TYPE_AWS.
    """
    provider = models.OneToOneField(Provider, on_delete=models.PROTECT)
    # these will be replaced with AWS-specific fields (credentials, etc.)
    visible_field = models.BooleanField(default=True)
    invisible_field = models.BooleanField(default=True)


class VMConfig(models.Model):
    """
    A VM Configuration for a Provider. A provider may have several of these.

    This model holds fields common across all VM Configs. Additional data
    specific to the provider's type is in a model linked via a one-to-one
    field.
    """
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    # The default schedule for this VM config. Users are allowed to choose this
    # schedule for VMs made from this config, even if the schedule itself
    # requires additional permissions.
    default_schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
    # Users need Perms.VM_CONF_INSTANTIATE to create a VM from this config.
    requires_permission = models.BooleanField(default=False)


class DummyVMConfig(models.Model):
    """
    Type-specific info for a VMConfig of type Provider.TYPE_DUMMY.
    """
    vmconfig = models.OneToOneField(VMConfig, on_delete=models.PROTECT)


class AWSVMConfig(models.Model):
    """
    Type-specific info for a VMConfig of type Provider.TYPE_AWS.
    """
    vmconfig = models.OneToOneField(VMConfig, on_delete=models.PROTECT)
    # These will be replaced with real fields
    img_id = models.CharField(max_length=50, blank=True)
    hardware_id = models.CharField(max_length=50, blank=True)
