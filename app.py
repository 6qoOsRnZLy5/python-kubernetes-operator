from pykubeop import KubernetesOperator, CRDBase
import os

class MyCustomResource(CRDBase):
    GROUP = os.environ["cfg_group"]
    VERSION = os.environ["cfg_version"]
    SINGULAR = os.environ["cfg_singular"]
    PLURAL = os.environ["cfg_plural"]
    KIND = os.environ["cfg_kind"]
    //GROUP = 'example.clearscore.io'
    //VERSION = 'v1alpha1'
    //SINGULAR = `testobject`
    //PLURAL = `testobjects`
    //KIND = `TestObject`

    def ensure_created(self):
        // Do some custom logic for ADDED events here
        print(self.args.my_argument)

    def ensure_modified(self):
        // Do some custom logic for MODIFIED events here

    def ensure_deleted(self):
        // Do some custom logic for DELETE events here


class MyOperator(KubernetesOperator):
    def add_arguments(self, parser):
        parser.add_argument(
            '--my-argument',
            type='str',
            help='My useful arg'
        )


if __name__ == '__main__':
    MyOperator(MyCustomResource).run()
