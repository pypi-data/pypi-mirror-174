import importlib
import zlib

from . import config
from . import signal_c
from . import signal_mod
from . import signal_std

from .config import BIN_SIZE, DEFAULT_VALUE, FILL_ENTRIES


class SignalReader:

    def __init__(self, reader):
        self.reader = reader
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def close(self):
        self.reader.close()

    @property
    def chr_sizes(self):
        return self.reader.chr_sizes

    def iter_loci_values(self, chr_ids, starts, ends):
        return self.reader.iter_loci_values(chr_ids, starts, ends)
    
    def read_loci_values(self, chr_ids, starts, ends):
        return list(self.iter_loci_values(chr_ids, starts, ends))

    def iter_loci_entries(self, chr_ids, starts, ends):
        return self.reader.iter_loci_entries(chr_ids, starts, ends)

    def read_loci_entries(self, chr_ids, starts, ends):
        return list(self.iter_loci_entries(chr_ids, starts, ends))

    def iter_chr_entries(self, chr_id):
        return self.reader.iter_chr_entries(chr_id)

    def read_chr_entries(self, chr_id):
        return list(self.iter_chr_entries(chr_id))

    def iter_entries(self, chr_id):
        for chr_id in self.chr_sizes:
            yield from self.reader.iter_chr_entries(chr_id)

    def read_entries(self):
        return list(self.read_entries())


class BigwigReader(SignalReader):

    def __init__(self, path, bin_size=BIN_SIZE, default_value=DEFAULT_VALUE, fill_entries=FILL_ENTRIES):
        self.path = path
        self.bin_size = bin_size
        self.default_value = default_value
        self.fill_entries = fill_entries
        super().__init__(get_signal_subreader("bigwig")(path, bin_size, default_value))

    def iter_loci_entries(self, chr_ids, starts, ends):
        loci_entries = self.reader.iter_loci_entries(chr_ids, starts, ends)
        if self.fill_entries:
            for entries, chr_id, start, end in zip(loci_entries, chr_ids, starts, ends):
                entries = fill_locus_entries(entries, chr_id, self.default_value, start, end)
                entries = merge_locus_entries(entries)
                yield list(entries)
        else:
            yield from loci_entries

    def iter_chr_entries(self, chr_id):
        entries = self.reader.iter_chr_entries(chr_id)
        if self.fill_entries:
            end = self.chr_sizes[chr_id]
            entries = fill_locus_entries(entries, chr_id, self.default_value, 0, end)
            entries = merge_locus_entries(entries)
        yield from entries


class BigbedReader(SignalReader):

    def __init__(self, path, bin_size=BIN_SIZE):
        self.path = path
        self.bin_size = bin_size
        super().__init__(get_signal_subreader("bigbed")(path, bin_size))


class BamReader(SignalReader):

    def __init__(self, path, bin_size=BIN_SIZE):
        self.path = path
        self.bin_size = bin_size
        super().__init__(get_signal_subreader("bam")(path, bin_size))


def fill_locus_entries(entries, chr_id, default_value, start=None, end=None):
    last_entry = [None, None, start, None]
    for entry in entries:
        try:
            if entry[1] > last_entry[2]:
                yield [chr_id, last_entry[2], entry[1], default_value]
        except Exception:
            if last_entry[2] is not None:
                raise
        yield entry
        last_entry = entry
    if last_entry[0] is None:
        if start is not None and end is not None and end > start:
            yield [chr_id, start, end, default_value]
    elif end is not None and last_entry[2] < end:
        yield [chr_id, last_entry[2], end, default_value]


def merge_locus_entries(entries):
    last_entry = None
    for entry in entries:
        if last_entry is None:
            last_entry = entry
            continue
        if entry[1] <= last_entry[2] and entry[3] == last_entry[3]:
            last_entry[2] = entry[2]
            continue
        yield entry
    if last_entry is not None:
        yield entry


def get_signal_file_type(path):
    with open(path, "rb") as file:
        chunk = file.read(4)
        if chunk in (b"&\xfc\x8f\x88", b"\x88\x8f\xfc&"):
            return "bigwig"
        if chunk in (b"\xeb\xf2\x89\x87", b"\x87\x89\xf2\xeb"):
            return "bigbed"
        if chunk[:2] == b"\x1f\x8b":
            chunk += file.read(65536 - 4)
            try:
                decompressed_chunk = zlib.decompress(chunk, 31)
                if decompressed_chunk[:4] == b"BAM\x01":
                    return "bam"
            except Exception:
                pass
    raise RuntimeError(f"neither bigwig, bigbed nor bam: {path}")


def get_signal_reader(path=None, type=None, return_type=False):
    if type is None:
        if path is None:
            raise RuntimeError("neither file type nor path specified")
        type = get_signal_file_type(path)
    targets = dict(
        bigwig=BigwigReader,
        bigbed=BigbedReader,
        bam=BamReader)
    reader = targets[type]
    return (type, reader) if return_type else reader


def get_signal_subreader(type):
    targets = dict(
        bigwig=["BigwigReader", "BIGWIG_READER_BIN", "pyBigWig"],
        bigbed=["BigbedReader", "BIGBED_READER_BIN", "pyBigWig"],
        bam=["BamReader", None, "pysam"])
    reader_name, c_lib_bin, py_mod_name = targets[type]
    if config.FORCE_STD_LIB:
        return getattr(signal_std, reader_name)
    if c_lib_bin and getattr(config, c_lib_bin):
        return getattr(signal_c, reader_name)
    try:
        importlib.import_module(py_mod_name)
        return getattr(signal_mod, reader_name)
    except Exception:
        return getattr(signal_std, reader_name)


def get_signal_writer(type):
    targets = dict(
        bigwig=["BigwigWriter", "BEDGRAPH_TO_BIGWIG_BIN", "pyBigWig"])
    writer_name, c_lib_bin, py_mod_name = targets[type]
    if config.FORCE_STD_LIB:
        return getattr(signal_std, writer_name)
    if c_lib_bin and getattr(config, c_lib_bin):
        return getattr(signal_c, writer_name)
    try:
        importlib.import_module(py_mod_name)
        return getattr(signal_mod, writer_name)
    except Exception:
        return getattr(signal_std, writer_name)
