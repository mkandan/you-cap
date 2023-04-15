FROM amazonlinux:2023
RUN ulimit -n 1024 && yum -y update && yum -y install \
    python39 \
    python38-pip \
    python38-devel \
    zip \
    && yum clean all

RUN python3 -m pip install pip==23.0.1
RUN pip install virtualenv==20.21.0