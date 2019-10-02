import os

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
TFT_IMG_UBUNTU_URL = os.environ.get(
    "TFT_IMG_UBUNTU_URL", 'https://cloud-images.ubuntu.com/bionic/current/'
                          'bionic-server-cloudimg-amd64.img'
)
TFT_CLOUD_INIT = os.environ.get(
    "TFT_CLOUD_INIT", 'data/images/cloud_init'
)
TFT_CLEANUP_SETUP = os.environ.get(
    "TFT_CLEANUP_SETUP", True
)
