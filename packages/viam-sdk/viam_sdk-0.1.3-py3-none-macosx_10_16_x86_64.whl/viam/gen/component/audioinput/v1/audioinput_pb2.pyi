"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing
if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _SampleFormat:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _SampleFormatEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_SampleFormat.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    SAMPLE_FORMAT_UNSPECIFIED: _SampleFormat.ValueType
    SAMPLE_FORMAT_INT16_INTERLEAVED: _SampleFormat.ValueType
    SAMPLE_FORMAT_FLOAT32_INTERLEAVED: _SampleFormat.ValueType

class SampleFormat(_SampleFormat, metaclass=_SampleFormatEnumTypeWrapper):
    ...
SAMPLE_FORMAT_UNSPECIFIED: SampleFormat.ValueType
SAMPLE_FORMAT_INT16_INTERLEAVED: SampleFormat.ValueType
SAMPLE_FORMAT_FLOAT32_INTERLEAVED: SampleFormat.ValueType
global___SampleFormat = SampleFormat

class RecordRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    DURATION_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Name of an audio input'

    @property
    def duration(self) -> google.protobuf.duration_pb2.Duration:
        ...

    def __init__(self, *, name: builtins.str=..., duration: google.protobuf.duration_pb2.Duration | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['duration', b'duration']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['duration', b'duration', 'name', b'name']) -> None:
        ...
global___RecordRequest = RecordRequest

class AudioChunkInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SAMPLE_FORMAT_FIELD_NUMBER: builtins.int
    CHANNELS_FIELD_NUMBER: builtins.int
    SAMPLING_RATE_FIELD_NUMBER: builtins.int
    sample_format: global___SampleFormat.ValueType
    'Actual sample encoding format of the response'
    channels: builtins.int
    sampling_rate: builtins.int

    def __init__(self, *, sample_format: global___SampleFormat.ValueType=..., channels: builtins.int=..., sampling_rate: builtins.int=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['channels', b'channels', 'sample_format', b'sample_format', 'sampling_rate', b'sampling_rate']) -> None:
        ...
global___AudioChunkInfo = AudioChunkInfo

class AudioChunk(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATA_FIELD_NUMBER: builtins.int
    LENGTH_FIELD_NUMBER: builtins.int
    data: builtins.bytes
    'Data is PCM data that is organized according to the sample format\n    along with its possible interleaving. Data in each format is\n    Little Endian.\n    '
    length: builtins.int
    'Length is the number of samples'

    def __init__(self, *, data: builtins.bytes=..., length: builtins.int=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['data', b'data', 'length', b'length']) -> None:
        ...
global___AudioChunk = AudioChunk

class ChunksRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    SAMPLE_FORMAT_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Name of an audio input'
    sample_format: global___SampleFormat.ValueType
    'Requested sample encoding format of the response'

    def __init__(self, *, name: builtins.str=..., sample_format: global___SampleFormat.ValueType=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name', 'sample_format', b'sample_format']) -> None:
        ...
global___ChunksRequest = ChunksRequest

class ChunksResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    INFO_FIELD_NUMBER: builtins.int
    CHUNK_FIELD_NUMBER: builtins.int

    @property
    def info(self) -> global___AudioChunkInfo:
        ...

    @property
    def chunk(self) -> global___AudioChunk:
        ...

    def __init__(self, *, info: global___AudioChunkInfo | None=..., chunk: global___AudioChunk | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['chunk', b'chunk', 'info', b'info', 'type', b'type']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['chunk', b'chunk', 'info', b'info', 'type', b'type']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing_extensions.Literal['type', b'type']) -> typing_extensions.Literal['info', 'chunk'] | None:
        ...
global___ChunksResponse = ChunksResponse

class PropertiesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Name of an audio input'

    def __init__(self, *, name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___PropertiesRequest = PropertiesRequest

class PropertiesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CHANNEL_COUNT_FIELD_NUMBER: builtins.int
    LATENCY_FIELD_NUMBER: builtins.int
    SAMPLE_RATE_FIELD_NUMBER: builtins.int
    SAMPLE_SIZE_FIELD_NUMBER: builtins.int
    IS_BIG_ENDIAN_FIELD_NUMBER: builtins.int
    IS_FLOAT_FIELD_NUMBER: builtins.int
    IS_INTERLEAVED_FIELD_NUMBER: builtins.int
    channel_count: builtins.int

    @property
    def latency(self) -> google.protobuf.duration_pb2.Duration:
        ...
    sample_rate: builtins.int
    sample_size: builtins.int
    is_big_endian: builtins.bool
    is_float: builtins.bool
    is_interleaved: builtins.bool

    def __init__(self, *, channel_count: builtins.int=..., latency: google.protobuf.duration_pb2.Duration | None=..., sample_rate: builtins.int=..., sample_size: builtins.int=..., is_big_endian: builtins.bool=..., is_float: builtins.bool=..., is_interleaved: builtins.bool=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['latency', b'latency']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['channel_count', b'channel_count', 'is_big_endian', b'is_big_endian', 'is_float', b'is_float', 'is_interleaved', b'is_interleaved', 'latency', b'latency', 'sample_rate', b'sample_rate', 'sample_size', b'sample_size']) -> None:
        ...
global___PropertiesResponse = PropertiesResponse