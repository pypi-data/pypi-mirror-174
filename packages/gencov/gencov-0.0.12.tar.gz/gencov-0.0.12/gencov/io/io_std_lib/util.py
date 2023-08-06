import struct
import zlib


class BinaryParser:

    struct_objects = dict()
    type_codes = dict(
        int8="b", uint8="B", int16="h", uint16="H",
        int32="i", uint32="I", int64="q", uint64="Q",
        float16="e", float32="f", float64="d",
        pad8="x", pad16="2x", pad32="4x", pad64="8x")

    def __init__(self, data, little_endian=True):
        self.data = data
        self.position = 0
        self.endian_code = "<" if little_endian else ">"

    @property
    def length(self):
        return len(self.data)

    @property
    def remaining_length(self):
        return self.length - self.position

    def get_struct(self, types):
        try:
            struct_object = self.struct_objects[(self.endian_code, types)]
        except KeyError:
            types_code = "".join(self.type_codes[type] for type in types.split("/"))
            struct_object = struct.Struct(self.endian_code + types_code)
            self.struct_objects[(self.endian_code, types)] = struct_object
        return struct_object
    
    def read(self, types):
        struct_object = self.get_struct(types)
        chunk = self.data[self.position:self.position + struct_object.size]
        output = struct_object.unpack(chunk)
        self.position += struct_object.size
        return output

    def read_sequence(self, types):
        return self.read(types)

    def read_number(self, type):
        return self.read(type)[0]

    def read_int8(self):
        return self.read("int8")[0]

    def read_uint8(self):
        return self.read("uint8")[0]

    def read_int16(self):
        return self.read("int16")[0]

    def read_uint16(self):
        return self.read("uint16")[0]

    def read_int32(self):
        return self.read("int32")[0]

    def read_uint32(self):
        return self.read("uint32")[0]

    def read_int64(self):
        return self.read("int64")[0]

    def read_uint64(self):
        return self.read("uint64")[0]

    def read_float16(self):
        return self.read("float16")[0]

    def read_float32(self):
        return self.read("float32")[0]

    def read_float64(self):
        return self.read("float64")[0]

    def read_string(self, length=None, null_terminated=False):
        if length is None:
            if null_terminated:
                null_index = self.data.find(b"\0", self.position)
                if null_index >= 0:
                    chunk = self.data[self.position:null_index]
                    self.position += null_index - self.position + 1
                else:
                    chunk = self.data[self.position:]
                    self.position += self.remaining_length
            else:
                chunk = self.data[self.position:]
                self.position += self.remaining_length
        else:
            length = min(length, self.remaining_length)
            chunk = self.data[self.position:self.position + length]
            self.position += length
            if null_terminated:
                null_index = chunk.find(b"\0")
                if null_index >= 0:
                    chunk = chunk[:null_index]
        return chunk.decode()


def add_in_resize_array(array, index, value, fill=None):
    if index >= len(array):
        array.extend([fill] * (index - len(array) + 1))
    array[index] = value


def decompress_bgzf(data):
    chunks = []
    decompressor = zlib.decompressobj(31)
    chunks.append(decompressor.decompress(data))
    while decompressor.unused_data:
        remaining_bytes = decompressor.unused_data
        decompressor = zlib.decompressobj(31)
        chunks.append(decompressor.decompress(remaining_bytes))
    return b"".join(chunks)
