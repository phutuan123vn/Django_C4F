FROM continuumio/miniconda3:latest

# ADD requirements.txt /tmp/requirements.txt

WORKDIR /Django_C4F

RUN conda update -n base -c defaults conda

RUN conda create -n pyDjango python=3.10.14


RUN conda init bash

SHELL ["/bin/bash", "--login", "-c"]
RUN conda init bash
# RUN bin/bash -c "conda activate pyDjango && pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir"

RUN conda activate pyDjango && \
    pip install --upgrade pip && \
    pip install django djangorestframework django-cors-headers

COPY . .

EXPOSE 8000
# RUN echo "conda activate pyDjango" >> $HOME/.bashrc
# CMD ["python", "manage.py", "factory", "runserver", ]
# CMD ["python", "manage.py", "runserver"]

# ENTRYPOINT [ "conda activate pyDjango" ]