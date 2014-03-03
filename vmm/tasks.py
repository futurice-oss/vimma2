from __future__ import absolute_import

import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

#from celery import shared_task
from django.conf import settings

from vmm.models import VirtualMachine

import aws.AWS_conn

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vimma2.settings')

app = Celery('tasks')
app.config_from_object('django.conf:settings')
logger = get_task_logger(__name__)

def create_cname(vm_name, public_dns_name):
    route53_conn = aws.AWS_conn.Route53Conn()
    route53_conn.connect()
    logger.warning
    route53_conn.create_cname(vm_name + ".dev.futurice.com", public_dns_name)

@app.task
def create_vm(vm_name):
    logger.warning('Starting to create instance.')
    aws_conn = aws.AWS_conn.EC2Conn()
    aws_conn.connect()

    #vm_name = "demovm" + str(int(time.time()))
    logger.warning('Creating instance with name: %r' % vm_name)

    # moved to view
    #vm_obj = VirtualMachine(primary_name = vm_name, schedule_id = 1)
    #setattr(vm_obj, 'status', 'creating')
    #vm_obj.save()

    try:
        vm_dict = aws_conn.create_instance(instance_name=vm_name).__dict__
    except:
        logger.warning('Instance creation failed for instance name: %r' % vm_name)
        VirtualMachine.objects.filter(primary_name=vm_name).delete()
        return dict()
    else:
        vm_obj = VirtualMachine.objects.get(primary_name=vm_name)
        setattr(vm_obj, 'instance_id', vm_dict['id'])
        setattr(vm_obj, 'status', 'created')
        vm_obj.save()

        # Create CNAME to Route53
        # WARNING: NOTICE: Perhaps move to own task?
        create_cname(vm_name, vm_dict['dns_name'])
        logger.warning("VM creation result dict: %r" % vm_dict)
        return vm_dict

@app.task
def terminate_vm(instance_id):
    logger.warning('Terminating instance id: %r' % instance_id)
    aws_conn = aws.AWS_conn.EC2Conn()
    aws_conn.connect()

    try:
        aws_conn.terminate_instance(instance_id=instance_id)
    except:
        logger.warning('Instance termination failed for instance id: %r' % instance_id)
        return False
    else:
        VirtualMachine.objects.filter(instance_id=instance_id).delete()
        return True
