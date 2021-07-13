FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# ARG github_private_key

WORKDIR /app/

# Copy in Github SSH Key to access private repositories with pip
# RUN mkdir -p ~/.ssh && \
#     chmod 0700 ~/.ssh && \
#     ssh-keyscan github.com > ~/.ssh/known_hosts

# # Do some linux magic to format the key properly.
# RUN echo $github_private_key > ~/.ssh/original
# RUN sed -i 's/ /\n/g' ~/.ssh/original
# RUN sed -i '1,4d' ~/.ssh/original
# RUN tac ~/.ssh/original | sed '1,4d' | tac > ~/.ssh/temp
# RUN echo "-----BEGIN RSA PRIVATE KEY-----" > ~/.ssh/id_rsa
# RUN cat ~/.ssh/temp >> ~/.ssh/id_rsa
# RUN echo "-----END RSA PRIVATE KEY-----" >> ~/.ssh/id_rsa
# RUN chmod 600 ~/.ssh/id_rsa

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/
# RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN pip install git+ssh://git@gitlab.com/codolytics/git-data-science.git@main

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

# RUN rm ~/.ssh/id_rsa

COPY ./app /app
ENV PYTHONPATH=/app
