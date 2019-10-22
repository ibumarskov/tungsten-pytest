import os


def bash_str_to_bool(val):
    if isinstance(val, str):
        if val.lower() == 'false':
            return False
        if val.lower() == 'true':
            return True
    return val


# TungstenFabric Tests (TFT)
TFT_CONF = os.environ.get(
    "TFT_CONF", 'etc/tungsten-pytest.cfg'
)
TFT_KUBECONFIG = os.environ.get(
    "TFT_KUBECONFIG", 'etc/kubeconfig'
)
TFT_INSTANCE_KEYS_PATH = os.environ.get(
    "TFT_INSTANCE_KEYS_PATH", 'data/keys'
)
TFT_IMG_PATH = os.environ.get(
    "TFT_IMG_PATH", 'data/images'
)
TFT_IMG_FORCE_UPLOAD = os.environ.get(
    "TFT_IMG_FORCE_UPLOAD", False
)
TFT_IMG_FORCE_UPLOAD = bash_str_to_bool(TFT_IMG_FORCE_UPLOAD)
TFT_IMG_UBUNTU_URL = os.environ.get(
    "TFT_IMG_UBUNTU_URL", 'https://cloud-images.ubuntu.com/bionic/current/'
                          'bionic-server-cloudimg-amd64.img'
)
TFT_CLOUD_INIT = os.environ.get(
    "TFT_CLOUD_INIT", 'tungsten_tests/data/cloud_init'
)
TFT_CLEANUP_SETUP = os.environ.get(
    "TFT_CLEANUP_SETUP", True
)
TFT_CLEANUP_SETUP = bash_str_to_bool(TFT_CLEANUP_SETUP)
