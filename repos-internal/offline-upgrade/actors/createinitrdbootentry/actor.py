from leapp.actors import Actor
from leapp.tags import IPUWorkflowTag, InterimPreparationPhaseTag
from subprocess import check_call

class CreateInitRdBootEntry(Actor):
    name = 'create_init_rd_boot_entry'
    description = 'No description has been provided for the create_init_rd_boot_entry actor.'
    consumes = ()
    produces = ()
    tags = (IPUWorkflowTag, InterimPreparationPhaseTag)

    def process(self):
        check_call([
            '/bin/cp',
            self.get_file_path('vmlinuz-upgrade.x86_64'),
            self.get_file_path('initramfs-upgrade.x86_64.img'),
            '/boot'
        ])
        check_call([
            '/usr/sbin/grubby',
            '--add-kernel=/boot/vmlinuz-upgrade.x86_64',
            '--initrd=/boot/initramfs-upgrade.x86_64.img',
            '--title=RHEL Upgrade RAMDISK',
            '--copy-default',
            '--make-default',
            '--args="debug enforcing=0 rd.plymouth=0 plymouth.enable=0"'
        ])
