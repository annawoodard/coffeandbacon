import os

from funcx.config import Config
from funcx.strategies import SimpleStrategy
from parsl.providers import CondorProvider
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname

proxy = '/tmp/x509up_u{}'.format(os.getuid())
if not os.path.isfile(proxy):
    raise RuntimeError('No valid proxy found-- run `voms-proxy-init -voms cms`')

worker_init = '''
source /cvmfs/sft.cern.ch/lcg/views/LCG_95apython3/x86_64-centos7-gcc7-opt/setup.sh

export PATH=~/.local/bin:$PATH
export PYTHONPATH=~/.local/lib/python3.6/site-packages:$PYTHONPATH
export FUNCX_TMPDIR=/tmp/{}

export X509_USER_PROXY=`pwd`/{}

mkdir -p $FUNCX_TMPDIR
'''.format(os.environ['USER'], os.path.basename(proxy))

config = Config(
    scaling_enabled=False,
    worker_debug=True,
    cores_per_worker=1,
    strategy=SimpleStrategy(max_idletime=60000), # TOTAL HACK FIXME
    provider=CondorProvider(
        scheduler_options='stream_error=TRUE\nstream_output=TRUE\nTransferOut=TRUE\nTransferErr=TRUE',
        cores_per_slot=8,
        init_blocks=90,
        max_blocks=90,
        worker_init=worker_init,
        transfer_input_files=[proxy]
    ),
)
