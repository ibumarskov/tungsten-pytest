import os

# TungstenFabric Tests (TFT)
TFT_CONF = os.environ.get(
    "TFT_CONF", '/home/ibumarskov/repositories/review.gerrithub.io/'
                'ibumarskov/tungsten-pytest/.venv/tungsten-pytest.cfg'
)
TFT_UBUNTU_IMG_URL = os.environ.get(
    "TFT_UBUNTU_IMG_URL", 'http://download.cirros-cloud.net/0.4.0/'
                          'cirros-0.4.0-x86_64-disk.img'
)
TFT_IMAGE_PATH = os.environ.get(
    "TFT_IMAGE_PATH", os.getcwd()
)
TFT_IMG_FORCE_UPLOAD = os.environ.get(
    "TFT_IMG_FORCE_UPLOAD", False
)
