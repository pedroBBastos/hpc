from hpccm import Stage
from hpccm.building_blocks import gnu, mlnx_ofed, openmpi
from hpccm.primitives import raw

# Create a stage (Stage0) for the container
Stage0 = Stage()

Stage0 += apt_get(ospackages=['wget', 'build-essential', 'gcc', 'gfortran', 'libpci-dev', 'make'])

# Set the base image as Ubuntu 22.04
Stage0.baseimage('ubuntu:22.04')

# Install Mellanox OFED (MLNX_OFED_LINUX-5.8-3.0.7.0)
Stage0 += mlnx_ofed(version='5.8-3.0.7.0')

# Install GCC 12.2.0
# Stage0 += gnu(version='12.2.0')

# Install additional necessary packages using apt-get
# Stage0 += apt_get(ospackages=['build-essential', 'wget', 'curl', 'libibverbs-dev', 'rdma-core'])

# Install CUDA (adjust version as needed)
# Stage0 += cuda(version='11.7')

# Install OpenMPI 4.1.1
Stage0 += openmpi(version='4.1.1', cuda=False)

# OSU Micro-Benchmarks download and build instructions
osu_version = '5.7'
Stage0 += generic_build(
    url=f'http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-{osu_version}.tar.gz',
    commands=[
        './configure CC=mpicc CXX=mpicxx',
        'make'
    ],
    directory=f'osu-micro-benchmarks-{osu_version}'
)

# Set up environment variables for MPI execution
Stage0 += shell(commands=[
    'echo "export PATH=/usr/local/bin:$PATH" >> /etc/bash.bashrc',
    'echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> /etc/bash.bashrc'
])

# Define runtime environment
Stage0 += shell(commands=[
    'export PATH=/usr/local/bin:$PATH',
    'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH'
])


# Write the container specification to stdout (Dockerfile or Singularity)
print(Stage0)
