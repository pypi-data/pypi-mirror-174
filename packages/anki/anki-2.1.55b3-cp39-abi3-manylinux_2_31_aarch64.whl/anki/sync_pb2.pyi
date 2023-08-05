"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class SyncAuth(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HKEY_FIELD_NUMBER: builtins.int
    HOST_NUMBER_FIELD_NUMBER: builtins.int
    hkey: builtins.str
    host_number: builtins.int
    def __init__(
        self,
        *,
        hkey: builtins.str = ...,
        host_number: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["hkey", b"hkey", "host_number", b"host_number"]) -> None: ...

global___SyncAuth = SyncAuth

class SyncLoginRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USERNAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    username: builtins.str
    password: builtins.str
    def __init__(
        self,
        *,
        username: builtins.str = ...,
        password: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["password", b"password", "username", b"username"]) -> None: ...

global___SyncLoginRequest = SyncLoginRequest

class SyncStatusResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Required:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _RequiredEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SyncStatusResponse._Required.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        NO_CHANGES: SyncStatusResponse._Required.ValueType  # 0
        NORMAL_SYNC: SyncStatusResponse._Required.ValueType  # 1
        FULL_SYNC: SyncStatusResponse._Required.ValueType  # 2

    class Required(_Required, metaclass=_RequiredEnumTypeWrapper): ...
    NO_CHANGES: SyncStatusResponse.Required.ValueType  # 0
    NORMAL_SYNC: SyncStatusResponse.Required.ValueType  # 1
    FULL_SYNC: SyncStatusResponse.Required.ValueType  # 2

    REQUIRED_FIELD_NUMBER: builtins.int
    required: global___SyncStatusResponse.Required.ValueType
    def __init__(
        self,
        *,
        required: global___SyncStatusResponse.Required.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["required", b"required"]) -> None: ...

global___SyncStatusResponse = SyncStatusResponse

class SyncCollectionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _ChangesRequired:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ChangesRequiredEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SyncCollectionResponse._ChangesRequired.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        NO_CHANGES: SyncCollectionResponse._ChangesRequired.ValueType  # 0
        NORMAL_SYNC: SyncCollectionResponse._ChangesRequired.ValueType  # 1
        FULL_SYNC: SyncCollectionResponse._ChangesRequired.ValueType  # 2
        FULL_DOWNLOAD: SyncCollectionResponse._ChangesRequired.ValueType  # 3
        """local collection has no cards; upload not an option"""
        FULL_UPLOAD: SyncCollectionResponse._ChangesRequired.ValueType  # 4
        """remote collection has no cards; download not an option"""

    class ChangesRequired(_ChangesRequired, metaclass=_ChangesRequiredEnumTypeWrapper): ...
    NO_CHANGES: SyncCollectionResponse.ChangesRequired.ValueType  # 0
    NORMAL_SYNC: SyncCollectionResponse.ChangesRequired.ValueType  # 1
    FULL_SYNC: SyncCollectionResponse.ChangesRequired.ValueType  # 2
    FULL_DOWNLOAD: SyncCollectionResponse.ChangesRequired.ValueType  # 3
    """local collection has no cards; upload not an option"""
    FULL_UPLOAD: SyncCollectionResponse.ChangesRequired.ValueType  # 4
    """remote collection has no cards; download not an option"""

    HOST_NUMBER_FIELD_NUMBER: builtins.int
    SERVER_MESSAGE_FIELD_NUMBER: builtins.int
    REQUIRED_FIELD_NUMBER: builtins.int
    host_number: builtins.int
    server_message: builtins.str
    required: global___SyncCollectionResponse.ChangesRequired.ValueType
    def __init__(
        self,
        *,
        host_number: builtins.int = ...,
        server_message: builtins.str = ...,
        required: global___SyncCollectionResponse.ChangesRequired.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["host_number", b"host_number", "required", b"required", "server_message", b"server_message"]) -> None: ...

global___SyncCollectionResponse = SyncCollectionResponse

class SyncServerMethodRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Method:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _MethodEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SyncServerMethodRequest._Method.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        HOST_KEY: SyncServerMethodRequest._Method.ValueType  # 0
        META: SyncServerMethodRequest._Method.ValueType  # 1
        START: SyncServerMethodRequest._Method.ValueType  # 2
        APPLY_GRAVES: SyncServerMethodRequest._Method.ValueType  # 3
        APPLY_CHANGES: SyncServerMethodRequest._Method.ValueType  # 4
        CHUNK: SyncServerMethodRequest._Method.ValueType  # 5
        APPLY_CHUNK: SyncServerMethodRequest._Method.ValueType  # 6
        SANITY_CHECK: SyncServerMethodRequest._Method.ValueType  # 7
        FINISH: SyncServerMethodRequest._Method.ValueType  # 8
        ABORT: SyncServerMethodRequest._Method.ValueType  # 9
        FULL_UPLOAD: SyncServerMethodRequest._Method.ValueType  # 10
        """caller must reopen after these two are called"""
        FULL_DOWNLOAD: SyncServerMethodRequest._Method.ValueType  # 11

    class Method(_Method, metaclass=_MethodEnumTypeWrapper): ...
    HOST_KEY: SyncServerMethodRequest.Method.ValueType  # 0
    META: SyncServerMethodRequest.Method.ValueType  # 1
    START: SyncServerMethodRequest.Method.ValueType  # 2
    APPLY_GRAVES: SyncServerMethodRequest.Method.ValueType  # 3
    APPLY_CHANGES: SyncServerMethodRequest.Method.ValueType  # 4
    CHUNK: SyncServerMethodRequest.Method.ValueType  # 5
    APPLY_CHUNK: SyncServerMethodRequest.Method.ValueType  # 6
    SANITY_CHECK: SyncServerMethodRequest.Method.ValueType  # 7
    FINISH: SyncServerMethodRequest.Method.ValueType  # 8
    ABORT: SyncServerMethodRequest.Method.ValueType  # 9
    FULL_UPLOAD: SyncServerMethodRequest.Method.ValueType  # 10
    """caller must reopen after these two are called"""
    FULL_DOWNLOAD: SyncServerMethodRequest.Method.ValueType  # 11

    METHOD_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    method: global___SyncServerMethodRequest.Method.ValueType
    data: builtins.bytes
    def __init__(
        self,
        *,
        method: global___SyncServerMethodRequest.Method.ValueType = ...,
        data: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data", "method", b"method"]) -> None: ...

global___SyncServerMethodRequest = SyncServerMethodRequest
