import math

from .config import CACHE, BIN_SIZE, DEFAULT_VALUE
from .sequence import get_sequence_reader
from .signal import get_signal_reader
from .util import DiskCache


class LociDataReader:

    def __init__(self, chr_ids, starts, ends, strands=None, cache=CACHE):
        self.chr_ids = list(chr_ids)
        self.starts = list(starts)
        self.ends = list(ends)
        self.strands = None if strands is None else list(strands)
        self.cache = cache
        self.sorting_indices = None
        if self.cache is not None:
            locations = [
                [str(chr_id), int(start), int(end), index]
                for index, (chr_id, start, end) in
                enumerate(zip(self.chr_ids, self.starts, self.ends))]
            for index in range(2, -1, -1):
                locations.sort(key=lambda location: location[index])
            self.chr_ids, self.starts, self.ends, self.sorting_indices = zip(*locations)
            cache_data = [self.chr_ids, self.starts, self.ends]
            self.cache = DiskCache(self.cache, "loci_data", cache_data)

    @classmethod
    def from_starts(cls, chr_ids, starts, span, cache=CACHE):
        starts = list(starts)
        ends = (start + span for start in starts)
        return cls(chr_ids, starts, ends, cache)

    @classmethod
    def from_centers(cls, chr_ids, centers, span, cache=CACHE):
        centers = list(centers)
        left_span = math.floor(span / 2)
        right_span = math.ceil(span / 2)
        starts = (center - left_span for center in centers)
        ends = (center + right_span for center in centers)
        return cls(chr_ids, starts, ends, cache)

    def read_signal(self, path, bin_size=BIN_SIZE, default_value=DEFAULT_VALUE):
        if self.cache:
            cache_path = self.cache.get_path([path, bin_size, default_value])
            if self.cache.exists(cache_path):
                return self.cache.read(cache_path)
        type, Reader = get_signal_reader(path, return_type=True)
        arguments = [path, bin_size, default_value] if type == "bigwig" else [path, bin_size]
        with Reader(*arguments) as reader:
            data = reader.read_loci_values(self.chr_ids, self.starts, self.ends)
        if self.cache is not None:
            self.cache.write(cache_path, data)
        if self.sorting_indices is not None:
            data = [data[index] for index in self.sorting_indices]
        if self.strands is not None:
            data = list(strand_loci_values(data, self.strands))
        return data

    def read_sequence(self, path):
        if self.cache:
            cache_path = self.cache.get_path([path])
            if self.cache.exists(cache_path):
                return self.cache.read(cache_path)
        Reader = get_sequence_reader(path)
        with Reader(path) as reader:
            data = reader.read_loci_sequence(self.chr_ids, self.starts, self.ends)
        if self.cache is not None:
            self.cache.write(cache_path, data)
        if self.sorting_indices is not None:
            data = [data[index] for index in self.sorting_indices]
        if self.strands is not None:
            data = list(strand_loci_values(data, self.strands))
        return data


def read_loci_coverage(path, chr_ids, starts, ends, strands=None, bin_size=BIN_SIZE, default_value=DEFAULT_VALUE, cache=CACHE):
    reader = LociDataReader(chr_ids, starts, ends, strands=strands, cache=cache)
    return reader.read_coverage(path, bin_size=bin_size, default_value=default_value)


def read_loci_sequence(path, chr_ids, starts, ends, strands=None, cache=CACHE):
    reader = LociDataReader(chr_ids, starts, ends, strands=strands, cache=cache)
    return reader.read_sequence(path)


def strand_loci_values(loci_values, strands):
    for values, strand in zip(loci_values, strands):
        if strand == "-":
            values.reverse()
        elif strand != "+":
            raise ValueError(f"invalid strand: {strand} (+ or -)")
        yield values
