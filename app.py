from pykubeop import KubernetesOperator, CRDBase
import os

class MyCustomResource(CRDBase):
    GROUP = os.environ["cfg_group"]
    VERSION = os.environ["cfg_version"]
    SINGULAR = os.environ["cfg_singular"]
    PLURAL = os.environ["cfg_plural"]
    KIND = os.environ["cfg_kind"]

    def ensure_created(self):
        print(self.args.my_argument)

    def ensure_modified(self):
        print(self.args.my_argument)

    def ensure_deleted(self):
        print(self.args.my_argument)


class MyOperator(KubernetesOperator):


if __name__ == '__main__':
    MyOperator(MyCustomResource).run()
