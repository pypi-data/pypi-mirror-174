"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
from .... import common
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.struct_pb2
import sys
import typing
if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class GetModelParameterSchemaRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    MODEL_TYPE_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    model_type: builtins.str
    'name of the type of vision model'

    def __init__(self, *, name: builtins.str=..., model_type: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['model_type', b'model_type', 'name', b'name']) -> None:
        ...
global___GetModelParameterSchemaRequest = GetModelParameterSchemaRequest

class GetModelParameterSchemaResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MODEL_PARAMETER_SCHEMA_FIELD_NUMBER: builtins.int
    model_parameter_schema: builtins.bytes
    'the parameters as JSON bytes of a jsonschema.Schema'

    def __init__(self, *, model_parameter_schema: builtins.bytes=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['model_parameter_schema', b'model_parameter_schema']) -> None:
        ...
global___GetModelParameterSchemaResponse = GetModelParameterSchemaResponse

class GetDetectorNamesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str

    def __init__(self, *, name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetDetectorNamesRequest = GetDetectorNamesRequest

class GetDetectorNamesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DETECTOR_NAMES_FIELD_NUMBER: builtins.int

    @property
    def detector_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """detectors in the registry"""

    def __init__(self, *, detector_names: collections.abc.Iterable[builtins.str] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['detector_names', b'detector_names']) -> None:
        ...
global___GetDetectorNamesResponse = GetDetectorNamesResponse

class AddDetectorRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    DETECTOR_NAME_FIELD_NUMBER: builtins.int
    DETECTOR_MODEL_TYPE_FIELD_NUMBER: builtins.int
    DETECTOR_PARAMETERS_FIELD_NUMBER: builtins.int
    name: builtins.str
    detector_name: builtins.str
    detector_model_type: builtins.str

    @property
    def detector_parameters(self) -> google.protobuf.struct_pb2.Struct:
        ...

    def __init__(self, *, name: builtins.str=..., detector_name: builtins.str=..., detector_model_type: builtins.str=..., detector_parameters: google.protobuf.struct_pb2.Struct | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['detector_parameters', b'detector_parameters']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['detector_model_type', b'detector_model_type', 'detector_name', b'detector_name', 'detector_parameters', b'detector_parameters', 'name', b'name']) -> None:
        ...
global___AddDetectorRequest = AddDetectorRequest

class AddDetectorResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None:
        ...
global___AddDetectorResponse = AddDetectorResponse

class RemoveDetectorRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    DETECTOR_NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    detector_name: builtins.str
    'name of detector in registry'

    def __init__(self, *, name: builtins.str=..., detector_name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['detector_name', b'detector_name', 'name', b'name']) -> None:
        ...
global___RemoveDetectorRequest = RemoveDetectorRequest

class RemoveDetectorResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None:
        ...
global___RemoveDetectorResponse = RemoveDetectorResponse

class GetDetectionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    IMAGE_FIELD_NUMBER: builtins.int
    WIDTH_FIELD_NUMBER: builtins.int
    HEIGHT_FIELD_NUMBER: builtins.int
    MIME_TYPE_FIELD_NUMBER: builtins.int
    DETECTOR_NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    image: builtins.bytes
    'the image, encoded as bytes'
    width: builtins.int
    'the width of the image'
    height: builtins.int
    'the height of the image'
    mime_type: builtins.str
    'the actual MIME type of image'
    detector_name: builtins.str
    'name of the registered detector to use'

    def __init__(self, *, name: builtins.str=..., image: builtins.bytes=..., width: builtins.int=..., height: builtins.int=..., mime_type: builtins.str=..., detector_name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['detector_name', b'detector_name', 'height', b'height', 'image', b'image', 'mime_type', b'mime_type', 'name', b'name', 'width', b'width']) -> None:
        ...
global___GetDetectionsRequest = GetDetectionsRequest

class GetDetectionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DETECTIONS_FIELD_NUMBER: builtins.int

    @property
    def detections(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Detection]:
        """the bounding boxes and labels"""

    def __init__(self, *, detections: collections.abc.Iterable[global___Detection] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['detections', b'detections']) -> None:
        ...
global___GetDetectionsResponse = GetDetectionsResponse

class GetDetectionsFromCameraRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    CAMERA_NAME_FIELD_NUMBER: builtins.int
    DETECTOR_NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    camera_name: builtins.str
    'name of camera source to use as input'
    detector_name: builtins.str
    'name of the registered detector to use'

    def __init__(self, *, name: builtins.str=..., camera_name: builtins.str=..., detector_name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['camera_name', b'camera_name', 'detector_name', b'detector_name', 'name', b'name']) -> None:
        ...
global___GetDetectionsFromCameraRequest = GetDetectionsFromCameraRequest

class GetDetectionsFromCameraResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DETECTIONS_FIELD_NUMBER: builtins.int

    @property
    def detections(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Detection]:
        """the bounding boxes and labels"""

    def __init__(self, *, detections: collections.abc.Iterable[global___Detection] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['detections', b'detections']) -> None:
        ...
global___GetDetectionsFromCameraResponse = GetDetectionsFromCameraResponse

class Detection(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_MIN_FIELD_NUMBER: builtins.int
    Y_MIN_FIELD_NUMBER: builtins.int
    X_MAX_FIELD_NUMBER: builtins.int
    Y_MAX_FIELD_NUMBER: builtins.int
    CONFIDENCE_FIELD_NUMBER: builtins.int
    CLASS_NAME_FIELD_NUMBER: builtins.int
    x_min: builtins.int
    'the four corners of the box'
    y_min: builtins.int
    x_max: builtins.int
    y_max: builtins.int
    confidence: builtins.float
    'the confidence of the detection'
    class_name: builtins.str
    'label associated with the detected object'

    def __init__(self, *, x_min: builtins.int | None=..., y_min: builtins.int | None=..., x_max: builtins.int | None=..., y_max: builtins.int | None=..., confidence: builtins.float=..., class_name: builtins.str=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['_x_max', b'_x_max', '_x_min', b'_x_min', '_y_max', b'_y_max', '_y_min', b'_y_min', 'x_max', b'x_max', 'x_min', b'x_min', 'y_max', b'y_max', 'y_min', b'y_min']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['_x_max', b'_x_max', '_x_min', b'_x_min', '_y_max', b'_y_max', '_y_min', b'_y_min', 'class_name', b'class_name', 'confidence', b'confidence', 'x_max', b'x_max', 'x_min', b'x_min', 'y_max', b'y_max', 'y_min', b'y_min']) -> None:
        ...

    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal['_x_max', b'_x_max']) -> typing_extensions.Literal['x_max'] | None:
        ...

    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal['_x_min', b'_x_min']) -> typing_extensions.Literal['x_min'] | None:
        ...

    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal['_y_max', b'_y_max']) -> typing_extensions.Literal['y_max'] | None:
        ...

    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal['_y_min', b'_y_min']) -> typing_extensions.Literal['y_min'] | None:
        ...
global___Detection = Detection

class GetClassifierNamesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'

    def __init__(self, *, name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetClassifierNamesRequest = GetClassifierNamesRequest

class GetClassifierNamesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CLASSIFIER_NAMES_FIELD_NUMBER: builtins.int

    @property
    def classifier_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        ...

    def __init__(self, *, classifier_names: collections.abc.Iterable[builtins.str] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['classifier_names', b'classifier_names']) -> None:
        ...
global___GetClassifierNamesResponse = GetClassifierNamesResponse

class AddClassifierRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    CLASSIFIER_NAME_FIELD_NUMBER: builtins.int
    CLASSIFIER_MODEL_TYPE_FIELD_NUMBER: builtins.int
    CLASSIFIER_PARAMETERS_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    classifier_name: builtins.str
    'name of classifier to add to registry'
    classifier_model_type: builtins.str
    'the type of classifier'

    @property
    def classifier_parameters(self) -> google.protobuf.struct_pb2.Struct:
        """additional parameters"""

    def __init__(self, *, name: builtins.str=..., classifier_name: builtins.str=..., classifier_model_type: builtins.str=..., classifier_parameters: google.protobuf.struct_pb2.Struct | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['classifier_parameters', b'classifier_parameters']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['classifier_model_type', b'classifier_model_type', 'classifier_name', b'classifier_name', 'classifier_parameters', b'classifier_parameters', 'name', b'name']) -> None:
        ...
global___AddClassifierRequest = AddClassifierRequest

class AddClassifierResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None:
        ...
global___AddClassifierResponse = AddClassifierResponse

class RemoveClassifierRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    CLASSIFIER_NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    classifier_name: builtins.str
    'name of the classifier in registry'

    def __init__(self, *, name: builtins.str=..., classifier_name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['classifier_name', b'classifier_name', 'name', b'name']) -> None:
        ...
global___RemoveClassifierRequest = RemoveClassifierRequest

class RemoveClassifierResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None:
        ...
global___RemoveClassifierResponse = RemoveClassifierResponse

class GetClassificationsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    IMAGE_FIELD_NUMBER: builtins.int
    WIDTH_FIELD_NUMBER: builtins.int
    HEIGHT_FIELD_NUMBER: builtins.int
    MIME_TYPE_FIELD_NUMBER: builtins.int
    CLASSIFIER_NAME_FIELD_NUMBER: builtins.int
    N_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    image: builtins.bytes
    'the image encoded as bytes'
    width: builtins.int
    'the width of the image'
    height: builtins.int
    'the height of the image'
    mime_type: builtins.str
    'the actual MIME type of image'
    classifier_name: builtins.str
    'the name of the registered classifier'
    n: builtins.int
    'the number of classifications desired'

    def __init__(self, *, name: builtins.str=..., image: builtins.bytes=..., width: builtins.int=..., height: builtins.int=..., mime_type: builtins.str=..., classifier_name: builtins.str=..., n: builtins.int=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['classifier_name', b'classifier_name', 'height', b'height', 'image', b'image', 'mime_type', b'mime_type', 'n', b'n', 'name', b'name', 'width', b'width']) -> None:
        ...
global___GetClassificationsRequest = GetClassificationsRequest

class GetClassificationsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CLASSIFICATIONS_FIELD_NUMBER: builtins.int

    @property
    def classifications(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Classification]:
        ...

    def __init__(self, *, classifications: collections.abc.Iterable[global___Classification] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['classifications', b'classifications']) -> None:
        ...
global___GetClassificationsResponse = GetClassificationsResponse

class GetClassificationsFromCameraRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    CAMERA_NAME_FIELD_NUMBER: builtins.int
    CLASSIFIER_NAME_FIELD_NUMBER: builtins.int
    N_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    camera_name: builtins.str
    'the image encoded as bytes'
    classifier_name: builtins.str
    'the name of the registered classifier'
    n: builtins.int
    'the number of classifications desired'

    def __init__(self, *, name: builtins.str=..., camera_name: builtins.str=..., classifier_name: builtins.str=..., n: builtins.int=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['camera_name', b'camera_name', 'classifier_name', b'classifier_name', 'n', b'n', 'name', b'name']) -> None:
        ...
global___GetClassificationsFromCameraRequest = GetClassificationsFromCameraRequest

class GetClassificationsFromCameraResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CLASSIFICATIONS_FIELD_NUMBER: builtins.int

    @property
    def classifications(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Classification]:
        ...

    def __init__(self, *, classifications: collections.abc.Iterable[global___Classification] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['classifications', b'classifications']) -> None:
        ...
global___GetClassificationsFromCameraResponse = GetClassificationsFromCameraResponse

class Classification(google.protobuf.message.Message):
    """the general form of the output from a classifier"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CLASS_NAME_FIELD_NUMBER: builtins.int
    CONFIDENCE_FIELD_NUMBER: builtins.int
    class_name: builtins.str
    'the class name'
    confidence: builtins.float
    'the confidence score of the classification'

    def __init__(self, *, class_name: builtins.str=..., confidence: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['class_name', b'class_name', 'confidence', b'confidence']) -> None:
        ...
global___Classification = Classification

class GetSegmenterNamesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str

    def __init__(self, *, name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetSegmenterNamesRequest = GetSegmenterNamesRequest

class GetSegmenterNamesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SEGMENTER_NAMES_FIELD_NUMBER: builtins.int

    @property
    def segmenter_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """segmenters in the registry"""

    def __init__(self, *, segmenter_names: collections.abc.Iterable[builtins.str] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['segmenter_names', b'segmenter_names']) -> None:
        ...
global___GetSegmenterNamesResponse = GetSegmenterNamesResponse

class AddSegmenterRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    SEGMENTER_NAME_FIELD_NUMBER: builtins.int
    SEGMENTER_MODEL_TYPE_FIELD_NUMBER: builtins.int
    SEGMENTER_PARAMETERS_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    segmenter_name: builtins.str
    'name of the segmenter'
    segmenter_model_type: builtins.str
    'name of the segmenter model'

    @property
    def segmenter_parameters(self) -> google.protobuf.struct_pb2.Struct:
        """parameters of the segmenter model"""

    def __init__(self, *, name: builtins.str=..., segmenter_name: builtins.str=..., segmenter_model_type: builtins.str=..., segmenter_parameters: google.protobuf.struct_pb2.Struct | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['segmenter_parameters', b'segmenter_parameters']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name', 'segmenter_model_type', b'segmenter_model_type', 'segmenter_name', b'segmenter_name', 'segmenter_parameters', b'segmenter_parameters']) -> None:
        ...
global___AddSegmenterRequest = AddSegmenterRequest

class AddSegmenterResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None:
        ...
global___AddSegmenterResponse = AddSegmenterResponse

class RemoveSegmenterRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    SEGMENTER_NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    'name of the vision service'
    segmenter_name: builtins.str
    'name of segmenter in registry'

    def __init__(self, *, name: builtins.str=..., segmenter_name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name', 'segmenter_name', b'segmenter_name']) -> None:
        ...
global___RemoveSegmenterRequest = RemoveSegmenterRequest

class RemoveSegmenterResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(self) -> None:
        ...
global___RemoveSegmenterResponse = RemoveSegmenterResponse

class GetObjectPointCloudsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    CAMERA_NAME_FIELD_NUMBER: builtins.int
    SEGMENTER_NAME_FIELD_NUMBER: builtins.int
    MIME_TYPE_FIELD_NUMBER: builtins.int
    name: builtins.str
    camera_name: builtins.str
    'Name of a camera'
    segmenter_name: builtins.str
    'Name of the segmentation algorithm'
    mime_type: builtins.str
    'Requested MIME type of response'

    def __init__(self, *, name: builtins.str=..., camera_name: builtins.str=..., segmenter_name: builtins.str=..., mime_type: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['camera_name', b'camera_name', 'mime_type', b'mime_type', 'name', b'name', 'segmenter_name', b'segmenter_name']) -> None:
        ...
global___GetObjectPointCloudsRequest = GetObjectPointCloudsRequest

class GetObjectPointCloudsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MIME_TYPE_FIELD_NUMBER: builtins.int
    OBJECTS_FIELD_NUMBER: builtins.int
    mime_type: builtins.str
    'Actual MIME type of response'

    @property
    def objects(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[common.v1.common_pb2.PointCloudObject]:
        """List of objects in the scene"""

    def __init__(self, *, mime_type: builtins.str=..., objects: collections.abc.Iterable[common.v1.common_pb2.PointCloudObject] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['mime_type', b'mime_type', 'objects', b'objects']) -> None:
        ...
global___GetObjectPointCloudsResponse = GetObjectPointCloudsResponse