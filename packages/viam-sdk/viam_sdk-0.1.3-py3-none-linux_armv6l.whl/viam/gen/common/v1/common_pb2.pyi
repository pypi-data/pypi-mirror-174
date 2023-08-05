"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
The following is a list of messages that are used across multiple resource subtypes"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys
if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ResourceName(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAMESPACE_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    SUBTYPE_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    namespace: builtins.str
    type: builtins.str
    subtype: builtins.str
    name: builtins.str

    def __init__(self, *, namespace: builtins.str=..., type: builtins.str=..., subtype: builtins.str=..., name: builtins.str=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name', 'namespace', b'namespace', 'subtype', b'subtype', 'type', b'type']) -> None:
        ...
global___ResourceName = ResourceName

class BoardStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class AnalogsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str

        @property
        def value(self) -> global___AnalogStatus:
            ...

        def __init__(self, *, key: builtins.str=..., value: global___AnalogStatus | None=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['value', b'value']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['key', b'key', 'value', b'value']) -> None:
            ...

    class DigitalInterruptsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str

        @property
        def value(self) -> global___DigitalInterruptStatus:
            ...

        def __init__(self, *, key: builtins.str=..., value: global___DigitalInterruptStatus | None=...) -> None:
            ...

        def HasField(self, field_name: typing_extensions.Literal['value', b'value']) -> builtins.bool:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['key', b'key', 'value', b'value']) -> None:
            ...
    ANALOGS_FIELD_NUMBER: builtins.int
    DIGITAL_INTERRUPTS_FIELD_NUMBER: builtins.int

    @property
    def analogs(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___AnalogStatus]:
        ...

    @property
    def digital_interrupts(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___DigitalInterruptStatus]:
        ...

    def __init__(self, *, analogs: collections.abc.Mapping[builtins.str, global___AnalogStatus] | None=..., digital_interrupts: collections.abc.Mapping[builtins.str, global___DigitalInterruptStatus] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['analogs', b'analogs', 'digital_interrupts', b'digital_interrupts']) -> None:
        ...
global___BoardStatus = BoardStatus

class AnalogStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.int
    "Current value of the analog reader of a robot's board"

    def __init__(self, *, value: builtins.int=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['value', b'value']) -> None:
        ...
global___AnalogStatus = AnalogStatus

class DigitalInterruptStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.int
    "Current value of the digital interrupt of a robot's board"

    def __init__(self, *, value: builtins.int=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['value', b'value']) -> None:
        ...
global___DigitalInterruptStatus = DigitalInterruptStatus

class Pose(google.protobuf.message.Message):
    """Pose is a combination of location and orientation.
    Location is expressed as distance which is represented by x , y, z coordinates. Orientation is expressed as an orientation vector which
    is represented by o_x, o_y, o_z and theta. The o_x, o_y, o_z coordinates represent the point on the cartesian unit sphere that the end of
    the arm is pointing to (with the origin as reference). That unit vector forms an axis around which theta rotates. This means that
    incrementing / decrementing theta will perform an inline rotation of the end effector.
    Theta is defined as rotation between two planes: the first being defined by the origin, the point (0,0,1), and the rx, ry, rz point, and the
    second being defined by the origin, the rx, ry, rz point and the local Z axis. Therefore, if theta is kept at zero as the north/south pole
    is circled, the Roll will correct itself to remain in-line.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    O_X_FIELD_NUMBER: builtins.int
    O_Y_FIELD_NUMBER: builtins.int
    O_Z_FIELD_NUMBER: builtins.int
    THETA_FIELD_NUMBER: builtins.int
    x: builtins.float
    'millimeters from the origin'
    y: builtins.float
    'millimeters from the origin'
    z: builtins.float
    'millimeters from the origin'
    o_x: builtins.float
    'z component of a vector defining axis of rotation'
    o_y: builtins.float
    'x component of a vector defining axis of rotation'
    o_z: builtins.float
    'y component of a vector defining axis of rotation'
    theta: builtins.float
    'degrees'

    def __init__(self, *, x: builtins.float=..., y: builtins.float=..., z: builtins.float=..., o_x: builtins.float=..., o_y: builtins.float=..., o_z: builtins.float=..., theta: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['o_x', b'o_x', 'o_y', b'o_y', 'o_z', b'o_z', 'theta', b'theta', 'x', b'x', 'y', b'y', 'z', b'z']) -> None:
        ...
global___Pose = Pose

class Orientation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    O_X_FIELD_NUMBER: builtins.int
    O_Y_FIELD_NUMBER: builtins.int
    O_Z_FIELD_NUMBER: builtins.int
    THETA_FIELD_NUMBER: builtins.int
    o_x: builtins.float
    'x component of a vector defining axis of rotation'
    o_y: builtins.float
    'y component of a vector defining axis of rotation'
    o_z: builtins.float
    'z component of a vector defining axis of rotation'
    theta: builtins.float
    'degrees'

    def __init__(self, *, o_x: builtins.float=..., o_y: builtins.float=..., o_z: builtins.float=..., theta: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['o_x', b'o_x', 'o_y', b'o_y', 'o_z', b'o_z', 'theta', b'theta']) -> None:
        ...
global___Orientation = Orientation

class PoseInFrame(google.protobuf.message.Message):
    """PoseInFrame contains a pose and the and the reference frame in which it was observed"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    REFERENCE_FRAME_FIELD_NUMBER: builtins.int
    POSE_FIELD_NUMBER: builtins.int
    reference_frame: builtins.str

    @property
    def pose(self) -> global___Pose:
        ...

    def __init__(self, *, reference_frame: builtins.str=..., pose: global___Pose | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['pose', b'pose']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['pose', b'pose', 'reference_frame', b'reference_frame']) -> None:
        ...
global___PoseInFrame = PoseInFrame

class Vector3(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    z: builtins.float

    def __init__(self, *, x: builtins.float=..., y: builtins.float=..., z: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['x', b'x', 'y', b'y', 'z', b'z']) -> None:
        ...
global___Vector3 = Vector3

class Sphere(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RADIUS_MM_FIELD_NUMBER: builtins.int
    radius_mm: builtins.float

    def __init__(self, *, radius_mm: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['radius_mm', b'radius_mm']) -> None:
        ...
global___Sphere = Sphere

class RectangularPrism(google.protobuf.message.Message):
    """RectangularPrism contains a Vector3 field corresponding to the X, Y, Z dimensions of the prism in mms
    These dimensions are with respect to the referenceframe in which the RectangularPrism is defined
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DIMS_MM_FIELD_NUMBER: builtins.int

    @property
    def dims_mm(self) -> global___Vector3:
        ...

    def __init__(self, *, dims_mm: global___Vector3 | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['dims_mm', b'dims_mm']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['dims_mm', b'dims_mm']) -> None:
        ...
global___RectangularPrism = RectangularPrism

class Geometry(google.protobuf.message.Message):
    """Geometry contains the dimensions of a given geometry and the pose of its center. The geometry is one of either a sphere or a box."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CENTER_FIELD_NUMBER: builtins.int
    SPHERE_FIELD_NUMBER: builtins.int
    BOX_FIELD_NUMBER: builtins.int
    LABEL_FIELD_NUMBER: builtins.int

    @property
    def center(self) -> global___Pose:
        """Pose of a gemetries center point"""

    @property
    def sphere(self) -> global___Sphere:
        ...

    @property
    def box(self) -> global___RectangularPrism:
        ...
    label: builtins.str
    'Label of the geometry. If none supplied, will be an empty string.'

    def __init__(self, *, center: global___Pose | None=..., sphere: global___Sphere | None=..., box: global___RectangularPrism | None=..., label: builtins.str=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['box', b'box', 'center', b'center', 'geometry_type', b'geometry_type', 'sphere', b'sphere']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['box', b'box', 'center', b'center', 'geometry_type', b'geometry_type', 'label', b'label', 'sphere', b'sphere']) -> None:
        ...

    def WhichOneof(self, oneof_group: typing_extensions.Literal['geometry_type', b'geometry_type']) -> typing_extensions.Literal['sphere', 'box'] | None:
        ...
global___Geometry = Geometry

class GeometriesInFrame(google.protobuf.message.Message):
    """GeometriesinFrame contains the dimensions of a given geometry, pose of its center point, and the reference frame by which it was
    observed.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    REFERENCE_FRAME_FIELD_NUMBER: builtins.int
    GEOMETRIES_FIELD_NUMBER: builtins.int
    reference_frame: builtins.str
    'Reference frame of the observer of the geometry'

    @property
    def geometries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Geometry]:
        """Dimensional type"""

    def __init__(self, *, reference_frame: builtins.str=..., geometries: collections.abc.Iterable[global___Geometry] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['geometries', b'geometries', 'reference_frame', b'reference_frame']) -> None:
        ...
global___GeometriesInFrame = GeometriesInFrame

class PointCloudObject(google.protobuf.message.Message):
    """PointCloudObject contains an image in bytes with point cloud data of all of the objects captured by a given observer as well as a
    repeated list of geometries which respresents the center point and geometry of each of the objects within the point cloud
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    POINT_CLOUD_FIELD_NUMBER: builtins.int
    GEOMETRIES_FIELD_NUMBER: builtins.int
    point_cloud: builtins.bytes
    'image frame expressed in bytes'

    @property
    def geometries(self) -> global___GeometriesInFrame:
        """volume of a given geometry"""

    def __init__(self, *, point_cloud: builtins.bytes=..., geometries: global___GeometriesInFrame | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['geometries', b'geometries']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['geometries', b'geometries', 'point_cloud', b'point_cloud']) -> None:
        ...
global___PointCloudObject = PointCloudObject

class GeoPoint(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LATITUDE_FIELD_NUMBER: builtins.int
    LONGITUDE_FIELD_NUMBER: builtins.int
    latitude: builtins.float
    longitude: builtins.float

    def __init__(self, *, latitude: builtins.float=..., longitude: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['latitude', b'latitude', 'longitude', b'longitude']) -> None:
        ...
global___GeoPoint = GeoPoint

class Transform(google.protobuf.message.Message):
    """Transform contains a pose and two reference frames. The first reference frame is the starting reference frame, and the second reference
    frame is the observer reference frame. The second reference frame has a pose which represents the pose of an object in the first
    reference frame as observed within the second reference frame.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    REFERENCE_FRAME_FIELD_NUMBER: builtins.int
    POSE_IN_OBSERVER_FRAME_FIELD_NUMBER: builtins.int
    reference_frame: builtins.str
    'the name of a given reference frame'

    @property
    def pose_in_observer_frame(self) -> global___PoseInFrame:
        """the pose of the above reference frame with respect to a different observer reference frame"""

    def __init__(self, *, reference_frame: builtins.str=..., pose_in_observer_frame: global___PoseInFrame | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['pose_in_observer_frame', b'pose_in_observer_frame']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['pose_in_observer_frame', b'pose_in_observer_frame', 'reference_frame', b'reference_frame']) -> None:
        ...
global___Transform = Transform

class WorldState(google.protobuf.message.Message):
    """WorldState contains information about the physical environment around a given robot. All of the fields within this message are optional,
    they can include information about the physical dimensions of an obstacle, the freespace of a robot, and any desired transforms between a
    given reference frame and a new target reference frame.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    OBSTACLES_FIELD_NUMBER: builtins.int
    INTERACTION_SPACES_FIELD_NUMBER: builtins.int
    TRANSFORMS_FIELD_NUMBER: builtins.int

    @property
    def obstacles(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GeometriesInFrame]:
        """a list of obstacles expressed as a geometry and the reference frame in which it was observed; this field is optional"""

    @property
    def interaction_spaces(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GeometriesInFrame]:
        """a list of spaces the robot is allowed to operate within expressed as a geometry and the reference frame it is measured fom;
        this field is optional
        """

    @property
    def transforms(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Transform]:
        """a list of Transforms needed to transform a pose from one reference frame to another; this field is optional"""

    def __init__(self, *, obstacles: collections.abc.Iterable[global___GeometriesInFrame] | None=..., interaction_spaces: collections.abc.Iterable[global___GeometriesInFrame] | None=..., transforms: collections.abc.Iterable[global___Transform] | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['interaction_spaces', b'interaction_spaces', 'obstacles', b'obstacles', 'transforms', b'transforms']) -> None:
        ...
global___WorldState = WorldState

class ActuatorStatus(google.protobuf.message.Message):
    """ActuatorStatus is a generic status for resources that only need to return actuator status."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    IS_MOVING_FIELD_NUMBER: builtins.int
    is_moving: builtins.bool

    def __init__(self, *, is_moving: builtins.bool=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['is_moving', b'is_moving']) -> None:
        ...
global___ActuatorStatus = ActuatorStatus