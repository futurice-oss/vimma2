from django.db import transaction
import logging

from vimma.celery import app
from vimma.models import (
    VM,
    DummyVM,
)
from vimma.util import retry_transaction


log = logging.getLogger(__name__)


def create_vm(vm, data):
    """
    Create a dummy VM, linking to parent ‘vm’, from ‘data’ → (vm, callables)

    data = {
        name: string,
        delay: int, // seconds before powering ON
    }

    This function must be called inside a transaction. The caller must execute
    the returned callables only after committing.
    """
    dummyVM = DummyVM.objects.create(vm=vm, name=data['name'],
            status='creating…')
    dummyVM.full_clean()

    # execute as much code as possible here (inside the transaction) not in the
    # callable (which runs after comitting the transaction).
    countdown = min(max(0, data['delay']), 60)
    callables = [
            lambda: do_power_on_vm.apply_async(args=(dummyVM.id,),
                countdown=countdown),
            ]
    return dummyVM, callables


def power_on_vm(vm_id, data):
    """
    Power on VM.

    ‘data’ is not used.

    This function must not be called inside a transaction.
    """
    with transaction.atomic():
        dummy_vm = VM.objects.get(id=vm_id).dummyvm
        dummy_vm.status = 'powering on…'
        dummy_vm.save()
    do_power_on_vm.delay(dummy_vm.id)


@app.task
def do_power_on_vm(dummy_vm_id):
    with transaction.atomic():
        dvm = DummyVM.objects.get(id=dummy_vm_id)
        # imagine this logic happens remotely, in an API call to the Provider
        if dvm.destroyed or dvm.poweredon:
            log.error(('Can\'t power on DummyVM {0.id} ‘{0.name}’ with ' +
                'poweredon ‘{0.poweredon}’, destroyed ‘{0.destroyed}’').format(
                    dvm))
            return
        dvm.poweredon = True
        dvm.save()


def power_off_vm(vm_id, data):
    """
    Power off VM.

    ‘data’ is not used.

    This function must not be called inside a transaction.
    """
    with transaction.atomic():
        dummy_vm = VM.objects.get(id=vm_id).dummyvm
        dummy_vm.status = 'powering off…'
        dummy_vm.save()
    do_power_off_vm.delay(dummy_vm.id)


@app.task
def do_power_off_vm(dummy_vm_id):
    with transaction.atomic():
        dvm = DummyVM.objects.get(id=dummy_vm_id)
        if dvm.destroyed or not dvm.poweredon:
            log.error(('Can\'t power off DummyVM {0.id} ‘{0.name}’ with ' +
                'poweredon ‘{0.poweredon}’, destroyed ‘{0.destroyed}’').format(
                    dvm))
            return
        dvm.poweredon = False
        dvm.save()


def reboot_vm(vm_id, data):
    """
    Reboot VM.

    ‘data’ is not used.

    This function must not be called inside a transaction.
    """
    with transaction.atomic():
        dummy_vm = VM.objects.get(id=vm_id).dummyvm
        dummy_vm.status = 'rebooting…'
        dummy_vm.save()
    do_reboot_vm.delay(dummy_vm.id)


@app.task
def do_reboot_vm(dummy_vm_id):
    with transaction.atomic():
        dvm = DummyVM.objects.get(id=dummy_vm_id)
        if dvm.destroyed:
            log.error(('Can\'t reboot DummyVM {0.id} ‘{0.name}’ with ' +
                'poweredon ‘{0.poweredon}’, destroyed ‘{0.destroyed}’').format(
                    dvm))
            return
        dvm.poweredon = True
        dvm.save()


def destroy_vm(vm_id, data):
    """
    Destroy VM.

    ‘data’ is not used.

    This function must not be called inside a transaction.
    """
    with transaction.atomic():
        dummy_vm = VM.objects.get(id=vm_id).dummyvm
        dummy_vm.status = 'destroying…'
        dummy_vm.save()
    do_destroy_vm.delay(dummy_vm.id)


@app.task
def do_destroy_vm(dummy_vm_id):
    with transaction.atomic():
        dvm = DummyVM.objects.get(id=dummy_vm_id)
        if dvm.destroyed:
            log.error(('Can\'t destroy DummyVM {0.id} ‘{0.name}’ with ' +
                'poweredon ‘{0.poweredon}’, destroyed ‘{0.destroyed}’').format(
                    dvm))
            return
        dvm.poweredon = False
        dvm.destroyed = True
        dvm.save()


@app.task
def update_vm_status(vm_id):
    def call():
        with transaction.atomic():
            dvm = VM.objects.get(id=vm_id).dummyvm
            if dvm.destroyed:
                dvm.status = 'destroyed'
            else:
                dvm.status = 'powered ' + ('on' if dvm.poweredon else 'off')
            dvm.save()

    retry_transaction(call)
