from hpccm import Stage
from hpccm.building_blocks import gnu, mlnx_ofed, openmpi
from hpccm.primitives import raw

# Create a stage (Stage0) for the container
Stage0 = Stage()

# Set the base image as Ubuntu 22.04
Stage0.baseimage('ubuntu:22.04')

# Install Mellanox OFED (MLNX_OFED_LINUX-5.8-3.0.7.0)
Stage0 += mlnx_ofed(version='5.8-3.0.7.0')

# Install GCC 12.3
Stage0 += gnu(version='12.3')

# Install additional necessary packages using apt-get
# Stage0 += apt_get(ospackages=['build-essential', 'wget', 'curl', 'libibverbs-dev', 'rdma-core'])

# Install OpenMPI 4.1.1
Stage0 += openmpi(version='4.1.1')

# Write the container specification to stdout (Dockerfile or Singularity)
print(Stage0)
