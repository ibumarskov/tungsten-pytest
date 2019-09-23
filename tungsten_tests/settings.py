import os

# TungstenFabric Tests (TFT)
TFT_CONF = os.environ.get(
    "TFT_CONF", '/home/ibumarskov/repositories/review.gerrithub.io/'
                'ibumarskov/tungsten-pytest/.venv/tungsten-pytest.cfg'
)
TFT_UBUNTU_IMG_URL = os.environ.get(
    "TFT_UBUNTU_IMG_URL", 'https://cloud-images.ubuntu.com/bionic/current/'
                          'bionic-server-cloudimg-amd64.img'
)
TFT_CLOUD_INIT = os.environ.get(
    "TFT_CLOUD_INIT", '/home/ibumarskov/repositories/review.gerrithub.io/'
                      'ibumarskov/tungsten-pytest/cloud_init'
)
TFT_IMAGE_PATH = os.environ.get(
    "TFT_IMAGE_PATH", os.getcwd()+'/.venv/images'
)
TFT_IMG_FORCE_UPLOAD = os.environ.get(
    "TFT_IMG_FORCE_UPLOAD", False
)
TFT_INSTANCE_KEYS_PATH = os.environ.get(
    "TFT_INSTANCE_KEYS_PATH", os.getcwd()+'/.venv/keys'
)
TFT_CLEANUP_SETUP = os.environ.get(
    "TFT_CLEANUP_SETUP", False
)
