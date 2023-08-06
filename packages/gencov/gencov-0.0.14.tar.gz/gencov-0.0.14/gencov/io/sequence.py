from . import config
from .util import LazyImport

pyfaidx = LazyImport("pyfaidx", path=config.PYFAIDX_MOD)


class FastaReader:

    def __init__(self, path):
        self.file = pyfaidx.Fasta(path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def close(self):
        self.file.close()

    def iter_loci_sequence(self):
        for chr_id, start, end in zip(self.chr_ids, self.starts, self.ends):
            yield self.file.get_seq(chr_id, start, end)

    def read_loci_sequence(self):
        return list(self.iter_loci_sequence())


def get_sequence_reader(path=None, type=None):
    return FastaReader
