FROM continuumio/anaconda3:latest

WORKDIR /Django_C4F

# ADD requirements.txt /tmp/requirements.txt
RUN conda update -n base -c defaults conda

RUN conda create -n pyDjango python=3.10.14

RUN conda init bash

COPY . .

RUN chmod +x /Django_C4F/entrypoint.sh
SHELL ["/bin/bash", "--login", "-c"]

RUN conda activate pyDjango && \
    pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

RUN echo "conda activate pyDjango" >> ~/.bashrc

ENTRYPOINT ["/Django_C4F/entrypoint.sh"]

CMD ["bash"]