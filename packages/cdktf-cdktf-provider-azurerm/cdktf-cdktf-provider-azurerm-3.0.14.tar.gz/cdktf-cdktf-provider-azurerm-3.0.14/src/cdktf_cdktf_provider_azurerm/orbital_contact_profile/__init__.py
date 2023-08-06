'''
# `azurerm_orbital_contact_profile`

Refer to the Terraform Registory for docs: [`azurerm_orbital_contact_profile`](https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf
import constructs


class OrbitalContactProfile(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfile",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile azurerm_orbital_contact_profile}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        auto_tracking: builtins.str,
        links: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[str, typing.Any]]]],
        location: builtins.str,
        minimum_variable_contact_duration: builtins.str,
        name: builtins.str,
        network_configuration_subnet_id: builtins.str,
        resource_group_name: builtins.str,
        event_hub_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OrbitalContactProfileTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile azurerm_orbital_contact_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auto_tracking: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#auto_tracking OrbitalContactProfile#auto_tracking}.
        :param links: links block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#links OrbitalContactProfile#links}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#location OrbitalContactProfile#location}.
        :param minimum_variable_contact_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#minimum_variable_contact_duration OrbitalContactProfile#minimum_variable_contact_duration}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param network_configuration_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#network_configuration_subnet_id OrbitalContactProfile#network_configuration_subnet_id}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#resource_group_name OrbitalContactProfile#resource_group_name}.
        :param event_hub_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#event_hub_uri OrbitalContactProfile#event_hub_uri}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#id OrbitalContactProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_elevation_degrees: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#minimum_elevation_degrees OrbitalContactProfile#minimum_elevation_degrees}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#tags OrbitalContactProfile#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#timeouts OrbitalContactProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id_: builtins.str,
                *,
                auto_tracking: builtins.str,
                links: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[str, typing.Any]]]],
                location: builtins.str,
                minimum_variable_contact_duration: builtins.str,
                name: builtins.str,
                network_configuration_subnet_id: builtins.str,
                resource_group_name: builtins.str,
                event_hub_uri: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["OrbitalContactProfileTimeouts", typing.Dict[str, typing.Any]]] = None,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OrbitalContactProfileConfig(
            auto_tracking=auto_tracking,
            links=links,
            location=location,
            minimum_variable_contact_duration=minimum_variable_contact_duration,
            name=name,
            network_configuration_subnet_id=network_configuration_subnet_id,
            resource_group_name=resource_group_name,
            event_hub_uri=event_hub_uri,
            id=id,
            minimum_elevation_degrees=minimum_elevation_degrees,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLinks")
    def put_links(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLinks", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#create OrbitalContactProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#delete OrbitalContactProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#read OrbitalContactProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#update OrbitalContactProfile#update}.
        '''
        value = OrbitalContactProfileTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEventHubUri")
    def reset_event_hub_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHubUri", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinimumElevationDegrees")
    def reset_minimum_elevation_degrees(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumElevationDegrees", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> "OrbitalContactProfileLinksList":
        return typing.cast("OrbitalContactProfileLinksList", jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OrbitalContactProfileTimeoutsOutputReference":
        return typing.cast("OrbitalContactProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoTrackingInput")
    def auto_tracking_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoTrackingInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubUriInput")
    def event_hub_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubUriInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linksInput")
    def links_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinks"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinks"]]], jsii.get(self, "linksInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumElevationDegreesInput")
    def minimum_elevation_degrees_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumElevationDegreesInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumVariableContactDurationInput")
    def minimum_variable_contact_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumVariableContactDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationSubnetIdInput")
    def network_configuration_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkConfigurationSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["OrbitalContactProfileTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["OrbitalContactProfileTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoTracking")
    def auto_tracking(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoTracking"))

    @auto_tracking.setter
    def auto_tracking(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoTracking", value)

    @builtins.property
    @jsii.member(jsii_name="eventHubUri")
    def event_hub_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHubUri"))

    @event_hub_uri.setter
    def event_hub_uri(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHubUri", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="minimumElevationDegrees")
    def minimum_elevation_degrees(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumElevationDegrees"))

    @minimum_elevation_degrees.setter
    def minimum_elevation_degrees(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumElevationDegrees", value)

    @builtins.property
    @jsii.member(jsii_name="minimumVariableContactDuration")
    def minimum_variable_contact_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumVariableContactDuration"))

    @minimum_variable_contact_duration.setter
    def minimum_variable_contact_duration(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumVariableContactDuration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfigurationSubnetId")
    def network_configuration_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConfigurationSubnetId"))

    @network_configuration_subnet_id.setter
    def network_configuration_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConfigurationSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auto_tracking": "autoTracking",
        "links": "links",
        "location": "location",
        "minimum_variable_contact_duration": "minimumVariableContactDuration",
        "name": "name",
        "network_configuration_subnet_id": "networkConfigurationSubnetId",
        "resource_group_name": "resourceGroupName",
        "event_hub_uri": "eventHubUri",
        "id": "id",
        "minimum_elevation_degrees": "minimumElevationDegrees",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class OrbitalContactProfileConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        auto_tracking: builtins.str,
        links: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[str, typing.Any]]]],
        location: builtins.str,
        minimum_variable_contact_duration: builtins.str,
        name: builtins.str,
        network_configuration_subnet_id: builtins.str,
        resource_group_name: builtins.str,
        event_hub_uri: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["OrbitalContactProfileTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auto_tracking: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#auto_tracking OrbitalContactProfile#auto_tracking}.
        :param links: links block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#links OrbitalContactProfile#links}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#location OrbitalContactProfile#location}.
        :param minimum_variable_contact_duration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#minimum_variable_contact_duration OrbitalContactProfile#minimum_variable_contact_duration}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param network_configuration_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#network_configuration_subnet_id OrbitalContactProfile#network_configuration_subnet_id}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#resource_group_name OrbitalContactProfile#resource_group_name}.
        :param event_hub_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#event_hub_uri OrbitalContactProfile#event_hub_uri}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#id OrbitalContactProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param minimum_elevation_degrees: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#minimum_elevation_degrees OrbitalContactProfile#minimum_elevation_degrees}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#tags OrbitalContactProfile#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#timeouts OrbitalContactProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = OrbitalContactProfileTimeouts(**timeouts)
        if __debug__:
            def stub(
                *,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
                auto_tracking: builtins.str,
                links: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinks", typing.Dict[str, typing.Any]]]],
                location: builtins.str,
                minimum_variable_contact_duration: builtins.str,
                name: builtins.str,
                network_configuration_subnet_id: builtins.str,
                resource_group_name: builtins.str,
                event_hub_uri: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                minimum_elevation_degrees: typing.Optional[jsii.Number] = None,
                tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                timeouts: typing.Optional[typing.Union["OrbitalContactProfileTimeouts", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auto_tracking", value=auto_tracking, expected_type=type_hints["auto_tracking"])
            check_type(argname="argument links", value=links, expected_type=type_hints["links"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument minimum_variable_contact_duration", value=minimum_variable_contact_duration, expected_type=type_hints["minimum_variable_contact_duration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration_subnet_id", value=network_configuration_subnet_id, expected_type=type_hints["network_configuration_subnet_id"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument event_hub_uri", value=event_hub_uri, expected_type=type_hints["event_hub_uri"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument minimum_elevation_degrees", value=minimum_elevation_degrees, expected_type=type_hints["minimum_elevation_degrees"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "auto_tracking": auto_tracking,
            "links": links,
            "location": location,
            "minimum_variable_contact_duration": minimum_variable_contact_duration,
            "name": name,
            "network_configuration_subnet_id": network_configuration_subnet_id,
            "resource_group_name": resource_group_name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if event_hub_uri is not None:
            self._values["event_hub_uri"] = event_hub_uri
        if id is not None:
            self._values["id"] = id
        if minimum_elevation_degrees is not None:
            self._values["minimum_elevation_degrees"] = minimum_elevation_degrees
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[cdktf.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[cdktf.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]], result)

    @builtins.property
    def auto_tracking(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#auto_tracking OrbitalContactProfile#auto_tracking}.'''
        result = self._values.get("auto_tracking")
        assert result is not None, "Required property 'auto_tracking' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def links(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinks"]]:
        '''links block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#links OrbitalContactProfile#links}
        '''
        result = self._values.get("links")
        assert result is not None, "Required property 'links' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinks"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#location OrbitalContactProfile#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def minimum_variable_contact_duration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#minimum_variable_contact_duration OrbitalContactProfile#minimum_variable_contact_duration}.'''
        result = self._values.get("minimum_variable_contact_duration")
        assert result is not None, "Required property 'minimum_variable_contact_duration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_configuration_subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#network_configuration_subnet_id OrbitalContactProfile#network_configuration_subnet_id}.'''
        result = self._values.get("network_configuration_subnet_id")
        assert result is not None, "Required property 'network_configuration_subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#resource_group_name OrbitalContactProfile#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_hub_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#event_hub_uri OrbitalContactProfile#event_hub_uri}.'''
        result = self._values.get("event_hub_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#id OrbitalContactProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_elevation_degrees(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#minimum_elevation_degrees OrbitalContactProfile#minimum_elevation_degrees}.'''
        result = self._values.get("minimum_elevation_degrees")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#tags OrbitalContactProfile#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OrbitalContactProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#timeouts OrbitalContactProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OrbitalContactProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinks",
    jsii_struct_bases=[],
    name_mapping={
        "channels": "channels",
        "direction": "direction",
        "name": "name",
        "polarization": "polarization",
    },
)
class OrbitalContactProfileLinks:
    def __init__(
        self,
        *,
        channels: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinksChannels", typing.Dict[str, typing.Any]]]],
        direction: builtins.str,
        name: builtins.str,
        polarization: builtins.str,
    ) -> None:
        '''
        :param channels: channels block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#channels OrbitalContactProfile#channels}
        :param direction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#direction OrbitalContactProfile#direction}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param polarization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#polarization OrbitalContactProfile#polarization}.
        '''
        if __debug__:
            def stub(
                *,
                channels: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinksChannels", typing.Dict[str, typing.Any]]]],
                direction: builtins.str,
                name: builtins.str,
                polarization: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument channels", value=channels, expected_type=type_hints["channels"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument polarization", value=polarization, expected_type=type_hints["polarization"])
        self._values: typing.Dict[str, typing.Any] = {
            "channels": channels,
            "direction": direction,
            "name": name,
            "polarization": polarization,
        }

    @builtins.property
    def channels(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinksChannels"]]:
        '''channels block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#channels OrbitalContactProfile#channels}
        '''
        result = self._values.get("channels")
        assert result is not None, "Required property 'channels' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinksChannels"]], result)

    @builtins.property
    def direction(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#direction OrbitalContactProfile#direction}.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def polarization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#polarization OrbitalContactProfile#polarization}.'''
        result = self._values.get("polarization")
        assert result is not None, "Required property 'polarization' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileLinks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannels",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_mhz": "bandwidthMhz",
        "center_frequency_mhz": "centerFrequencyMhz",
        "end_point": "endPoint",
        "name": "name",
        "demodulation_configuration": "demodulationConfiguration",
        "modulation_configuration": "modulationConfiguration",
    },
)
class OrbitalContactProfileLinksChannels:
    def __init__(
        self,
        *,
        bandwidth_mhz: jsii.Number,
        center_frequency_mhz: jsii.Number,
        end_point: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinksChannelsEndPoint", typing.Dict[str, typing.Any]]]],
        name: builtins.str,
        demodulation_configuration: typing.Optional[builtins.str] = None,
        modulation_configuration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_mhz: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#bandwidth_mhz OrbitalContactProfile#bandwidth_mhz}.
        :param center_frequency_mhz: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#center_frequency_mhz OrbitalContactProfile#center_frequency_mhz}.
        :param end_point: end_point block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#end_point OrbitalContactProfile#end_point}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.
        :param demodulation_configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#demodulation_configuration OrbitalContactProfile#demodulation_configuration}.
        :param modulation_configuration: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#modulation_configuration OrbitalContactProfile#modulation_configuration}.
        '''
        if __debug__:
            def stub(
                *,
                bandwidth_mhz: jsii.Number,
                center_frequency_mhz: jsii.Number,
                end_point: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["OrbitalContactProfileLinksChannelsEndPoint", typing.Dict[str, typing.Any]]]],
                name: builtins.str,
                demodulation_configuration: typing.Optional[builtins.str] = None,
                modulation_configuration: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument bandwidth_mhz", value=bandwidth_mhz, expected_type=type_hints["bandwidth_mhz"])
            check_type(argname="argument center_frequency_mhz", value=center_frequency_mhz, expected_type=type_hints["center_frequency_mhz"])
            check_type(argname="argument end_point", value=end_point, expected_type=type_hints["end_point"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument demodulation_configuration", value=demodulation_configuration, expected_type=type_hints["demodulation_configuration"])
            check_type(argname="argument modulation_configuration", value=modulation_configuration, expected_type=type_hints["modulation_configuration"])
        self._values: typing.Dict[str, typing.Any] = {
            "bandwidth_mhz": bandwidth_mhz,
            "center_frequency_mhz": center_frequency_mhz,
            "end_point": end_point,
            "name": name,
        }
        if demodulation_configuration is not None:
            self._values["demodulation_configuration"] = demodulation_configuration
        if modulation_configuration is not None:
            self._values["modulation_configuration"] = modulation_configuration

    @builtins.property
    def bandwidth_mhz(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#bandwidth_mhz OrbitalContactProfile#bandwidth_mhz}.'''
        result = self._values.get("bandwidth_mhz")
        assert result is not None, "Required property 'bandwidth_mhz' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def center_frequency_mhz(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#center_frequency_mhz OrbitalContactProfile#center_frequency_mhz}.'''
        result = self._values.get("center_frequency_mhz")
        assert result is not None, "Required property 'center_frequency_mhz' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def end_point(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinksChannelsEndPoint"]]:
        '''end_point block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#end_point OrbitalContactProfile#end_point}
        '''
        result = self._values.get("end_point")
        assert result is not None, "Required property 'end_point' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["OrbitalContactProfileLinksChannelsEndPoint"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#name OrbitalContactProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def demodulation_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#demodulation_configuration OrbitalContactProfile#demodulation_configuration}.'''
        result = self._values.get("demodulation_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modulation_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#modulation_configuration OrbitalContactProfile#modulation_configuration}.'''
        result = self._values.get("modulation_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileLinksChannels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsEndPoint",
    jsii_struct_bases=[],
    name_mapping={
        "end_point_name": "endPointName",
        "ip_address": "ipAddress",
        "port": "port",
        "protocol": "protocol",
    },
)
class OrbitalContactProfileLinksChannelsEndPoint:
    def __init__(
        self,
        *,
        end_point_name: builtins.str,
        ip_address: builtins.str,
        port: builtins.str,
        protocol: builtins.str,
    ) -> None:
        '''
        :param end_point_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#end_point_name OrbitalContactProfile#end_point_name}.
        :param ip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#ip_address OrbitalContactProfile#ip_address}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#port OrbitalContactProfile#port}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#protocol OrbitalContactProfile#protocol}.
        '''
        if __debug__:
            def stub(
                *,
                end_point_name: builtins.str,
                ip_address: builtins.str,
                port: builtins.str,
                protocol: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument end_point_name", value=end_point_name, expected_type=type_hints["end_point_name"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[str, typing.Any] = {
            "end_point_name": end_point_name,
            "ip_address": ip_address,
            "port": port,
            "protocol": protocol,
        }

    @builtins.property
    def end_point_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#end_point_name OrbitalContactProfile#end_point_name}.'''
        result = self._values.get("end_point_name")
        assert result is not None, "Required property 'end_point_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#ip_address OrbitalContactProfile#ip_address}.'''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#port OrbitalContactProfile#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#protocol OrbitalContactProfile#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileLinksChannelsEndPoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrbitalContactProfileLinksChannelsEndPointList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsEndPointList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrbitalContactProfileLinksChannelsEndPointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrbitalContactProfileLinksChannelsEndPointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrbitalContactProfileLinksChannelsEndPointOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsEndPointOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endPointNameInput")
    def end_point_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endPointNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="endPointName")
    def end_point_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endPointName"))

    @end_point_name.setter
    def end_point_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endPointName", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "port"))

    @port.setter
    def port(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrbitalContactProfileLinksChannelsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OrbitalContactProfileLinksChannelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrbitalContactProfileLinksChannelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrbitalContactProfileLinksChannelsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksChannelsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEndPoint")
    def put_end_point(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannelsEndPoint, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEndPoint", [value]))

    @jsii.member(jsii_name="resetDemodulationConfiguration")
    def reset_demodulation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDemodulationConfiguration", []))

    @jsii.member(jsii_name="resetModulationConfiguration")
    def reset_modulation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModulationConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="endPoint")
    def end_point(self) -> OrbitalContactProfileLinksChannelsEndPointList:
        return typing.cast(OrbitalContactProfileLinksChannelsEndPointList, jsii.get(self, "endPoint"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthMhzInput")
    def bandwidth_mhz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthMhzInput"))

    @builtins.property
    @jsii.member(jsii_name="centerFrequencyMhzInput")
    def center_frequency_mhz_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "centerFrequencyMhzInput"))

    @builtins.property
    @jsii.member(jsii_name="demodulationConfigurationInput")
    def demodulation_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "demodulationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="endPointInput")
    def end_point_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannelsEndPoint]]], jsii.get(self, "endPointInput"))

    @builtins.property
    @jsii.member(jsii_name="modulationConfigurationInput")
    def modulation_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modulationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthMhz")
    def bandwidth_mhz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthMhz"))

    @bandwidth_mhz.setter
    def bandwidth_mhz(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthMhz", value)

    @builtins.property
    @jsii.member(jsii_name="centerFrequencyMhz")
    def center_frequency_mhz(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "centerFrequencyMhz"))

    @center_frequency_mhz.setter
    def center_frequency_mhz(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "centerFrequencyMhz", value)

    @builtins.property
    @jsii.member(jsii_name="demodulationConfiguration")
    def demodulation_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "demodulationConfiguration"))

    @demodulation_configuration.setter
    def demodulation_configuration(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "demodulationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="modulationConfiguration")
    def modulation_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modulationConfiguration"))

    @modulation_configuration.setter
    def modulation_configuration(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modulationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OrbitalContactProfileLinksChannels, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OrbitalContactProfileLinksChannels, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OrbitalContactProfileLinksChannels, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[OrbitalContactProfileLinksChannels, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrbitalContactProfileLinksList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OrbitalContactProfileLinksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OrbitalContactProfileLinksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinks]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinks]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinks]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OrbitalContactProfileLinksOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileLinksOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putChannels")
    def put_channels(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannels, typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[OrbitalContactProfileLinksChannels, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putChannels", [value]))

    @builtins.property
    @jsii.member(jsii_name="channels")
    def channels(self) -> OrbitalContactProfileLinksChannelsList:
        return typing.cast(OrbitalContactProfileLinksChannelsList, jsii.get(self, "channels"))

    @builtins.property
    @jsii.member(jsii_name="channelsInput")
    def channels_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[OrbitalContactProfileLinksChannels]]], jsii.get(self, "channelsInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="polarizationInput")
    def polarization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "polarizationInput"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="polarization")
    def polarization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "polarization"))

    @polarization.setter
    def polarization(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "polarization", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OrbitalContactProfileLinks, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OrbitalContactProfileLinks, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OrbitalContactProfileLinks, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[OrbitalContactProfileLinks, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class OrbitalContactProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#create OrbitalContactProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#delete OrbitalContactProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#read OrbitalContactProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#update OrbitalContactProfile#update}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                delete: typing.Optional[builtins.str] = None,
                read: typing.Optional[builtins.str] = None,
                update: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#create OrbitalContactProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#delete OrbitalContactProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#read OrbitalContactProfile#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/orbital_contact_profile#update OrbitalContactProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrbitalContactProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrbitalContactProfileTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.orbitalContactProfile.OrbitalContactProfileTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OrbitalContactProfileTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OrbitalContactProfileTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OrbitalContactProfileTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[OrbitalContactProfileTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OrbitalContactProfile",
    "OrbitalContactProfileConfig",
    "OrbitalContactProfileLinks",
    "OrbitalContactProfileLinksChannels",
    "OrbitalContactProfileLinksChannelsEndPoint",
    "OrbitalContactProfileLinksChannelsEndPointList",
    "OrbitalContactProfileLinksChannelsEndPointOutputReference",
    "OrbitalContactProfileLinksChannelsList",
    "OrbitalContactProfileLinksChannelsOutputReference",
    "OrbitalContactProfileLinksList",
    "OrbitalContactProfileLinksOutputReference",
    "OrbitalContactProfileTimeouts",
    "OrbitalContactProfileTimeoutsOutputReference",
]

publication.publish()
