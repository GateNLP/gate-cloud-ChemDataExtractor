# This was the latest version on 20210929
FROM condaforge/mambaforge:4.10.3-6 as conda

# use the lock file to install the none python dependencies
COPY conda-linux-64.lock .
RUN --mount=type=cache,target=/opt/conda/pkgs mamba create --copy -p /env --file conda-linux-64.lock

# now we install the python packages we need --no-deps
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache conda run -p /env python -m pip install  -r requirements.txt

# pull in the data needed by the chemdataextractor package
RUN conda run -p /env cde data download

# copy in the server code (done last so changes to this don't cause
# us to touch any of the previous layers so a nice quick build)
COPY serve.py .

# Default to a single worker thread (which we can then override in
# docker-compose.yml or elsewhere
ENV WORKERS=1

ENV ROOT_PATH=/

# make sure we use the --no-capture-output flag otherwise we get
# zero console output, which makes debugging a nightmare
CMD [ "conda", "run", "-p", "/env", "--no-capture-output", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers","$WORKERS","--timeout", "120", "serve:app" ]

