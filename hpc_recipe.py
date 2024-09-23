from hpccm import Stage
from hpccm.building_blocks import gnu, mlnx_ofed, openmpi, ucx
from hpccm.primitives import raw, environment

Stage0 = Stage()

Stage0 += apt_get(ospackages=['wget', 'build-essential', 'gcc', 'gfortran', 'libpci-dev', 'make'])

Stage0.baseimage('ubuntu:22.04')

# Install Mellanox OFED (MLNX_OFED_LINUX-5.8-3.0.7.0) - "ofed_info -s"
Stage0 += mlnx_ofed(version='5.8-3.0.7.0')

# GCC já instalado pelo 'apt_get' acima
# Stage0 += gnu(version='12.2.0')

Stage0 += ucx(version='1.14.1', cuda=False)

# Install OpenMPI 4.1.1
Stage0 += openmpi(version='4.1.1', cuda=False)

# Set up environment variables
Stage0 += shell(commands=[
    'echo "export PATH=/usr/local/bin:$PATH" >> /etc/bash.bashrc',
    'echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> /etc/bash.bashrc'
])

# Define runtime environment
Stage0 += shell(commands=[
    'export PATH=/usr/local/bin:$PATH',
    'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH'
])

# OSU Micro-Benchmarks download and build instructions
osu_version = '5.7'
Stage0 += shell(commands=[
    f'mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-{osu_version}.tar.gz',
    f'tar -x -f /var/tmp/osu-micro-benchmarks-{osu_version}.tar.gz -C /var/tmp -z',
    f'cd /var/tmp/osu-micro-benchmarks-{osu_version}',
    './configure CC=mpicc CXX=mpicxx',
    'make',
    'make install',
    f'rm -rf /var/tmp/osu-micro-benchmarks-{osu_version} /var/tmp/osu-micro-benchmarks-{osu_version}.tar.gz'
])

# Para poder rodar o 'osu_bw' de qualquer lugar
Stage0 += environment(variables={
    'PATH': '/usr/local/libexec/osu-micro-benchmarks/mpi/pt2pt:$PATH'
})

print(Stage0)
