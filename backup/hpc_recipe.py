from hpccm import Stage
from hpccm.building_blocks import gnu, mlnx_ofed, apt_get # , openmpi
from hpccm.primitives import raw

# Create a stage (Stage0) for the container
Stage0 = Stage()

# Set the base image as Ubuntu 22.04
Stage0 += comment("Ubuntu 22.04 with Mellanox OFED, Intel MPI, and GCC")
Stage0.baseimage('ubuntu:22.04')

# Install Mellanox OFED (MLNX_OFED_LINUX-5.8-3.0.7.0)
Stage0 += mlnx_ofed(version='5.8-3.0.7.0')

# Install GCC 12.3
Stage0 += gnu(version='12.3')

# Install additional necessary packages using apt-get
Stage0 += apt_get(ospackages=['build-essential', 'wget', 'curl', 'libibverbs-dev', 'rdma-core'])

# Install OpenMPI 4.1.1
# Stage0 += openmpi(version='4.1.1')

# Manually download and install Intel MPI 2019.5.0 using raw shell commands
mpi_installer = '''
wget https://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15547/l_mpi_2019.5.281.tgz
tar -xzf l_mpi_2019.5.281.tgz
cd l_mpi_2019.5.281 && ./install.sh --silent --accept_eula
'''
Stage0 += raw(script=mpi_installer)

# Set environment variables for OpenMPI and Intel MPI (if needed)
Stage0 += raw(script='export PATH=$PATH:/opt/intel/mpi/latest/bin')
Stage0 += raw(script='export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/mpi/latest/lib')

# Write the container specification to stdout (Dockerfile or Singularity)
print(Stage0)
