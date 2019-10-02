FROM python:2

COPY tungsten_tests /tungsten-pytest/tungsten_tests
COPY data /tungsten-pytest/data
COPY etc /tungsten-pytest/etc
COPY requirements.txt /tungsten-pytest/
COPY tox.ini /tungsten-pytest/
COPY entrypoint.sh /tungsten-pytest/

WORKDIR /tungsten-pytest

RUN pip install -r requirements.txt

ENV TFT_CONF="etc/tungsten-pytest.cfg"
ENV TFT_KUBECONFIG="etc/kubeconfig"

ENTRYPOINT ["/tungsten-pytest/entrypoint.sh"]
