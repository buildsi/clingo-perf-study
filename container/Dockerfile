FROM python:3.7

WORKDIR /opt/sc22

ENV PATH=/opt/sc22/spack/bin:${PATH}

# Update python dependencies
RUN pip install -U pip && pip install pandas numpy matplotlib

# Checkout the correct version of Spack
RUN git clone -b v0.17.2 --single-branch https://github.com/spack/spack.git && \
    spack compiler find && \
    spack --version && \
    spack python --version && \
    spack debug report 

# Patch Spack to return inner timings
COPY ./modified_spack/asp.py /opt/sc22/spack/lib/spack/spack/solver/asp.py
COPY ./modified_spack/spec.py /opt/sc22/spack/lib/spack/spack/spec.py

# Bootstrap clingo
RUN spack solve hdf5

# Copy scripts to reproduce smaller scale experiments
COPY ./asp_solve.py /opt/sc22/experiments/
COPY ./analyze*.py /opt/sc22/experiments/
COPY ./*.list /opt/sc22/experiments/

WORKDIR /opt/sc22/experiments

ENTRYPOINT ["/bin/bash"]
