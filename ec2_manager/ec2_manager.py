import os
from dataclasses import dataclass

import boto3


@dataclass
class EC2Manager:
    KEY_PAIR_NAME: str = 'ec2_keypair'
    resource = boto3.resource('ec2')
    client = boto3.client('ec2')

    def create_key_pair_for_instance(self):
        try:
            with open(f'{self.KEY_PAIR_NAME}.pem', 'w') as outfile:
                key_pair = self.resource.create_key_pair(KeyName=self.KEY_PAIR_NAME)
                key_pair_out = str(key_pair.key_material)
                print('---------key-pair created successfully!---------')
                outfile.write(key_pair_out)
                print('---------pem file created successfully!---------')
                self._set_read_perm()
        except Exception as e:
            raise SystemError(f'failed to create ec2 keypair, got \n: {e}')

    def delete_key_pair(self):
        print('----------removing key-pair----------')
        r = self.client.delete_key_pair(KeyName=self.KEY_PAIR_NAME)
        print('----------response:----------')
        print(r)
        print('----------removing pem file----------')
        os.remove(f'{self.KEY_PAIR_NAME}.pem')

    def create_ec2_instance(self):
        instances = self.resource.create_instances(
            ImageId='ami-0de5311b2a443fb89',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=self.KEY_PAIR_NAME
        )
        print(instances)

    @staticmethod
    def _set_read_perm():
        print('-----------setting read params for user script--------------')
        os.system('read_perm.cmd')
        print(f'-----------script executed successfully!--------------')


if __name__ == '__main__':
    ec2 = EC2Manager()
