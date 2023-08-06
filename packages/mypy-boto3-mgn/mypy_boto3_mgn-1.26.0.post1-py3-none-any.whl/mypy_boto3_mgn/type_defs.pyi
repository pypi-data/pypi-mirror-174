"""
Type annotations for mgn service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/type_defs/)

Usage::

    ```python
    from mypy_boto3_mgn.type_defs import CPUTypeDef

    data: CPUTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    BootModeType,
    ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    DataReplicationErrorStringType,
    DataReplicationInitiationStepNameType,
    DataReplicationInitiationStepStatusType,
    DataReplicationStateType,
    FirstBootType,
    InitiatedByType,
    JobLogEventType,
    JobStatusType,
    JobTypeType,
    LaunchDispositionType,
    LaunchStatusType,
    LifeCycleStateType,
    PostLaunchActionExecutionStatusType,
    PostLaunchActionsDeploymentTypeType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
    ReplicationTypeType,
    SsmDocumentTypeType,
    TargetInstanceTypeRightSizingMethodType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CPUTypeDef",
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    "CreateReplicationConfigurationTemplateRequestRequestTypeDef",
    "DataReplicationErrorTypeDef",
    "DataReplicationInfoReplicatedDiskTypeDef",
    "DataReplicationInitiationStepTypeDef",
    "DeleteJobRequestRequestTypeDef",
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    "DeleteSourceServerRequestRequestTypeDef",
    "DeleteVcenterClientRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeJobLogItemsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeJobsRequestFiltersTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    "ReplicationConfigurationTemplateTypeDef",
    "DescribeSourceServersRequestFiltersTypeDef",
    "DescribeVcenterClientsRequestRequestTypeDef",
    "VcenterClientTypeDef",
    "DisconnectFromServiceRequestRequestTypeDef",
    "DiskTypeDef",
    "FinalizeCutoverRequestRequestTypeDef",
    "GetLaunchConfigurationRequestRequestTypeDef",
    "GetReplicationConfigurationRequestRequestTypeDef",
    "IdentificationHintsTypeDef",
    "JobLogEventDataTypeDef",
    "LicensingTypeDef",
    "LaunchedInstanceTypeDef",
    "LifeCycleLastCutoverFinalizedTypeDef",
    "LifeCycleLastCutoverInitiatedTypeDef",
    "LifeCycleLastCutoverRevertedTypeDef",
    "LifeCycleLastTestFinalizedTypeDef",
    "LifeCycleLastTestInitiatedTypeDef",
    "LifeCycleLastTestRevertedTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "MarkAsArchivedRequestRequestTypeDef",
    "NetworkInterfaceTypeDef",
    "OSTypeDef",
    "ReplicationConfigurationReplicatedDiskTypeDef",
    "RetryDataReplicationRequestRequestTypeDef",
    "SsmParameterStoreParameterTypeDef",
    "StartCutoverRequestRequestTypeDef",
    "StartReplicationRequestRequestTypeDef",
    "StartTestRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TerminateTargetInstancesRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    "UpdateSourceServerReplicationTypeRequestRequestTypeDef",
    "ChangeServerLifeCycleStateRequestRequestTypeDef",
    "DataReplicationInitiationTypeDef",
    "DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    "DescribeJobsRequestRequestTypeDef",
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    "DescribeSourceServersRequestRequestTypeDef",
    "DescribeVcenterClientsResponseTypeDef",
    "JobLogTypeDef",
    "LifeCycleLastCutoverTypeDef",
    "LifeCycleLastTestTypeDef",
    "SourcePropertiesTypeDef",
    "ReplicationConfigurationTypeDef",
    "UpdateReplicationConfigurationRequestRequestTypeDef",
    "SsmDocumentTypeDef",
    "DataReplicationInfoTypeDef",
    "DescribeJobLogItemsResponseTypeDef",
    "LifeCycleTypeDef",
    "JobPostLaunchActionsLaunchStatusTypeDef",
    "PostLaunchActionsTypeDef",
    "SourceServerResponseMetadataTypeDef",
    "SourceServerTypeDef",
    "PostLaunchActionsStatusTypeDef",
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    "LaunchConfigurationTemplateResponseMetadataTypeDef",
    "LaunchConfigurationTemplateTypeDef",
    "LaunchConfigurationTypeDef",
    "UpdateLaunchConfigurationRequestRequestTypeDef",
    "UpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    "DescribeSourceServersResponseTypeDef",
    "ParticipatingServerTypeDef",
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    "JobTypeDef",
    "DescribeJobsResponseTypeDef",
    "StartCutoverResponseTypeDef",
    "StartTestResponseTypeDef",
    "TerminateTargetInstancesResponseTypeDef",
)

CPUTypeDef = TypedDict(
    "CPUTypeDef",
    {
        "cores": int,
        "modelName": str,
    },
    total=False,
)

ChangeServerLifeCycleStateSourceServerLifecycleTypeDef = TypedDict(
    "ChangeServerLifeCycleStateSourceServerLifecycleTypeDef",
    {
        "state": ChangeServerLifeCycleStateSourceServerLifecycleStateType,
    },
)

_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
)
_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "ebsEncryptionKeyArn": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredCreateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalCreateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass

DataReplicationErrorTypeDef = TypedDict(
    "DataReplicationErrorTypeDef",
    {
        "error": DataReplicationErrorStringType,
        "rawError": str,
    },
    total=False,
)

DataReplicationInfoReplicatedDiskTypeDef = TypedDict(
    "DataReplicationInfoReplicatedDiskTypeDef",
    {
        "backloggedStorageBytes": int,
        "deviceName": str,
        "replicatedStorageBytes": int,
        "rescannedStorageBytes": int,
        "totalStorageBytes": int,
    },
    total=False,
)

DataReplicationInitiationStepTypeDef = TypedDict(
    "DataReplicationInitiationStepTypeDef",
    {
        "name": DataReplicationInitiationStepNameType,
        "status": DataReplicationInitiationStepStatusType,
    },
    total=False,
)

DeleteJobRequestRequestTypeDef = TypedDict(
    "DeleteJobRequestRequestTypeDef",
    {
        "jobID": str,
    },
)

DeleteLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)

DeleteReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "DeleteReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)

DeleteSourceServerRequestRequestTypeDef = TypedDict(
    "DeleteSourceServerRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

DeleteVcenterClientRequestRequestTypeDef = TypedDict(
    "DeleteVcenterClientRequestRequestTypeDef",
    {
        "vcenterClientID": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestRequestTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class DescribeJobLogItemsRequestRequestTypeDef(
    _RequiredDescribeJobLogItemsRequestRequestTypeDef,
    _OptionalDescribeJobLogItemsRequestRequestTypeDef,
):
    pass

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DescribeJobsRequestFiltersTypeDef = TypedDict(
    "DescribeJobsRequestFiltersTypeDef",
    {
        "fromDate": str,
        "jobIDs": Sequence[str],
        "toDate": str,
    },
    total=False,
)

DescribeLaunchConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesRequestRequestTypeDef",
    {
        "launchConfigurationTemplateIDs": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesRequestRequestTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "replicationConfigurationTemplateIDs": Sequence[str],
    },
    total=False,
)

_RequiredReplicationConfigurationTemplateTypeDef = TypedDict(
    "_RequiredReplicationConfigurationTemplateTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalReplicationConfigurationTemplateTypeDef = TypedDict(
    "_OptionalReplicationConfigurationTemplateTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)

class ReplicationConfigurationTemplateTypeDef(
    _RequiredReplicationConfigurationTemplateTypeDef,
    _OptionalReplicationConfigurationTemplateTypeDef,
):
    pass

DescribeSourceServersRequestFiltersTypeDef = TypedDict(
    "DescribeSourceServersRequestFiltersTypeDef",
    {
        "isArchived": bool,
        "lifeCycleStates": Sequence[LifeCycleStateType],
        "replicationTypes": Sequence[ReplicationTypeType],
        "sourceServerIDs": Sequence[str],
    },
    total=False,
)

DescribeVcenterClientsRequestRequestTypeDef = TypedDict(
    "DescribeVcenterClientsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

VcenterClientTypeDef = TypedDict(
    "VcenterClientTypeDef",
    {
        "arn": str,
        "datacenterName": str,
        "hostname": str,
        "lastSeenDatetime": str,
        "sourceServerTags": Dict[str, str],
        "tags": Dict[str, str],
        "vcenterClientID": str,
        "vcenterUUID": str,
    },
    total=False,
)

DisconnectFromServiceRequestRequestTypeDef = TypedDict(
    "DisconnectFromServiceRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

DiskTypeDef = TypedDict(
    "DiskTypeDef",
    {
        "bytes": int,
        "deviceName": str,
    },
    total=False,
)

FinalizeCutoverRequestRequestTypeDef = TypedDict(
    "FinalizeCutoverRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

GetLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "GetLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

GetReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "GetReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

IdentificationHintsTypeDef = TypedDict(
    "IdentificationHintsTypeDef",
    {
        "awsInstanceID": str,
        "fqdn": str,
        "hostname": str,
        "vmPath": str,
        "vmWareUuid": str,
    },
    total=False,
)

JobLogEventDataTypeDef = TypedDict(
    "JobLogEventDataTypeDef",
    {
        "conversionServerID": str,
        "rawError": str,
        "sourceServerID": str,
        "targetInstanceID": str,
    },
    total=False,
)

LicensingTypeDef = TypedDict(
    "LicensingTypeDef",
    {
        "osByol": bool,
    },
    total=False,
)

LaunchedInstanceTypeDef = TypedDict(
    "LaunchedInstanceTypeDef",
    {
        "ec2InstanceID": str,
        "firstBoot": FirstBootType,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastCutoverFinalizedTypeDef = TypedDict(
    "LifeCycleLastCutoverFinalizedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastCutoverInitiatedTypeDef = TypedDict(
    "LifeCycleLastCutoverInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastCutoverRevertedTypeDef = TypedDict(
    "LifeCycleLastCutoverRevertedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastTestFinalizedTypeDef = TypedDict(
    "LifeCycleLastTestFinalizedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

LifeCycleLastTestInitiatedTypeDef = TypedDict(
    "LifeCycleLastTestInitiatedTypeDef",
    {
        "apiCallDateTime": str,
        "jobID": str,
    },
    total=False,
)

LifeCycleLastTestRevertedTypeDef = TypedDict(
    "LifeCycleLastTestRevertedTypeDef",
    {
        "apiCallDateTime": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

MarkAsArchivedRequestRequestTypeDef = TypedDict(
    "MarkAsArchivedRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "ips": List[str],
        "isPrimary": bool,
        "macAddress": str,
    },
    total=False,
)

OSTypeDef = TypedDict(
    "OSTypeDef",
    {
        "fullString": str,
    },
    total=False,
)

ReplicationConfigurationReplicatedDiskTypeDef = TypedDict(
    "ReplicationConfigurationReplicatedDiskTypeDef",
    {
        "deviceName": str,
        "iops": int,
        "isBootDisk": bool,
        "stagingDiskType": ReplicationConfigurationReplicatedDiskStagingDiskTypeType,
        "throughput": int,
    },
    total=False,
)

RetryDataReplicationRequestRequestTypeDef = TypedDict(
    "RetryDataReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

SsmParameterStoreParameterTypeDef = TypedDict(
    "SsmParameterStoreParameterTypeDef",
    {
        "parameterName": str,
        "parameterType": Literal["STRING"],
    },
)

_RequiredStartCutoverRequestRequestTypeDef = TypedDict(
    "_RequiredStartCutoverRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalStartCutoverRequestRequestTypeDef = TypedDict(
    "_OptionalStartCutoverRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class StartCutoverRequestRequestTypeDef(
    _RequiredStartCutoverRequestRequestTypeDef, _OptionalStartCutoverRequestRequestTypeDef
):
    pass

StartReplicationRequestRequestTypeDef = TypedDict(
    "StartReplicationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)

_RequiredStartTestRequestRequestTypeDef = TypedDict(
    "_RequiredStartTestRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalStartTestRequestRequestTypeDef = TypedDict(
    "_OptionalStartTestRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class StartTestRequestRequestTypeDef(
    _RequiredStartTestRequestRequestTypeDef, _OptionalStartTestRequestRequestTypeDef
):
    pass

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTerminateTargetInstancesRequestRequestTypeDef = TypedDict(
    "_RequiredTerminateTargetInstancesRequestRequestTypeDef",
    {
        "sourceServerIDs": Sequence[str],
    },
)
_OptionalTerminateTargetInstancesRequestRequestTypeDef = TypedDict(
    "_OptionalTerminateTargetInstancesRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class TerminateTargetInstancesRequestRequestTypeDef(
    _RequiredTerminateTargetInstancesRequestRequestTypeDef,
    _OptionalTerminateTargetInstancesRequestRequestTypeDef,
):
    pass

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "replicationConfigurationTemplateID": str,
    },
)
_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)

class UpdateReplicationConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationTemplateRequestRequestTypeDef,
):
    pass

UpdateSourceServerReplicationTypeRequestRequestTypeDef = TypedDict(
    "UpdateSourceServerReplicationTypeRequestRequestTypeDef",
    {
        "replicationType": ReplicationTypeType,
        "sourceServerID": str,
    },
)

ChangeServerLifeCycleStateRequestRequestTypeDef = TypedDict(
    "ChangeServerLifeCycleStateRequestRequestTypeDef",
    {
        "lifeCycle": ChangeServerLifeCycleStateSourceServerLifecycleTypeDef,
        "sourceServerID": str,
    },
)

DataReplicationInitiationTypeDef = TypedDict(
    "DataReplicationInitiationTypeDef",
    {
        "nextAttemptDateTime": str,
        "startDateTime": str,
        "steps": List[DataReplicationInitiationStepTypeDef],
    },
    total=False,
)

_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "jobID": str,
    },
)
_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef = TypedDict(
    "_OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class DescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef(
    _RequiredDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
    _OptionalDescribeJobLogItemsRequestDescribeJobLogItemsPaginateTypeDef,
):
    pass

DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesRequestDescribeLaunchConfigurationTemplatesPaginateTypeDef",
    {
        "launchConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesRequestDescribeReplicationConfigurationTemplatesPaginateTypeDef",
    {
        "replicationConfigurationTemplateIDs": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef = TypedDict(
    "DescribeVcenterClientsRequestDescribeVcenterClientsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplicationConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "ReplicationConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "replicationConfigurationTemplateID": str,
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "tags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeJobsRequestDescribeJobsPaginateTypeDef = TypedDict(
    "DescribeJobsRequestDescribeJobsPaginateTypeDef",
    {
        "filters": DescribeJobsRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeJobsRequestRequestTypeDef = TypedDict(
    "DescribeJobsRequestRequestTypeDef",
    {
        "filters": DescribeJobsRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeReplicationConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeReplicationConfigurationTemplatesResponseTypeDef",
    {
        "items": List[ReplicationConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef = TypedDict(
    "DescribeSourceServersRequestDescribeSourceServersPaginateTypeDef",
    {
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSourceServersRequestRequestTypeDef = TypedDict(
    "DescribeSourceServersRequestRequestTypeDef",
    {
        "filters": DescribeSourceServersRequestFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

DescribeVcenterClientsResponseTypeDef = TypedDict(
    "DescribeVcenterClientsResponseTypeDef",
    {
        "items": List[VcenterClientTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobLogTypeDef = TypedDict(
    "JobLogTypeDef",
    {
        "event": JobLogEventType,
        "eventData": JobLogEventDataTypeDef,
        "logDateTime": str,
    },
    total=False,
)

LifeCycleLastCutoverTypeDef = TypedDict(
    "LifeCycleLastCutoverTypeDef",
    {
        "finalized": LifeCycleLastCutoverFinalizedTypeDef,
        "initiated": LifeCycleLastCutoverInitiatedTypeDef,
        "reverted": LifeCycleLastCutoverRevertedTypeDef,
    },
    total=False,
)

LifeCycleLastTestTypeDef = TypedDict(
    "LifeCycleLastTestTypeDef",
    {
        "finalized": LifeCycleLastTestFinalizedTypeDef,
        "initiated": LifeCycleLastTestInitiatedTypeDef,
        "reverted": LifeCycleLastTestRevertedTypeDef,
    },
    total=False,
)

SourcePropertiesTypeDef = TypedDict(
    "SourcePropertiesTypeDef",
    {
        "cpus": List[CPUTypeDef],
        "disks": List[DiskTypeDef],
        "identificationHints": IdentificationHintsTypeDef,
        "lastUpdatedDateTime": str,
        "networkInterfaces": List[NetworkInterfaceTypeDef],
        "os": OSTypeDef,
        "ramBytes": int,
        "recommendedInstanceType": str,
    },
    total=False,
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "replicatedDisks": List[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": List[str],
        "sourceServerID": str,
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Dict[str, str],
        "useDedicatedReplicationServer": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateReplicationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateReplicationConfigurationRequestRequestTypeDef",
    {
        "associateDefaultSecurityGroup": bool,
        "bandwidthThrottling": int,
        "createPublicIP": bool,
        "dataPlaneRouting": ReplicationConfigurationDataPlaneRoutingType,
        "defaultLargeStagingDiskType": ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        "ebsEncryption": ReplicationConfigurationEbsEncryptionType,
        "ebsEncryptionKeyArn": str,
        "name": str,
        "replicatedDisks": Sequence[ReplicationConfigurationReplicatedDiskTypeDef],
        "replicationServerInstanceType": str,
        "replicationServersSecurityGroupsIDs": Sequence[str],
        "stagingAreaSubnetId": str,
        "stagingAreaTags": Mapping[str, str],
        "useDedicatedReplicationServer": bool,
    },
    total=False,
)

class UpdateReplicationConfigurationRequestRequestTypeDef(
    _RequiredUpdateReplicationConfigurationRequestRequestTypeDef,
    _OptionalUpdateReplicationConfigurationRequestRequestTypeDef,
):
    pass

_RequiredSsmDocumentTypeDef = TypedDict(
    "_RequiredSsmDocumentTypeDef",
    {
        "actionName": str,
        "ssmDocumentName": str,
    },
)
_OptionalSsmDocumentTypeDef = TypedDict(
    "_OptionalSsmDocumentTypeDef",
    {
        "mustSucceedForCutover": bool,
        "parameters": Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]],
        "timeoutSeconds": int,
    },
    total=False,
)

class SsmDocumentTypeDef(_RequiredSsmDocumentTypeDef, _OptionalSsmDocumentTypeDef):
    pass

DataReplicationInfoTypeDef = TypedDict(
    "DataReplicationInfoTypeDef",
    {
        "dataReplicationError": DataReplicationErrorTypeDef,
        "dataReplicationInitiation": DataReplicationInitiationTypeDef,
        "dataReplicationState": DataReplicationStateType,
        "etaDateTime": str,
        "lagDuration": str,
        "lastSnapshotDateTime": str,
        "replicatedDisks": List[DataReplicationInfoReplicatedDiskTypeDef],
    },
    total=False,
)

DescribeJobLogItemsResponseTypeDef = TypedDict(
    "DescribeJobLogItemsResponseTypeDef",
    {
        "items": List[JobLogTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifeCycleTypeDef = TypedDict(
    "LifeCycleTypeDef",
    {
        "addedToServiceDateTime": str,
        "elapsedReplicationDuration": str,
        "firstByteDateTime": str,
        "lastCutover": LifeCycleLastCutoverTypeDef,
        "lastSeenByServiceDateTime": str,
        "lastTest": LifeCycleLastTestTypeDef,
        "state": LifeCycleStateType,
    },
    total=False,
)

JobPostLaunchActionsLaunchStatusTypeDef = TypedDict(
    "JobPostLaunchActionsLaunchStatusTypeDef",
    {
        "executionID": str,
        "executionStatus": PostLaunchActionExecutionStatusType,
        "failureReason": str,
        "ssmDocument": SsmDocumentTypeDef,
        "ssmDocumentType": SsmDocumentTypeType,
    },
    total=False,
)

PostLaunchActionsTypeDef = TypedDict(
    "PostLaunchActionsTypeDef",
    {
        "cloudWatchLogGroupName": str,
        "deployment": PostLaunchActionsDeploymentTypeType,
        "s3LogBucket": str,
        "s3OutputKeyPrefix": str,
        "ssmDocuments": Sequence[SsmDocumentTypeDef],
    },
    total=False,
)

SourceServerResponseMetadataTypeDef = TypedDict(
    "SourceServerResponseMetadataTypeDef",
    {
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "isArchived": bool,
        "launchedInstance": LaunchedInstanceTypeDef,
        "lifeCycle": LifeCycleTypeDef,
        "replicationType": ReplicationTypeType,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
        "vcenterClientID": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SourceServerTypeDef = TypedDict(
    "SourceServerTypeDef",
    {
        "arn": str,
        "dataReplicationInfo": DataReplicationInfoTypeDef,
        "isArchived": bool,
        "launchedInstance": LaunchedInstanceTypeDef,
        "lifeCycle": LifeCycleTypeDef,
        "replicationType": ReplicationTypeType,
        "sourceProperties": SourcePropertiesTypeDef,
        "sourceServerID": str,
        "tags": Dict[str, str],
        "vcenterClientID": str,
    },
    total=False,
)

PostLaunchActionsStatusTypeDef = TypedDict(
    "PostLaunchActionsStatusTypeDef",
    {
        "postLaunchActionsLaunchStatusList": List[JobPostLaunchActionsLaunchStatusTypeDef],
        "ssmAgentDiscoveryDatetime": str,
    },
    total=False,
)

CreateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "CreateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "postLaunchActions": PostLaunchActionsTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

LaunchConfigurationTemplateResponseMetadataTypeDef = TypedDict(
    "LaunchConfigurationTemplateResponseMetadataTypeDef",
    {
        "arn": str,
        "launchConfigurationTemplateID": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredLaunchConfigurationTemplateTypeDef = TypedDict(
    "_RequiredLaunchConfigurationTemplateTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalLaunchConfigurationTemplateTypeDef = TypedDict(
    "_OptionalLaunchConfigurationTemplateTypeDef",
    {
        "arn": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "tags": Dict[str, str],
    },
    total=False,
)

class LaunchConfigurationTemplateTypeDef(
    _RequiredLaunchConfigurationTemplateTypeDef, _OptionalLaunchConfigurationTemplateTypeDef
):
    pass

LaunchConfigurationTypeDef = TypedDict(
    "LaunchConfigurationTypeDef",
    {
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "ec2LaunchTemplateID": str,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "name": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "sourceServerID": str,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalUpdateLaunchConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationRequestRequestTypeDef",
    {
        "bootMode": BootModeType,
        "copyPrivateIp": bool,
        "copyTags": bool,
        "launchDisposition": LaunchDispositionType,
        "licensing": LicensingTypeDef,
        "name": str,
        "postLaunchActions": PostLaunchActionsTypeDef,
        "targetInstanceTypeRightSizingMethod": TargetInstanceTypeRightSizingMethodType,
    },
    total=False,
)

class UpdateLaunchConfigurationRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationRequestRequestTypeDef,
):
    pass

_RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "launchConfigurationTemplateID": str,
    },
)
_OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef",
    {
        "postLaunchActions": PostLaunchActionsTypeDef,
    },
    total=False,
)

class UpdateLaunchConfigurationTemplateRequestRequestTypeDef(
    _RequiredUpdateLaunchConfigurationTemplateRequestRequestTypeDef,
    _OptionalUpdateLaunchConfigurationTemplateRequestRequestTypeDef,
):
    pass

DescribeSourceServersResponseTypeDef = TypedDict(
    "DescribeSourceServersResponseTypeDef",
    {
        "items": List[SourceServerTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredParticipatingServerTypeDef = TypedDict(
    "_RequiredParticipatingServerTypeDef",
    {
        "sourceServerID": str,
    },
)
_OptionalParticipatingServerTypeDef = TypedDict(
    "_OptionalParticipatingServerTypeDef",
    {
        "launchStatus": LaunchStatusType,
        "launchedEc2InstanceID": str,
        "postLaunchActionsStatus": PostLaunchActionsStatusTypeDef,
    },
    total=False,
)

class ParticipatingServerTypeDef(
    _RequiredParticipatingServerTypeDef, _OptionalParticipatingServerTypeDef
):
    pass

DescribeLaunchConfigurationTemplatesResponseTypeDef = TypedDict(
    "DescribeLaunchConfigurationTemplatesResponseTypeDef",
    {
        "items": List[LaunchConfigurationTemplateTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredJobTypeDef = TypedDict(
    "_RequiredJobTypeDef",
    {
        "jobID": str,
    },
)
_OptionalJobTypeDef = TypedDict(
    "_OptionalJobTypeDef",
    {
        "arn": str,
        "creationDateTime": str,
        "endDateTime": str,
        "initiatedBy": InitiatedByType,
        "participatingServers": List[ParticipatingServerTypeDef],
        "status": JobStatusType,
        "tags": Dict[str, str],
        "type": JobTypeType,
    },
    total=False,
)

class JobTypeDef(_RequiredJobTypeDef, _OptionalJobTypeDef):
    pass

DescribeJobsResponseTypeDef = TypedDict(
    "DescribeJobsResponseTypeDef",
    {
        "items": List[JobTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartCutoverResponseTypeDef = TypedDict(
    "StartCutoverResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTestResponseTypeDef = TypedDict(
    "StartTestResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TerminateTargetInstancesResponseTypeDef = TypedDict(
    "TerminateTargetInstancesResponseTypeDef",
    {
        "job": JobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
