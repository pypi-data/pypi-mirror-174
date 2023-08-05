"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright: Ankitects Pty Ltd and contributors
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""
import anki.generic_pb2
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

class OpenCollectionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COLLECTION_PATH_FIELD_NUMBER: builtins.int
    MEDIA_FOLDER_PATH_FIELD_NUMBER: builtins.int
    MEDIA_DB_PATH_FIELD_NUMBER: builtins.int
    LOG_PATH_FIELD_NUMBER: builtins.int
    collection_path: builtins.str
    media_folder_path: builtins.str
    media_db_path: builtins.str
    log_path: builtins.str
    def __init__(
        self,
        *,
        collection_path: builtins.str = ...,
        media_folder_path: builtins.str = ...,
        media_db_path: builtins.str = ...,
        log_path: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["collection_path", b"collection_path", "log_path", b"log_path", "media_db_path", b"media_db_path", "media_folder_path", b"media_folder_path"]) -> None: ...

global___OpenCollectionRequest = OpenCollectionRequest

class CloseCollectionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DOWNGRADE_TO_SCHEMA11_FIELD_NUMBER: builtins.int
    downgrade_to_schema11: builtins.bool
    def __init__(
        self,
        *,
        downgrade_to_schema11: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["downgrade_to_schema11", b"downgrade_to_schema11"]) -> None: ...

global___CloseCollectionRequest = CloseCollectionRequest

class CheckDatabaseResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PROBLEMS_FIELD_NUMBER: builtins.int
    @property
    def problems(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        problems: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["problems", b"problems"]) -> None: ...

global___CheckDatabaseResponse = CheckDatabaseResponse

class OpChanges(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CARD_FIELD_NUMBER: builtins.int
    NOTE_FIELD_NUMBER: builtins.int
    DECK_FIELD_NUMBER: builtins.int
    TAG_FIELD_NUMBER: builtins.int
    NOTETYPE_FIELD_NUMBER: builtins.int
    CONFIG_FIELD_NUMBER: builtins.int
    DECK_CONFIG_FIELD_NUMBER: builtins.int
    MTIME_FIELD_NUMBER: builtins.int
    BROWSER_TABLE_FIELD_NUMBER: builtins.int
    BROWSER_SIDEBAR_FIELD_NUMBER: builtins.int
    NOTE_TEXT_FIELD_NUMBER: builtins.int
    STUDY_QUEUES_FIELD_NUMBER: builtins.int
    card: builtins.bool
    note: builtins.bool
    deck: builtins.bool
    tag: builtins.bool
    notetype: builtins.bool
    config: builtins.bool
    deck_config: builtins.bool
    mtime: builtins.bool
    browser_table: builtins.bool
    browser_sidebar: builtins.bool
    note_text: builtins.bool
    """editor and displayed card in review screen"""
    study_queues: builtins.bool
    """whether to call .reset() and getCard()"""
    def __init__(
        self,
        *,
        card: builtins.bool = ...,
        note: builtins.bool = ...,
        deck: builtins.bool = ...,
        tag: builtins.bool = ...,
        notetype: builtins.bool = ...,
        config: builtins.bool = ...,
        deck_config: builtins.bool = ...,
        mtime: builtins.bool = ...,
        browser_table: builtins.bool = ...,
        browser_sidebar: builtins.bool = ...,
        note_text: builtins.bool = ...,
        study_queues: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["browser_sidebar", b"browser_sidebar", "browser_table", b"browser_table", "card", b"card", "config", b"config", "deck", b"deck", "deck_config", b"deck_config", "mtime", b"mtime", "note", b"note", "note_text", b"note_text", "notetype", b"notetype", "study_queues", b"study_queues", "tag", b"tag"]) -> None: ...

global___OpChanges = OpChanges

class OpChangesWithCount(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COUNT_FIELD_NUMBER: builtins.int
    CHANGES_FIELD_NUMBER: builtins.int
    count: builtins.int
    @property
    def changes(self) -> global___OpChanges: ...
    def __init__(
        self,
        *,
        count: builtins.int = ...,
        changes: global___OpChanges | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["changes", b"changes"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["changes", b"changes", "count", b"count"]) -> None: ...

global___OpChangesWithCount = OpChangesWithCount

class OpChangesWithId(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    CHANGES_FIELD_NUMBER: builtins.int
    id: builtins.int
    @property
    def changes(self) -> global___OpChanges: ...
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        changes: global___OpChanges | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["changes", b"changes"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["changes", b"changes", "id", b"id"]) -> None: ...

global___OpChangesWithId = OpChangesWithId

class UndoStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UNDO_FIELD_NUMBER: builtins.int
    REDO_FIELD_NUMBER: builtins.int
    LAST_STEP_FIELD_NUMBER: builtins.int
    undo: builtins.str
    redo: builtins.str
    last_step: builtins.int
    def __init__(
        self,
        *,
        undo: builtins.str = ...,
        redo: builtins.str = ...,
        last_step: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["last_step", b"last_step", "redo", b"redo", "undo", b"undo"]) -> None: ...

global___UndoStatus = UndoStatus

class OpChangesAfterUndo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CHANGES_FIELD_NUMBER: builtins.int
    OPERATION_FIELD_NUMBER: builtins.int
    REVERTED_TO_TIMESTAMP_FIELD_NUMBER: builtins.int
    NEW_STATUS_FIELD_NUMBER: builtins.int
    COUNTER_FIELD_NUMBER: builtins.int
    @property
    def changes(self) -> global___OpChanges: ...
    operation: builtins.str
    reverted_to_timestamp: builtins.int
    @property
    def new_status(self) -> global___UndoStatus: ...
    counter: builtins.int
    def __init__(
        self,
        *,
        changes: global___OpChanges | None = ...,
        operation: builtins.str = ...,
        reverted_to_timestamp: builtins.int = ...,
        new_status: global___UndoStatus | None = ...,
        counter: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["changes", b"changes", "new_status", b"new_status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["changes", b"changes", "counter", b"counter", "new_status", b"new_status", "operation", b"operation", "reverted_to_timestamp", b"reverted_to_timestamp"]) -> None: ...

global___OpChangesAfterUndo = OpChangesAfterUndo

class Progress(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class MediaSync(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        CHECKED_FIELD_NUMBER: builtins.int
        ADDED_FIELD_NUMBER: builtins.int
        REMOVED_FIELD_NUMBER: builtins.int
        checked: builtins.str
        added: builtins.str
        removed: builtins.str
        def __init__(
            self,
            *,
            checked: builtins.str = ...,
            added: builtins.str = ...,
            removed: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["added", b"added", "checked", b"checked", "removed", b"removed"]) -> None: ...

    class FullSync(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        TRANSFERRED_FIELD_NUMBER: builtins.int
        TOTAL_FIELD_NUMBER: builtins.int
        transferred: builtins.int
        total: builtins.int
        def __init__(
            self,
            *,
            transferred: builtins.int = ...,
            total: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["total", b"total", "transferred", b"transferred"]) -> None: ...

    class NormalSync(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        STAGE_FIELD_NUMBER: builtins.int
        ADDED_FIELD_NUMBER: builtins.int
        REMOVED_FIELD_NUMBER: builtins.int
        stage: builtins.str
        added: builtins.str
        removed: builtins.str
        def __init__(
            self,
            *,
            stage: builtins.str = ...,
            added: builtins.str = ...,
            removed: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["added", b"added", "removed", b"removed", "stage", b"stage"]) -> None: ...

    class DatabaseCheck(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        STAGE_FIELD_NUMBER: builtins.int
        STAGE_TOTAL_FIELD_NUMBER: builtins.int
        STAGE_CURRENT_FIELD_NUMBER: builtins.int
        stage: builtins.str
        stage_total: builtins.int
        stage_current: builtins.int
        def __init__(
            self,
            *,
            stage: builtins.str = ...,
            stage_total: builtins.int = ...,
            stage_current: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["stage", b"stage", "stage_current", b"stage_current", "stage_total", b"stage_total"]) -> None: ...

    NONE_FIELD_NUMBER: builtins.int
    MEDIA_SYNC_FIELD_NUMBER: builtins.int
    MEDIA_CHECK_FIELD_NUMBER: builtins.int
    FULL_SYNC_FIELD_NUMBER: builtins.int
    NORMAL_SYNC_FIELD_NUMBER: builtins.int
    DATABASE_CHECK_FIELD_NUMBER: builtins.int
    IMPORTING_FIELD_NUMBER: builtins.int
    EXPORTING_FIELD_NUMBER: builtins.int
    @property
    def none(self) -> anki.generic_pb2.Empty: ...
    @property
    def media_sync(self) -> global___Progress.MediaSync: ...
    media_check: builtins.str
    @property
    def full_sync(self) -> global___Progress.FullSync: ...
    @property
    def normal_sync(self) -> global___Progress.NormalSync: ...
    @property
    def database_check(self) -> global___Progress.DatabaseCheck: ...
    importing: builtins.str
    exporting: builtins.str
    def __init__(
        self,
        *,
        none: anki.generic_pb2.Empty | None = ...,
        media_sync: global___Progress.MediaSync | None = ...,
        media_check: builtins.str = ...,
        full_sync: global___Progress.FullSync | None = ...,
        normal_sync: global___Progress.NormalSync | None = ...,
        database_check: global___Progress.DatabaseCheck | None = ...,
        importing: builtins.str = ...,
        exporting: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["database_check", b"database_check", "exporting", b"exporting", "full_sync", b"full_sync", "importing", b"importing", "media_check", b"media_check", "media_sync", b"media_sync", "none", b"none", "normal_sync", b"normal_sync", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["database_check", b"database_check", "exporting", b"exporting", "full_sync", b"full_sync", "importing", b"importing", "media_check", b"media_check", "media_sync", b"media_sync", "none", b"none", "normal_sync", b"normal_sync", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value", b"value"]) -> typing_extensions.Literal["none", "media_sync", "media_check", "full_sync", "normal_sync", "database_check", "importing", "exporting"] | None: ...

global___Progress = Progress

class CreateBackupRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BACKUP_FOLDER_FIELD_NUMBER: builtins.int
    FORCE_FIELD_NUMBER: builtins.int
    WAIT_FOR_COMPLETION_FIELD_NUMBER: builtins.int
    backup_folder: builtins.str
    force: builtins.bool
    """Create a backup even if the configured interval hasn't elapsed yet."""
    wait_for_completion: builtins.bool
    def __init__(
        self,
        *,
        backup_folder: builtins.str = ...,
        force: builtins.bool = ...,
        wait_for_completion: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["backup_folder", b"backup_folder", "force", b"force", "wait_for_completion", b"wait_for_completion"]) -> None: ...

global___CreateBackupRequest = CreateBackupRequest
