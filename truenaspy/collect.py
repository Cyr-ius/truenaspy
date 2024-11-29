"""Class to collect a data."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from mashumaro import DataClassDictMixin, field_options

from .helper import b2gib, utc_from_timestamp


@dataclass
class System(DataClassDictMixin):  # type: ignore
    """System."""

    version: str
    hostname: str
    system_serial: str
    system_product: str
    system_manufacturer: str
    uptime_seconds: int = 0


@dataclass
class Update(DataClassDictMixin):  # type: ignore
    """Update."""

    available: UpdateStatus
    version: UpdateVersion
    job_id: int
    progress: int


@dataclass
class UpdateStatus(DataClassDictMixin):  # type: ignore
    status: str
    available: bool | None = field(
        metadata=field_options(deserialize=lambda x: x == "AVAILABLE"), default=None
    )


@dataclass
class UpdateVersion(DataClassDictMixin):  # type: ignore
    version: str


@dataclass
class Job(DataClassDictMixin):  # type: ignore
    """Job."""

    progress: Progress
    state: State


@dataclass
class Interfaces(DataClassDictMixin):  # type: ignore
    Interfaces: list[Interface]


@dataclass
class Interface(DataClassDictMixin):  # type: ignore
    id: str
    name: str
    description: str
    state: InterfaceState
    mtu: int | None = None


@dataclass
class InterfaceState(DataClassDictMixin):  # type: ignore
    link_state: str
    active_media_type: str
    link_address: str


@dataclass
class Services(DataClassDictMixin):  # type: ignore
    services: list[Service]


@dataclass
class Service(DataClassDictMixin):  # type: ignore
    id: int
    service: str
    enable: bool = False
    # state: State


@dataclass
class Pool(DataClassDictMixin):  # type: ignore
    id: int
    autotrim: AutoTrim
    guid: str
    healthy: bool
    name: str
    path: str
    scan: Scan
    status: str
    is_decrypted: bool | None = None


@dataclass
class AutoTrim(DataClassDictMixin):  # type: ignore
    parsed: bool


@dataclass
class Scan(DataClassDictMixin):  # type: ignore
    function: str
    state: str
    scrub_start: DateTime = field(metadata=field_options(alias="start_time"))
    scrub_end: DateTime = field(metadata=field_options(alias="end_time"))
    # scrub_end: StopTime = field(metadata=field_options(alias="end_time"))
    scrub_secs_left: int | None = field(metadata=field_options(alias="total_secs_left"))


@dataclass
class Boot(DataClassDictMixin):  # type: ignore
    name: str
    path: str
    status: str
    healthy: bool
    autotrim: AutoTrim
    scan: Scan
    used: int = field(metadata=field_options(alias="allocated"), default=0)
    available: int = field(metadata=field_options(alias="free"), default=0)
    size: int = 0
    id: int = 0
    guid: str = "boot"
    root_dataset: RootDataset | None = None
    is_decrypted: bool | None = None


@dataclass
class RootDataset(DataClassDictMixin):  # type: ignore
    properties: Properties


@dataclass
class Properties(DataClassDictMixin):  # type: ignore
    used: Parsed
    available: Parsed


@dataclass
class Disk(DataClassDictMixin):  # type: ignore
    name: str
    devname: str
    serial: str
    size: int
    advpowermgmt: str
    togglesmart: bool
    model: str
    rotationrate: str
    type: str
    acousticlevel: str | None = None
    hddstandby_force: bool | None = None


@dataclass
class Jail(DataClassDictMixin):  # type: ignore
    """Jail."""

    id: str
    comment: str
    host_hostname: str
    jail_zfs_dataset: str
    last_started: str
    ip4_addr: str
    ip6_addr: str
    release: str
    state: bool
    type: str
    plugin_name: str


@dataclass
class VirtualMachine(DataClassDictMixin):  # type: ignore
    """VirtualMachine."""

    id: int
    name: str
    description: str
    vcpus: int
    memory: int
    autostart: bool
    cores: int
    threads: int
    status: State


@dataclass
class Dataset(DataClassDictMixin):  # type: ignore
    available: Parsed
    checksum: Parsed
    compression: Parsed
    copies: Parsed
    deduplication: Parsed
    encrypted: bool
    id: str
    locked: str
    mountpoint: str
    name: str
    pool: str
    readonly: Parsed
    sync: Parsed
    type: str
    used: Parsed
    used_gb: Parsed | None = field(
        metadata=field_options(deserialize=lambda x: 0 if not x else b2gib(x)),
        default=None,
    )
    recordsize: Parsed | None = None
    quota: Parsed | None = None
    exec: Parsed | None = None
    comments: Parsed | None = None
    casesensitivity: Parsed | None = None
    atime: Parsed | None = None


@dataclass
class CloudSync(DataClassDictMixin):  # type: ignore
    id: int
    description: str
    direction: str
    path: str
    enabled: bool
    transfer_mode: str
    snapshot: bool
    state: Job


@dataclass
class Replication(DataClassDictMixin):  # type: ignore
    id: int
    name: str
    source_datasets: str
    target_dataset: str
    recursive: bool
    enabled: bool
    direction: str
    transport: str
    auto: bool
    retention_policy: str
    state: Job


@dataclass
class Snapshottask(DataClassDictMixin):  # type: ignore
    id: int
    dataset: str
    recursive: bool
    lifetime_value: str
    lifetime_unit: str
    enabled: bool
    naming_schema: str
    allow_empty: bool
    vmware_sync: bool
    state: Job


@dataclass
class Charts(DataClassDictMixin):  # type: ignore
    id: int
    name: str
    description: str
    meta_version: str
    meta_app_version: str
    meta_latests_version: bool
    human_version: str
    human_latest_version: str
    update_available: str
    container_images_update_available: str
    portal: Portals
    status: State


@dataclass
class Apps(DataClassDictMixin):  # type: ignore
    apps: list[Alert]


@dataclass
class App(DataClassDictMixin):  # type: ignore
    id: str
    name: str
    state: bool | None = field(
        metadata=field_options(deserialize=lambda x: x == "RUNNING"), default=None
    )
    upgrade_available: bool | None = None
    image_updates_available: bool | None = None
    human_version: str | None = None
    version: str | None = None
    portal: dict[str, Any] | None = None


@dataclass
class Docker(DataClassDictMixin):  # type: ignore
    description: str
    status: bool | None = field(
        metadata=field_options(deserialize=lambda x: x == "RUNNING"), default=None
    )


@dataclass
class Smart(DataClassDictMixin):  # type: ignore
    name: str
    serial: str
    model: str
    zfs_guid: str
    devname: bool
    tests: StateTest


@dataclass
class Alerts(DataClassDictMixin):  # type: ignore
    alerts: list[Alert]


@dataclass
class Alert(DataClassDictMixin):  # type: ignore
    uuid: str
    formatted: str
    klass: str
    level: str
    date_created: DateTime = field(metadata=field_options(alias="datetime"))
    last_occurrence: DateTime


@dataclass
class Rsync(DataClassDictMixin):  # type: ignore
    id: int
    desc: str


@dataclass
class Portals(DataClassDictMixin):  # type: ignore
    open: str | None = field(
        metadata=field_options(
            deserialize=lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
        ),
        default=None,
    )


@dataclass
class StateTest(DataClassDictMixin):  # type: ignore
    status: str | None = field(
        metadata=field_options(
            deserialize=lambda x: x[0].get("status") != "SUCCESS"
            if isinstance(x, list) and len(x) > 0
            else False
        ),
        default=None,
    )


@dataclass
class State(DataClassDictMixin):  # type: ignore
    running: bool | None = field(
        metadata=field_options(deserialize=lambda x: x == "RUNNING"), default=None
    )


@dataclass
class Parsed(DataClassDictMixin):  # type: ignore
    parsed: str


@dataclass
class StartTime:
    start_time: DateTime


@dataclass
class StopTime:
    stop_time: DateTime


@dataclass
class DateTime(DataClassDictMixin):  # type: ignore
    date: datetime = field(
        metadata=field_options(
            deserialize=lambda x: utc_from_timestamp(
                x if x < 100000000000 else x / 1000
            ),
            alias="$date",
        )
    )


@dataclass
class Progress(DataClassDictMixin):  # type: ignore
    """Jobs."""

    percent: int = 0