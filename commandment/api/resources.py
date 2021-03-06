"""
    This module defines resources, as required by the Flask-REST-JSONAPI package. This represents most of the REST API.
"""

from .schema import DeviceSchema, CertificateSchema, PrivateKeySchema, \
    CertificateSigningRequestSchema, OrganizationSchema, CommandSchema, InstalledApplicationSchema, ProfileSchema, \
    InstalledCertificateSchema, DeviceGroupSchema, InstalledProfileSchema, TagSchema, AvailableOSUpdateSchema
from commandment.models import db, Device, Certificate, CertificateSigningRequest, CACertificate, PushCertificate, \
    SSLCertificate, Organization, Command, InstalledApplication, InstalledProfile, InstalledCertificate, DeviceGroup, \
    Tag, AvailableOSUpdate
from commandment.profiles.models import Profile

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship


class DeviceList(ResourceList):
    schema = DeviceSchema
    data_layer = {'session': db.session, 'model': Device}


class DeviceDetail(ResourceDetail):
    schema = DeviceSchema
    data_layer = {
        'session': db.session,
        'model': Device,
        'url_field': 'device_id'
    }


class DeviceGroupList(ResourceList):
    schema = DeviceGroupSchema
    data_layer = {'session': db.session, 'model': DeviceGroup}


class DeviceGroupDetail(ResourceDetail):
    schema = DeviceGroupSchema
    data_layer = {
        'session': db.session,
        'model': DeviceGroup,
        'url_field': 'device_group_id'
    }


class DeviceRelationship(ResourceRelationship):
    schema = DeviceSchema
    data_layer = {
        'session': db.session,
        'model': Device,
        'url_field': 'device_id'
    }


class CertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateTypeDetail(ResourceDetail):
    schema = CertificateSchema
    data_layer = {'session': db.session, 'model': Certificate}


class PrivateKeyDetail(ResourceDetail):
    schema = PrivateKeySchema
    data_layer = {'session': db.session, 'model': Certificate}


class CertificateSigningRequestList(ResourceList):
    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db.session,
        'model': CertificateSigningRequest,
    }


class CertificateSigningRequestDetail(ResourceDetail):
    schema = CertificateSigningRequestSchema
    data_layer = {
        'session': db.session,
        'model': CertificateSigningRequest
    }


class PushCertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': PushCertificate
    }


class CACertificateList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': CACertificate
    }


class SSLCertificatesList(ResourceList):
    schema = CertificateSchema
    data_layer = {
        'session': db.session,
        'model': SSLCertificate
    }


class OrganizationList(ResourceList):
    schema = OrganizationSchema
    data_layer = {
        'session': db.session,
        'model': Organization
    }


class OrganizationDetail(ResourceDetail):
    schema = OrganizationSchema
    data_layer = {
        'session': db.session,
        'model': Organization
    }


class CommandsList(ResourceList):
    schema = CommandSchema
    data_layer = {
        'session': db.session,
        'model': Command,
    }


class CommandDetail(ResourceDetail):
    schema = CommandSchema
    data_layer = {
        'session': db.session,
        'model': Command,
        'url_field': 'command_id'
    }


class CommandRelationship(ResourceRelationship):
    schema = CommandSchema
    data_layer = {'session': db.session, 'model': Command}


class InstalledApplicationsList(ResourceList):
    schema = InstalledApplicationSchema
    data_layer = {
        'session': db.session,
        'model': InstalledApplication
    }


class InstalledApplicationDetail(ResourceDetail):
    schema = InstalledApplicationSchema
    data_layer = {
        'session': db.session,
        'model': InstalledApplication
    }


class InstalledCertificatesList(ResourceList):
    schema = InstalledCertificateSchema
    data_layer = {
        'session': db.session,
        'model': InstalledCertificate
    }


class InstalledCertificateDetail(ResourceDetail):
    schema = InstalledCertificateSchema
    data_layer = {
        'session': db.session,
        'model': InstalledCertificate,
        'url_field': 'installed_certificate_id'
    }


# class PayloadsList(ResourceList):
#     schema = PayloadSchema
#     data_layer = {
#         'session': db.session,
#         'model': Payload
#     }
#
#
# class PayloadDetail(ResourceDetail):
#     schema = PayloadSchema
#     data_layer = {
#         'session': db.session,
#         'model': Payload
#     }


class ProfilesList(ResourceList):
    schema = ProfileSchema
    data_layer = {
        'session': db.session,
        'model': Profile
    }


class ProfileDetail(ResourceDetail):
    schema = ProfileSchema
    data_layer = {
        'session': db.session,
        'model': Profile,
        'url_field': 'profile_id'
    }


class ProfileRelationship(ResourceRelationship):
    schema = ProfileSchema
    data_layer = {
        'session': db.session,
        'model': Profile,
        'url_field': 'profile_id'
    }


class InstalledProfilesList(ResourceList):
    schema = InstalledProfileSchema
    data_layer = {
        'session': db.session,
        'model': InstalledProfile
    }


class InstalledProfileDetail(ResourceDetail):
    schema = InstalledProfileSchema
    data_layer = {
        'session': db.session,
        'model': InstalledProfile
    }


class TagsList(ResourceList):
    schema = TagSchema
    data_layer = {
        'session': db.session,
        'model': Tag
    }
    view_kwargs = True


class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {
        'session': db.session,
        'model': Tag,
        'url_field': 'tag_id'
    }


class TagRelationship(ResourceRelationship):
    schema = TagSchema
    data_layer = {
        'session': db.session,
        'model': Tag,
        'url_field': 'tag_id'
    }


class AvailableOSUpdateList(ResourceList):
    schema = AvailableOSUpdateSchema
    data_layer = {
        'session': db.session,
        'model': AvailableOSUpdate
    }


class AvailableOSUpdateDetail(ResourceDetail):
    schema = AvailableOSUpdateSchema
    data_layer = {
        'session': db.session,
        'model': AvailableOSUpdate,
        'url_field': 'available_os_update_id'
    }
