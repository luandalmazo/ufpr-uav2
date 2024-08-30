FROM --platform=linux/amd64 pytorch/pytorch

ENV PYTHONUNBUFFERED 1

RUN groupadd -r user && useradd -m --no-log-init -r -g user user
USER user

WORKDIR /opt/app

COPY --chown=user:user requirements.txt /opt/app/
COPY --chown=user:user resources /opt/app/
COPY --chown=user:user best-901.zip /opt/app/

RUN python -m pip install \
    --user \
    --no-cache-dir \
    --no-color \
    --requirement /opt/app/requirements.txt

COPY --chown=user:user nnUNet /opt/app/nnUNet
RUN python -m pip install --user -e /opt/app/nnUNet
ENV PATH=$PATH:/home/user/.local/bin

ENV nnUNet_raw=/opt/app/
ENV nnUNet_preprocessed=/opt/app/
ENV nnUNet_results=/opt/app/

COPY --chown=user:user inference.py /opt/app/

ENTRYPOINT ["python", "inference.py"]

