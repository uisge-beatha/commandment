from enum import Enum
from uuid import uuid4
from typing import Set
import semver
from . import AccessRights, Platform


class Command(object):

    def __init__(self, uuid=None):
        if uuid is None:
            uuid = uuid4()

        self._uuid = uuid


class DeviceInformation(Command):
    request_type = 'DeviceInformation'
    require_access = {AccessRights.QueryDeviceInformation, AccessRights.QueryNetworkInformation}

    class Queries(Enum):
        """The Queries enumeration contains all possible Query types for the DeviceInformation command."""

        # Table 5 : General Queries
        UDID = 'UDID'
        Languages = 'Languages'
        Locales = 'Locales'
        DeviceID = 'DeviceID'
        OrganizationInfo = 'OrganizationInfo'
        LastCloudBackupDate = 'LastCloudBackupDate'
        AwaitingConfiguration = 'AwaitingConfiguration'
        AutoSetupAdminAccounts = 'AutoSetupAdminAccounts'

        # Table 6 : iTunes Account
        iTunesStoreAccountIsActive = 'iTunesStoreAccountIsActive'
        iTunesStoreAccountHash = 'iTunesStoreAccountHash'

        # Table 7 : Device Queries
        DeviceName = 'DeviceName'
        OSVersion = 'OSVersion'
        BuildVersion = 'BuildVersion'
        ModelName = 'ModelName'
        Model = 'Model'
        ProductName = 'ProductName'
        SerialNumber = 'SerialNumber'
        DeviceCapacity = 'DeviceCapacity'
        AvailableDeviceCapacity = 'AvailableDeviceCapacity'
        BatteryLevel = 'BatteryLevel'
        CellularTechnology = 'CellularTechnology'
        IMEI = 'IMEI'
        MEID = 'MEID'
        ModemFirmwareVersion = 'ModemFirmwareVersion'
        IsSupervised = 'IsSupervised'
        IsDeviceLocatorServiceEnabled = 'IsDeviceLocatorServiceEnabled'
        IsActivationLockEnabled = 'IsActivationLockEnabled'
        IsDoNotDisturbInEffect = 'IsDoNotDisturbInEffect'
        EASDeviceIdentifier = 'EASDeviceIdentifier'
        IsCloudBackupEnabled = 'IsCloudBackupEnabled'
        OSUpdateSettings = 'OSUpdateSettings'
        LocalHostName = 'LocalHostName'
        HostName = 'HostName'
        SystemIntegrityProtectionEnabled = 'SystemIntegrityProtectionEnabled'
        ActiveManagedUsers = 'ActiveManagedUsers'
        IsMDMLostModeEnabled = 'IsMDMLostModeEnabled'
        MaximumResidentUsers = 'MaximumResidentUsers'

        # Table 9 : Network Information Queries
        ICCID = 'ICCID'
        BluetoothMAC = 'BluetoothMAC'
        WiFiMAC = 'WiFiMAC'
        EthernetMACs = 'EthernetMACs'
        CurrentCarrierNetwork = 'CurrentCarrierNetwork'
        SIMCarrierNetwork = 'SIMCarrierNetwork'
        SubscriberCarrierNetwork = 'SubscriberCarrierNetwork'
        CarrierSettingsVersion = 'CarrierSettingsVersion'
        PhoneNumber = 'PhoneNumber'
        VoiceRoamingEnabled = 'VoiceRoamingEnabled'
        DataRoamingEnabled = 'DataRoamingEnabled'
        IsRoaming = 'IsRoaming'
        PersonalHotspotEnabled = 'PersonalHotspotEnabled'
        SubscriberMCC = 'SubscriberMCC'
        SubscriberMNC = 'SubscriberMNC'
        CurrentMCC = 'CurrentMCC'
        CurrentMNC = 'CurrentMNC'
        
    Requirements = {
        'Languages': [
            (Platform.iOS, '>=7'),
            (Platform.tvOS, '>=6'),
            (Platform.macOS, '>=10.10'),
        ],
        'Locales': [
            (Platform.iOS, '>=7'),
            (Platform.tvOS, '>=6'),
            (Platform.macOS, '>=10.10'),
        ],
        'DeviceID': [
            (Platform.tvOS, '>=6'),
        ],
        'OrganizationInfo': [
            (Platform.iOS, '>=7'),
        ],
        'LastCloudBackupDate': [
            (Platform.iOS, '>=8'),
            (Platform.macOS, '>=10.10')
        ],
        'AwaitingConfiguration': [
            (Platform.iOS, '>=9'),
        ],
        'AutoSetupAdminAccounts': [
            (Platform.macOS, '>=10.11')
        ],
        'BatteryLevel': [
            (Platform.iOS, '>=5')
        ],
        'CellularTechnology': [
            (Platform.iOS, '>=4.2.6')
        ],
        'iTunesStoreAccountIsActive': [
            (Platform.iOS, '>=7'),
            (Platform.macOS, '>=10.9')
        ],
        'iTunesStoreAccountHash': [
            (Platform.iOS, '>=8'),
            (Platform.macOS, '>=10.10')
        ],
        'IMEI': [
            (Platform.iOS, '*'),
        ],
        'MEID': [
            (Platform.iOS, '*'),
        ],
        'ModemFirmwareVersion': [
            (Platform.iOS, '*'),
        ],
        'IsSupervised': [
            (Platform.iOS, '>=6'),
        ],
        'IsDeviceLocatorServiceEnabled': [
            (Platform.iOS, '>=7'),
        ],
        'IsActivationLockEnabled': [
            (Platform.iOS, '>=7'),
            (Platform.macOS, '>=10.9')
        ],
        'IsDoNotDisturbInEffect': [
            (Platform.iOS, '>=7'),
        ],
        'EASDeviceIdentifier': [
            (Platform.iOS, '>=7'),
            (Platform.macOS, '>=10.9'),
        ],
        'IsCloudBackupEnabled': [
            (Platform.iOS, '>=7.1'),
        ],
        'OSUpdateSettings': [
            (Platform.macOS, '>=10.11'),
        ],
        'LocalHostName': [
            (Platform.macOS, '>=10.11'),
        ],
        'HostName': [
            (Platform.macOS, '>=10.11'),
        ],
        'SystemIntegrityProtectionEnabled': [
            (Platform.macOS, '>=10.12'),
        ],
        'ActiveManagedUsers': [
            (Platform.macOS, '>=10.11'),
        ],
        'IsMDMLostModeEnabled': [
            (Platform.iOS, '>=9.3'),
        ],
        'MaximumResidentUsers': [
            (Platform.iOS, '>=9.3'),
        ]
    }

    def __init__(self, uuid=None, **kwargs):
        super(DeviceInformation, self).__init__(uuid)
        self._attrs = kwargs

    @classmethod
    def for_platform(cls, platform: Platform, min_os_version: str, queries: Set[Queries] = None):
        """Generate a command that is compatible with the specified platform and OS version.

        Args:
              platform (Platform): Desired target platform
              min_os_version (str): Desired OS version
              queries (Set[Queries]): Desired Queries, or default to ALL queries.

        Returns:
              DeviceInformation instance with supported queries.
        """

        def supported(query: cls.Queries) -> bool:
            if query.value not in cls.Requirements:
                return True

            platforms = cls.Requirements[query.value]
            for req_platform, req_min_version in platforms:
                if req_platform != platform:
                    continue

                return semver.match(min_os_version, req_min_version)
                
            return False
            
        if queries is None:
            supported_queries = filter(supported, [q for q in cls.Queries])
        else:
            supported_queries = filter(supported, queries)

        return cls(Queries=supported_queries)


class SecurityInfo(Command):
    request_type = 'SecurityInfo'
    require_access = {AccessRights.SecurityQueries}

    def __init__(self, uuid=None, **kwargs):
        super(SecurityInfo, self).__init__(uuid)
        self._attrs = kwargs


class DeviceLock(Command):
    request_type = 'DeviceLock'
    require_access = {AccessRights.DeviceLockPasscodeRemoval}

    def __init__(self, uuid=None, **kwargs):
        super(DeviceLock, self).__init__(uuid)
        self._attrs = kwargs


class ProfileList(Command):
    request_type = 'ProfileList'
    require_access = {AccessRights.ProfileInspection}

    def __init__(self, uuid=None, **kwargs):
        super(ProfileList, self).__init__(uuid)
        self._attrs = kwargs


class InstallProfile(Command):
    request_type = 'InstallProfile'
    require_access = {AccessRights.ProfileInstallRemove}

    def __init__(self, uuid=None, **kwargs):
        super(InstallProfile, self).__init__(uuid)
        self._attrs = kwargs


class RemoveProfile(Command):
    request_type = 'RemoveProfile'
    require_access = {AccessRights.ProfileInstallRemove}

    def __init__(self, uuid=None, **kwargs):
        super(RemoveProfile, self).__init__(uuid)
        self._attrs = kwargs


class CertificateList(Command):
    request_type = 'CertificateList'
    require_access = {AccessRights.ProfileInspection}

    def __init__(self, uuid=None, **kwargs):
        super(CertificateList, self).__init__(uuid)
        self._attrs = kwargs


class InstalledApplicationList(Command):
    request_type = 'InstalledApplicationList'
    require_access = {}

    def __init__(self, uuid=None, **kwargs):
        super(InstalledApplicationList, self).__init__(uuid)
        self._attrs = {
            'ManagedAppsOnly': False
        }
        self._attrs.update(kwargs)

    @property
    def identifiers(self):
        return self._attrs['Identifiers'] if 'Identifiers' in self._attrs else None


class InstallApplication(Command):
    request_type = 'InstallApplication'
    require_access = {AccessRights.ManageApps}

    def __init__(self, uuid=None, **kwargs):
        super(InstallApplication, self).__init__(uuid)
        self._attrs = {}
        self._attrs.update(kwargs)
