"""
Google Cloud Platform compute buckets state module.

Copyright (c) 2022 VMware, Inc. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

"""

__contracts__ = ["resource"]

from dataclasses import field
from dataclasses import make_dataclass
from typing import Dict, Any, List
import copy


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    source_instance_template: str = None,
    source_machine_image: str = None,
    request_id: str = None,
    zone: str = None,
    project: str = None,
    advanced_machine_features: Dict = None,
    can_ip_forward: bool = False,
    confidential_instance_config: Dict = None,
    deletion_protection: bool = False,
    description: str = None,
    disks: List[
        make_dataclass(
            "AttachedDisk",
            [
                ("disk_encryption_key", {}, field(default=None)),
                ("index", int, field(default=None)),
                ("kind", str, field(default="compute#attachedDisk")),
                ("source", str, field(default=None)),
                ("boot", bool, field(default=None)),
                ("interface", str, field(default=None)),
                ("disk_size_gb", str, field(default=None)),
                ("initialize_params", {}, field(default=None)),
                ("force_attach", bool, field(default=None)),
                ("mode", str, field(default=None)),
                ("auto_delete", bool, field(default=None)),
                ("architecture", str, field(default=None)),
                ("licenses", List[str], field(default=None)),
                ("device_name", str, field(default=None)),
                (
                    "guest_os_features",
                    List[
                        make_dataclass(
                            "GuestOsFeature", [("type", str, field(default=None))]
                        )
                    ],
                    field(default=None),
                ),
                ("type", str, field(default=None)),
                ("shielded_instance_initial_state", {}, field(default=None)),
            ],
        )
    ] = None,
    display_device: Dict = None,
    fingerprint: str = None,
    guest_accelerators: List[
        make_dataclass(
            "AcceleratorConfig",
            [
                ("accelerator_type", str, field(default=None)),
                ("accelerator_count", int, field(default=None)),
            ],
        )
    ] = None,
    hostname: str = None,
    key_revocation_action_type: str = None,
    label_fingerprint: str = None,
    labels: Dict[
        str,
        make_dataclass("Labels", [("additional_properties", str, field(default=None))]),
    ] = None,
    machine_type: str = None,
    metadata: Dict = None,
    min_cpu_platform: str = None,
    network_interfaces: List[
        make_dataclass(
            "NetworkInterface",
            [
                (
                    "ipv6_access_configs",
                    List[
                        make_dataclass(
                            "AccessConfig",
                            [
                                ("name", str, field(default=None)),
                                ("type", str, field(default="ONE_TO_ONE_NAT")),
                                ("public_ptr_domain_name", str, field(default=None)),
                                ("external_ipv6", str, field(default=None)),
                                ("kind", str, field(default="compute#accessConfig")),
                                ("nat_ip", str, field(default=None)),
                                (
                                    "external_ipv6_prefix_length",
                                    int,
                                    field(default=None),
                                ),
                                ("network_tier", str, field(default=None)),
                                ("set_public_ptr", bool, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("network_ip", str, field(default=None)),
                ("internal_ipv6_prefix_length", int, field(default=None)),
                ("ipv6_access_type", str, field(default=None)),
                ("network", str, field(default=None)),
                ("nic_type", str, field(default=None)),
                ("stack_type", str, field(default=None)),
                ("queue_count", int, field(default=None)),
                ("ipv6_address", str, field(default=None)),
                ("kind", str, field(default="compute#networkInterface")),
                ("fingerprint", str, field(default=None)),
                (
                    "alias_ip_ranges",
                    List[
                        make_dataclass(
                            "AliasIpRange",
                            [
                                ("ip_cidr_range", str, field(default=None)),
                                ("subnetwork_range_name", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("subnetwork", str, field(default=None)),
                ("name", str, field(default=None)),
                (
                    "access_configs",
                    List[
                        make_dataclass(
                            "AccessConfig",
                            [
                                ("name", str, field(default=None)),
                                ("type", str, field(default="ONE_TO_ONE_NAT")),
                                ("public_ptr_domain_name", str, field(default=None)),
                                ("external_ipv6", str, field(default=None)),
                                ("kind", str, field(default="compute#accessConfig")),
                                ("nat_ip", str, field(default=None)),
                                (
                                    "external_ipv6_prefix_length",
                                    int,
                                    field(default=None),
                                ),
                                ("network_tier", str, field(default=None)),
                                ("set_public_ptr", bool, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
            ],
        )
    ] = None,
    network_performance_config: Dict = None,
    params: Dict = None,
    private_ipv6_google_access: str = None,
    reservation_affinity: Dict = None,
    resource_policies: List = None,
    scheduling: Dict = None,
    service_accounts: List[
        make_dataclass(
            "ServiceAccount",
            [
                ("email", str, field(default=None)),
                ("scopes", List[str], field(default=None)),
            ],
        )
    ] = None,
    shielded_instance_config: Dict = None,
    shielded_instance_integrity_policy: Dict = None,
    source_machine_image_encryption_key: Dict = None,
    status: str = None,
    tags: Dict = None,
) -> Dict[str, Any]:
    r"""

    Creates an instance resource in the specified project using the data included in the request.
        or
    Updates an instance only if the necessary resources are available. This method can update only a specific set of instance properties. See Updating a running instance for a list of updatable instance properties.

    Args:
        name(str, optional): The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Defaults to None.
        resource_id(str, optional): . Defaults to None.
        source_instance_template(str, optional): Specifies instance template to create the instance. This field is optional. It can be a full or partial URL. For example, the following are all valid URLs to an instance template: - https://www.googleapis.com/compute/v1/projects/project /global/instanceTemplates/instanceTemplate - projects/project/global/instanceTemplates/instanceTemplate - global/instanceTemplates/instanceTemplate . Defaults to None.
        source_machine_image(str, optional): Source machine image. Defaults to None.
        zone(str): The name of the zone for this request.
        project(str): Project ID for this request.
        request_id(str, optional): An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.
        params(Dict[str, Any], optional): Input only. [Input Only] Additional params passed with the request, but not persisted as part of resource payload. Defaults to None.
        resource_policies(list[str], optional): Resource policies applied to this instance. Defaults to None.
        description(str, optional): An optional description of this resource. Provide this property when you create the resource. Defaults to None.
        creation_timestamp(str, optional): [Output Only] Creation timestamp in RFC3339 text format. Defaults to None.
        source_machine_image_encryption_key(Dict[str, Any], optional): Source machine image encryption key when creating an instance from a machine image. Defaults to None.
        min_cpu_platform(str, optional): Specifies a minimum CPU platform for the VM instance. Applicable values are the friendly names of CPU platforms, such as minCpuPlatform: "Intel Haswell" or minCpuPlatform: "Intel Sandy Bridge". Defaults to None.
        id_(str, optional): [Output Only] The unique identifier for the resource. This identifier is defined by the server. Defaults to None.
        status_message(str, optional): [Output Only] An optional, human-readable explanation of the status. Defaults to None.
        confidential_instance_config(Dict[str, Any], optional): None. Defaults to None.
        labels(Dict[str, Any], optional): Labels to apply to this instance. These can be later modified by the setLabels method. Defaults to None.
            * additionalProperties (str, optional): None
        reservation_affinity(Dict[str, Any], optional): Specifies the reservations that this instance can consume from. Defaults to None.
        last_start_timestamp(str, optional): [Output Only] Last start timestamp in RFC3339 text format. Defaults to None.
        machine_type(str, optional): Full or partial URL of the machine type resource to use for this instance, in the format: zones/zone/machineTypes/machine-type. This is provided by the client when the instance is created. For example, the following is a valid partial url to a predefined machine type: zones/us-central1-f/machineTypes/n1-standard-1 To create a custom machine type, provide a URL to a machine type in the following format, where CPUS is 1 or an even number up to 32 (2, 4, 6, ... 24, etc), and MEMORY is the total memory for this instance. Memory must be a multiple of 256 MB and must be supplied in MB (e.g. 5 GB of memory is 5120 MB): zones/zone/machineTypes/custom-CPUS-MEMORY For example: zones/us-central1-f/machineTypes/custom-4-5120 For a full list of restrictions, read the Specifications for custom machine types. Defaults to None.
        last_suspended_timestamp(str, optional): [Output Only] Last suspended timestamp in RFC3339 text format. Defaults to None.
        start_restricted(bool, optional): [Output Only] Whether a VM has been restricted for start because Compute Engine has detected suspicious activity. Defaults to None.
        label_fingerprint(str, optional): A fingerprint for this request, which is essentially a hash of the label's contents and used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash in order to update or change labels. To see the latest fingerprint, make get() request to the instance. Defaults to None.
        kind(str, optional): [Output Only] Type of the resource. Always compute#instance for instances. Defaults to "compute#instance".
        shielded_instance_integrity_policy(Dict[str, Any], optional): None. Defaults to None.
        display_device(Dict[str, Any], optional): Enables display device for the instance. Defaults to None.
        deletion_protection(bool, optional): Whether the resource should be protected against deletion. Defaults to None.
        guest_accelerators(list[Dict[str, Any]], optional): A list of the type and count of accelerator cards attached to the instance. Defaults to None.
            * properties (Dict[str, Any], optional): A specification of the type and number of accelerator cards attached to the instance.
                * acceleratorCount (int, optional): The number of the guest accelerator cards exposed to this instance.
                * acceleratorType (str, optional): Full or partial URL of the accelerator type resource to attach to this instance. For example: projects/my-project/zones/us-central1-c/acceleratorTypes/nvidia-tesla-p100 If you are creating an instance template, specify only the accelerator name. See GPUs on Compute Engine for a full list of accelerator types.
        metadata(Dict[str, Any], optional): The metadata key/value pairs assigned to this instance. This includes custom metadata and predefined keys. Defaults to None.
        scheduling(Dict[str, Any], optional): Sets the scheduling options for this instance. Defaults to None.
        shielded_instance_config(Dict[str, Any], optional): None. Defaults to None.
        hostname(str, optional): Specifies the hostname of the instance. The specified hostname must be RFC1035 compliant. If hostname is not specified, the default hostname is [INSTANCE_NAME].c.[PROJECT_ID].internal when using the global DNS, and [INSTANCE_NAME].[ZONE].c.[PROJECT_ID].internal when using zonal DNS. Defaults to None.
        self_link(str, optional): [Output Only] Server-defined URL for this resource. Defaults to None.
        tags(Dict[str, Any], optional): Tags to apply to this instance. Tags are used to identify valid sources or targets for network firewalls and are specified by the client during instance creation. The tags can be later modified by the setTags method. Each tag within the list must comply with RFC1035. Multiple tags can be specified via the 'tags.items' field. Defaults to None.
        service_accounts(list[Dict[str, Any]], optional): A list of service accounts, with their specified scopes, authorized for this instance. Only one service account per VM instance is supported. Service accounts generate access tokens that can be accessed through the metadata server and used to authenticate applications on the instance. See Service Accounts for more information. Defaults to None.
            * properties (Dict[str, Any], optional): A service account.
                * email (str, optional): Email address of the service account.
                * scopes (list[str], optional): The list of scopes to be made available for this service account.
        cpu_platform(str, optional): [Output Only] The CPU platform used by this instance. Defaults to None.
        resource_status(Dict[str, Any], optional): [Output Only] Specifies values set for instance attributes as compared to the values requested by user in the corresponding input only field. Defaults to None.
        last_stop_timestamp(str, optional): [Output Only] Last stop timestamp in RFC3339 text format. Defaults to None.
        status(str, optional): [Output Only] The status of the instance. One of the following values: PROVISIONING, STAGING, RUNNING, STOPPING, SUSPENDING, SUSPENDED, REPAIRING, and TERMINATED. For more information about the status of the instance, see Instance life cycle. Defaults to None.
        fingerprint(str, optional): Specifies a fingerprint for this resource, which is essentially a hash of the instance's contents and used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update the instance. You must always provide an up-to-date fingerprint hash in order to update the instance. To see the latest fingerprint, make get() request to the instance. Defaults to None.
        network_performance_config(Dict[str, Any], optional): None. Defaults to None.
        can_ip_forward(bool, optional): Allows this instance to send and receive packets with non-matching destination or source IPs. This is required if you plan to use this instance to forward routes. For more information, see Enabling IP Forwarding . Defaults to None.
        disks(list[Dict[str, Any]], optional): Array of disks associated with this instance. Persistent disks must be created before you can assign them. Defaults to None.
            * properties (Dict[str, Any], optional): An instance-attached disk resource.
                * boot (bool, optional): Indicates that this is a boot disk. The virtual machine will use the first partition of the disk for its root filesystem.
                * licenses (list[str], optional): [Output Only] Any valid publicly visible licenses.
                * type (str, optional): Specifies the type of the disk, either SCRATCH or PERSISTENT. If not specified, the default is PERSISTENT.
                * initializeParams (Dict[str, Any], optional): [Input Only] Specifies the parameters for a new disk that will be created alongside the new instance. Use initialization parameters to create boot disks or local SSDs attached to the new instance. This property is mutually exclusive with the source property; you can only define one or the other, but not both.
                * guestOsFeatures (list[Dict[str, Any]], optional): A list of features to enable on the guest operating system. Applicable only for bootable images. Read Enabling guest operating system features to see a list of available options.
                    * properties (Dict[str, Any], optional): Guest OS features.
                        * type (str, optional): The ID of a supported feature. To add multiple values, use commas to separate values. Set to one or more of the following values: - VIRTIO_SCSI_MULTIQUEUE - WINDOWS - MULTI_IP_SUBNET - UEFI_COMPATIBLE - GVNIC - SEV_CAPABLE - SUSPEND_RESUME_COMPATIBLE - SEV_SNP_CAPABLE For more information, see Enabling guest operating system features.
                * diskEncryptionKey (Dict[str, Any], optional): Encrypts or decrypts a disk using a customer-supplied encryption key. If you are creating a new disk, this field encrypts the new disk using an encryption key that you provide. If you are attaching an existing disk that is already encrypted, this field decrypts the disk using the customer-supplied encryption key. If you encrypt a disk using a customer-supplied key, you must provide the same key again when you attempt to use this resource at a later time. For example, you must provide the key when you create a snapshot or an image from the disk or when you attach the disk to a virtual machine instance. If you do not provide an encryption key, then the disk will be encrypted using an automatically generated key and you do not need to provide a key to use the disk later. Instance templates do not store customer-supplied encryption keys, so you cannot use your own keys to encrypt disks in a managed instance group.
                * deviceName (str, optional): Specifies a unique device name of your choice that is reflected into the /dev/disk/by-id/google-* tree of a Linux operating system running within the instance. This name can be used to reference the device for mounting, resizing, and so on, from within the instance. If not specified, the server chooses a default device name to apply to this disk, in the form persistent-disk-x, where x is a number assigned by Google Compute Engine. This field is only applicable for persistent disks.
                * mode (str, optional): The mode in which to attach this disk, either READ_WRITE or READ_ONLY. If not specified, the default is to attach the disk in READ_WRITE mode.
                * interface (str, optional): Specifies the disk interface to use for attaching this disk, which is either SCSI or NVME. For most machine types, the default is SCSI. Local SSDs can use either NVME or SCSI. In certain configurations, persistent disks can use NVMe. For more information, see About persistent disks.
                * shieldedInstanceInitialState (Dict[str, Any], optional): [Output Only] shielded vm initial state stored on disk
                * source (str, optional): Specifies a valid partial or full URL to an existing Persistent Disk resource. When creating a new instance, one of initializeParams.sourceImage or initializeParams.sourceSnapshot or disks.source is required except for local SSD. If desired, you can also attach existing non-root persistent disks using this property. This field is only applicable for persistent disks. Note that for InstanceTemplate, specify the disk name for zonal disk, and the URL for regional disk.
                * forceAttach (bool, optional): [Input Only] Whether to force attach the regional disk even if it's currently attached to another instance. If you try to force attach a zonal disk to an instance, you will receive an error.
                * diskSizeGb (str, optional): The size of the disk in GB.
                * index (int, optional): [Output Only] A zero-based index to this disk, where 0 is reserved for the boot disk. If you have many disks attached to an instance, each disk would have a unique index number.
                * architecture (str, optional): [Output Only] The architecture of the attached disk. Valid values are ARM64 or X86_64.
                * autoDelete (bool, optional): Specifies whether the disk will be auto-deleted when the instance is deleted (but not when the disk is detached from the instance).
                * kind (str, optional): [Output Only] Type of the resource. Always compute#attachedDisk for attached disks.
        network_interfaces(list[Dict[str, Any]], optional): An array of network configurations for this instance. These specify how interfaces are configured to interact with other network services, such as connecting to the internet. Multiple interfaces are supported per instance. Defaults to None.
            * properties (Dict[str, Any], optional): A network interface resource attached to an instance.
                * ipv6AccessType (str, optional): [Output Only] One of EXTERNAL, INTERNAL to indicate whether the IP can be accessed from the Internet. This field is always inherited from its subnetwork. Valid only if stackType is IPV4_IPV6.
                * accessConfigs (list[Dict[str, Any]], optional): An array of configurations for this interface. Currently, only one access config, ONE_TO_ONE_NAT, is supported. If there are no accessConfigs specified, then this instance will have no external internet access.
                    * properties (Dict[str, Any], optional): An access configuration attached to an instance's network interface. Only one access config per instance is supported.
                        * kind (str, optional): [Output Only] Type of the resource. Always compute#accessConfig for access configs.
                        * natIP (str, optional): An external IP address associated with this instance. Specify an unused static external IP address available to the project or leave this field undefined to use an IP from a shared ephemeral IP address pool. If you specify a static external IP address, it must live in the same region as the zone of the instance.
                        * externalIpv6 (str, optional): The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig. The field is output only, an IPv6 address from a subnetwork associated with the instance will be allocated dynamically.
                        * networkTier (str, optional): This signifies the networking tier used for configuring this access configuration and can only take the following values: PREMIUM, STANDARD. If an AccessConfig is specified without a valid external IP address, an ephemeral IP will be created with this networkTier. If an AccessConfig with a valid external IP address is specified, it must match that of the networkTier associated with the Address resource owning that IP.
                        * name (str, optional): The name of this access configuration. The default and recommended name is External NAT, but you can use any arbitrary string, such as My external IP or Network Access.
                        * externalIpv6PrefixLength (int, optional): The prefix length of the external IPv6 range.
                        * setPublicPtr (bool, optional): Specifies whether a public DNS 'PTR' record should be created to map the external IP address of the instance to a DNS domain name. This field is not used in ipv6AccessConfig. A default PTR record will be created if the VM has external IPv6 range associated.
                        * publicPtrDomainName (str, optional): The DNS domain name for the public PTR record. You can set this field only if the `setPublicPtr` field is enabled in accessConfig. If this field is unspecified in ipv6AccessConfig, a default PTR record will be createc for first IP in associated external IPv6 range.
                        * type (str, optional): The type of configuration. The default and only option is ONE_TO_ONE_NAT.
                * name (str, optional): [Output Only] The name of the network interface, which is generated by the server. For a VM, the network interface uses the nicN naming format. Where N is a value between 0 and 7. The default interface value is nic0.
                * ipv6Address (str, optional): An IPv6 internal network address for this network interface.
                * ipv6AccessConfigs (list[Dict[str, Any]], optional): An array of IPv6 access configurations for this interface. Currently, only one IPv6 access config, DIRECT_IPV6, is supported. If there is no ipv6AccessConfig specified, then this instance will have no external IPv6 Internet access.
                    * properties (Dict[str, Any], optional): An access configuration attached to an instance's network interface. Only one access config per instance is supported.
                        * kind (str, optional): [Output Only] Type of the resource. Always compute#accessConfig for access configs.
                        * natIP (str, optional): An external IP address associated with this instance. Specify an unused static external IP address available to the project or leave this field undefined to use an IP from a shared ephemeral IP address pool. If you specify a static external IP address, it must live in the same region as the zone of the instance.
                        * externalIpv6 (str, optional): The first IPv6 address of the external IPv6 range associated with this instance, prefix length is stored in externalIpv6PrefixLength in ipv6AccessConfig. The field is output only, an IPv6 address from a subnetwork associated with the instance will be allocated dynamically.
                        * networkTier (str, optional): This signifies the networking tier used for configuring this access configuration and can only take the following values: PREMIUM, STANDARD. If an AccessConfig is specified without a valid external IP address, an ephemeral IP will be created with this networkTier. If an AccessConfig with a valid external IP address is specified, it must match that of the networkTier associated with the Address resource owning that IP.
                        * name (str, optional): The name of this access configuration. The default and recommended name is External NAT, but you can use any arbitrary string, such as My external IP or Network Access.
                        * externalIpv6PrefixLength (int, optional): The prefix length of the external IPv6 range.
                        * setPublicPtr (bool, optional): Specifies whether a public DNS 'PTR' record should be created to map the external IP address of the instance to a DNS domain name. This field is not used in ipv6AccessConfig. A default PTR record will be created if the VM has external IPv6 range associated.
                        * publicPtrDomainName (str, optional): The DNS domain name for the public PTR record. You can set this field only if the `setPublicPtr` field is enabled in accessConfig. If this field is unspecified in ipv6AccessConfig, a default PTR record will be createc for first IP in associated external IPv6 range.
                        * type (str, optional): The type of configuration. The default and only option is ONE_TO_ONE_NAT.
                * kind (str, optional): [Output Only] Type of the resource. Always compute#networkInterface for network interfaces.
                * network (str, optional): URL of the VPC network resource for this instance. When creating an instance, if neither the network nor the subnetwork is specified, the default network global/networks/default is used. If the selected project doesn't have the default network, you must specify a network or subnet. If the network is not specified but the subnetwork is specified, the network is inferred. If you specify this property, you can specify the network as a full or partial URL. For example, the following are all valid URLs: - https://www.googleapis.com/compute/v1/projects/project/global/networks/ network - projects/project/global/networks/network - global/networks/default
                * stackType (str, optional): The stack type for this network interface to identify whether the IPv6 feature is enabled or not. If not specified, IPV4_ONLY will be used. This field can be both set at instance creation and update network interface operations.
                * internalIpv6PrefixLength (int, optional): The prefix length of the primary internal IPv6 range.
                * networkIP (str, optional): An IPv4 internal IP address to assign to the instance for this network interface. If not specified by the user, an unused internal IP is assigned by the system.
                * fingerprint (str, optional): Fingerprint hash of contents stored in this network interface. This field will be ignored when inserting an Instance or adding a NetworkInterface. An up-to-date fingerprint must be provided in order to update the NetworkInterface. The request will fail with error 400 Bad Request if the fingerprint is not provided, or 412 Precondition Failed if the fingerprint is out of date.
                * queueCount (int, optional): The networking queue count that's specified by users for the network interface. Both Rx and Tx queues will be set to this number. It'll be empty if not specified by the users.
                * nicType (str, optional): The type of vNIC to be used on this interface. This may be gVNIC or VirtioNet.
                * subnetwork (str, optional): The URL of the Subnetwork resource for this instance. If the network resource is in legacy mode, do not specify this field. If the network is in auto subnet mode, specifying the subnetwork is optional. If the network is in custom subnet mode, specifying the subnetwork is required. If you specify this field, you can specify the subnetwork as a full or partial URL. For example, the following are all valid URLs: - https://www.googleapis.com/compute/v1/projects/project/regions/region /subnetworks/subnetwork - regions/region/subnetworks/subnetwork
                * aliasIpRanges (list[Dict[str, Any]], optional): An array of alias IP ranges for this network interface. You can only specify this field for network interfaces in VPC networks.
                    * properties (Dict[str, Any], optional): An alias IP range attached to an instance's network interface.
                        * ipCidrRange (str, optional): The IP alias ranges to allocate for this interface. This IP CIDR range must belong to the specified subnetwork and cannot contain IP addresses reserved by system or used by other network interfaces. This range may be a single IP address (such as 10.2.3.4), a netmask (such as /24) or a CIDR-formatted string (such as 10.1.2.0/24).
                        * subnetworkRangeName (str, optional): The name of a subnetwork secondary IP range from which to allocate an IP alias range. If not specified, the primary range of the subnetwork is used.
        satisfies_pzs(bool, optional): [Output Only] Reserved for future use. Defaults to None.
        private_ipv6_google_access(str, optional): The private IPv6 google access type for the VM. If not specified, use INHERIT_FROM_SUBNETWORK as default. Defaults to None.
        advanced_machine_features(Dict[str, Any], optional): Controls for advanced machine-related behavior features. Defaults to None.
        key_revocation_action_type(str, optional): KeyRevocationActionType of the instance. Supported options are "STOP" and "NONE". The default value is "NONE" if it is not specified. Defaults to None.
        most_disruptive_allowed_action(str, optional): Specifies the most disruptive action that can be taken on the instance as part of the update. Compute Engine returns an error if the instance properties require a more disruptive action as part of the instance update. Valid options from lowest to highest are NO_EFFECT, REFRESH, and RESTART. Defaults to None.
        instance(str): Name of the instance resource to return.
        minimal_action(str, optional): Specifies the action to take when updating an instance even if the updated properties do not require it. If not specified, then Compute Engine acts based on the minimum action that the updated properties require. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

    """
    result = {
        "result": True,
        "old_state": None,
        "new_state": None,
        "name": name,
        "comment": [],
    }

    # Get the resource_id from ESM
    if not resource_id:
        resource_id = (ctx.get("old_state") or {}).get("resource_id")

    old = None

    # TODO: Handle operation result state
    if ctx.get("rerun_data"):
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.instances"
        )

        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    if resource_id:
        old_get_ret = await hub.exec.gcp.compute.instances.get(
            ctx, name=name, resource_id=resource_id
        )

        if not old_get_ret["result"] or not old_get_ret["ret"]:
            result["result"] = False
            result["comment"] += old_get_ret["comment"]
            # TODO: Handle the case when resource does not exist
            return result

        # copy.copy(old_get_ret['ret']) is needed to convert any objects of type NamespaceDict to dict
        # in old_get_ret['ret']. This is done so that comparisons with the plan_state which has
        # objects of type dict works properly
        old = copy.deepcopy(copy.copy(old_get_ret["ret"]))
        zone = hub.tool.gcp.resource_prop_utils.parse_link_to_zone(old["zone"])
        old["zone"] = zone
        result["old_state"] = old

    # TODO: Check if body contains the same parameters as old
    # to be autogenerated by pop-create based on insert/update props in properties.yaml
    resource_body = {
        "service_accounts": service_accounts,
        "name": name,
        "label_fingerprint": label_fingerprint,
        "min_cpu_platform": min_cpu_platform,
        "disks": disks,
        "network_performance_config": network_performance_config,
        "shielded_instance_integrity_policy": shielded_instance_integrity_policy,
        "private_ipv6_google_access": private_ipv6_google_access,
        "source_machine_image_encryption_key": source_machine_image_encryption_key,
        "confidential_instance_config": confidential_instance_config,
        "guest_accelerators": guest_accelerators,
        "description": description,
        "metadata": metadata,
        "resource_policies": resource_policies,
        "key_revocation_action_type": key_revocation_action_type,
        "hostname": hostname,
        "reservation_affinity": reservation_affinity,
        "tags": tags,
        "scheduling": scheduling,
        "advanced_machine_features": advanced_machine_features,
        "params": params,
        "fingerprint": fingerprint,
        "machine_type": machine_type,
        "source_machine_image": source_machine_image,
        "shielded_instance_config": shielded_instance_config,
        "labels": labels,
        "status": status,
        "deletion_protection": deletion_protection,
        "network_interfaces": network_interfaces,
        "can_ip_forward": can_ip_forward,
        "display_device": display_device,
        "zone": zone,
    }

    # TODO: How to handle query params which are not returned in the response body of get
    plan_state = {
        # "project": project,
        # "predefined_acl": predefined_acl,
        # "predefined_default_object_acl": predefined_default_object_acl,
        "resource_id": resource_id,
        **resource_body,
    }

    plan_state = {k: v for (k, v) in plan_state.items() if v is not None}
    operation = None
    if old:
        changes = hub.tool.gcp.utils.has_changes(old, plan_state, "compute.instances")

        if not changes:
            result["result"] = True
            result["comment"].append(
                hub.tool.gcp.comment_utils.already_exists_comment(
                    "gcp.compute.instance", name
                )
            )
            result["new_state"] = plan_state

            return result

        non_updatable_properties = (
            hub.tool.gcp.resource_prop_utils.get_non_updatable_properties(
                "compute.instances"
            )
        )

        changed_non_updatable_properties = []
        for key, value in plan_state.items():
            if value != old.get(key) and key in non_updatable_properties:
                changed_non_updatable_properties.append(key)

        if changed_non_updatable_properties:
            result["result"] = False
            result["comment"].append(
                hub.tool.gcp.comment_utils.non_updatable_properties_comment(
                    "gcp.compute.instance", name, changed_non_updatable_properties
                )
            )
            result["new_state"] = copy.deepcopy(old)
            return result

        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_update("gcp.compute.instance", name)
            )
            result["new_state"] = plan_state
            return result

        # TODO: if we fix isPending() to not update after creation we can make the fingerprint required upon update
        if not plan_state.get("fingerprint"):
            plan_state["fingerprint"] = old.get("fingerprint")
            resource_body["fingerprint"] = old.get("fingerprint")

        # Perform update
        update_ret = await hub.exec.gcp.compute.instances.update(
            hub, ctx, name=name, resource_id=resource_id, body=resource_body
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result
        result["comment"].append(
            hub.tool.gcp.comment_utils.update_comment("gcp.compute.instance", name)
        )

    else:
        if ctx["test"]:
            result["comment"].append(
                hub.tool.gcp.comment_utils.would_create_comment(
                    "gcp.compute.instance", name
                )
            )
            result["new_state"] = plan_state
            return result

        # Create
        create_ret = await hub.exec.gcp.compute.instances.insert(
            ctx, name=name, project=project, zone=zone, body=resource_body
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
            return result
        result["comment"].append(
            hub.tool.gcp.comment_utils.create_comment("gcp.compute.instance", name)
        )
        result["old_state"] = {}
        resource_id = create_ret["ret"].get("resource_id")
        if "compute#operation" in create_ret["ret"].get("kind"):
            operation = create_ret["ret"]

    if operation:
        operation_id = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
            operation.get("selfLink"), "compute.zoneOperations"
        )
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, operation_id, "compute.instances"
        )

        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    # Try getting the resource again
    # TODO: Reconciliation or waiter loop?
    # TODO: Check if this can be removed because insert and update may also return the necessary data on success
    get_ret = await hub.exec.gcp.compute.instances.get(
        ctx, name=name, resource_id=resource_id
    )

    if not get_ret["result"] and not get_ret["ret"]:
        result["result"] = False
        result["comment"] += get_ret["comment"]
        return result

    result["new_state"] = get_ret["ret"]

    return result


async def absent(
    hub,
    ctx,
    name: str = None,
    project: str = None,
    zone: str = None,
    resource_id: str = None,
    request_id: str = None,
) -> Dict[str, Any]:
    r"""

    Deletes the specified Instance resource. For more information, see Deleting an instance.

    Args:
        name(str): .
        resource_id(str, optional): . Defaults to None.
        instance(str): Name of the instance resource to return.
        project(str): Project ID for this request.
        zone(str): The name of the zone for this request.
        request_id(str, optional): An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. For example, consider a situation where you make an initial request and the request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported ( 00000000-0000-0000-0000-000000000000). Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

    """
    result = {
        "comment": [],
        "old_state": ctx.get("old_state"),
        "new_state": None,
        "name": name,
        "result": True,
    }

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if ctx.test:
        result["comment"] += [f"Would terminate instance '{name}'"]
        return result

    if not ctx.get("rerun_data"):
        # First iteration; invoke instance's delete()
        delete_ret = await hub.exec.gcp.compute.instances.delete(
            ctx, resource_id=resource_id
        )
        if delete_ret["ret"]:
            if "compute#operation" in delete_ret["ret"].get("kind"):
                result["result"] = False
                result["comment"] += delete_ret["comment"]
                result[
                    "rerun_data"
                ] = hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
                    delete_ret["ret"].get("selfLink"), "compute.zoneOperations"
                )
                return result

    else:
        # delete() has been called on some previous iteration
        handle_operation_ret = await hub.tool.gcp.operation_utils.handle_operation(
            ctx, ctx.get("rerun_data"), "compute.instances"
        )
        if not handle_operation_ret["result"]:
            result["result"] = False
            result["comment"] += handle_operation_ret["comment"]
            result["rerun_data"] = handle_operation_ret["rerun_data"]
            return result

        resource_id = handle_operation_ret["resource_id"]

    if not resource_id:
        result["comment"] += [f"Instance '{name}' already terminated"]
        return result

    result["comment"] += [f"Terminated instance '{name}'"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Retrieves the list of instances contained within the specified zone.

    Args:
        order_by(str, optional): Sorts list results by a certain order. By default, results are returned in alphanumerical order based on the resource name. You can also sort results in descending order based on the creation timestamp using `orderBy="creationTimestamp desc"`. This sorts results based on the `creationTimestamp` field in reverse chronological order (newest result first). Use this to sort resources like operations so that the newest operation is returned first. Currently, only sorting by `name` or `creationTimestamp desc` is supported. Defaults to None.
        max_results(int, optional): The maximum number of results per page that should be returned. If the number of available results is larger than `maxResults`, Compute Engine returns a `nextPageToken` that can be used to get the next page of results in subsequent list requests. Acceptable values are `0` to `500`, inclusive. (Default: `500`). Defaults to 500.
        return_partial_success(bool, optional): Opt-in for partial success behavior which provides partial results in case of failure. The default value is false. Defaults to None.
        page_token(str, optional): Specifies a page token to use. Set `pageToken` to the `nextPageToken` returned by a previous list request to get the next page of results. Defaults to None.
        zone(str): The name of the zone for this request.
        filter_(str, optional): A filter expression that filters resources listed in the response. Most Compute resources support two types of filter expressions: expressions that support regular expressions and expressions that follow API improvement proposal AIP-160. If you want to use AIP-160, your expression must specify the field name, an operator, and the value that you want to use for filtering. The value must be a string, a number, or a boolean. The operator must be either `=`, `!=`, `>`, `<`, `<=`, `>=` or `:`. For example, if you are filtering Compute Engine instances, you can exclude instances named `example-instance` by specifying `name != example-instance`. The `:` operator can be used with string fields to match substrings. For non-string fields it is equivalent to the `=` operator. The `:*` comparison can be used to test whether a key has been defined. For example, to find all objects with `owner` label use: ``` labels.owner:* ``` You can also filter nested fields. For example, you could specify `scheduling.automaticRestart = false` to include instances only if they are not scheduled for automatic restarts. You can use filtering on nested fields to filter based on resource labels. To filter on multiple expressions, provide each separate expression within parentheses. For example: ``` (scheduling.automaticRestart = true) (cpuPlatform = "Intel Skylake") ``` By default, each expression is an `AND` expression. However, you can include `AND` and `OR` expressions explicitly. For example: ``` (cpuPlatform = "Intel Skylake") OR (cpuPlatform = "Intel Broadwell") AND (scheduling.automaticRestart = true) ``` If you want to use a regular expression, use the `eq` (equal) or `ne` (not equal) operator against a single un-parenthesized expression with or without quotes or against multiple parenthesized expressions. Examples: `fieldname eq unquoted literal` `fieldname eq 'single quoted literal'` `fieldname eq "double quoted literal"` `(fieldname1 eq literal) (fieldname2 ne "literal")` The literal value is interpreted as a regular expression using Google RE2 library syntax. The literal value must match the entire field. For example, to filter for instances that do not end with name "instance", you would use `name ne .*instance`. Defaults to None.
        project(str): Project ID for this request.
        instance(str): Name of the instance resource to return.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:

        .. code-block:: bash

            $ idem describe gcp_auto.compute.instances

    """
    result = {}

    # TODO: Pagination
    describe_ret = await hub.exec.gcp.compute.instances.aggregatedList(
        ctx, project=ctx.acct.project_id
    )

    if not describe_ret["result"]:
        hub.log.debug(f"Could not describe instances {describe_ret['comment']}")
        return {}

    for resource in describe_ret["ret"]["items"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "gcp.compute.instances.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
