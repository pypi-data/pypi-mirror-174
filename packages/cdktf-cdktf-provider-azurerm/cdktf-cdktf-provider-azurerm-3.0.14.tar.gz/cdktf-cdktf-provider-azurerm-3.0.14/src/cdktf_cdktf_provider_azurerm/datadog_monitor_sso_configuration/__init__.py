'''
# `azurerm_datadog_monitor_sso_configuration`

Refer to the Terraform Registory for docs: [`azurerm_datadog_monitor_sso_configuration`](https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration).
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


class DatadogMonitorSsoConfiguration(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.datadogMonitorSsoConfiguration.DatadogMonitorSsoConfiguration",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration azurerm_datadog_monitor_sso_configuration}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        datadog_monitor_id: builtins.str,
        enterprise_application_id: builtins.str,
        single_sign_on_enabled: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatadogMonitorSsoConfigurationTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration azurerm_datadog_monitor_sso_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param datadog_monitor_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#datadog_monitor_id DatadogMonitorSsoConfiguration#datadog_monitor_id}.
        :param enterprise_application_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#enterprise_application_id DatadogMonitorSsoConfiguration#enterprise_application_id}.
        :param single_sign_on_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#single_sign_on_enabled DatadogMonitorSsoConfiguration#single_sign_on_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#id DatadogMonitorSsoConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#name DatadogMonitorSsoConfiguration#name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#timeouts DatadogMonitorSsoConfiguration#timeouts}
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
                datadog_monitor_id: builtins.str,
                enterprise_application_id: builtins.str,
                single_sign_on_enabled: builtins.str,
                id: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["DatadogMonitorSsoConfigurationTimeouts", typing.Dict[str, typing.Any]]] = None,
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
        config = DatadogMonitorSsoConfigurationConfig(
            datadog_monitor_id=datadog_monitor_id,
            enterprise_application_id=enterprise_application_id,
            single_sign_on_enabled=single_sign_on_enabled,
            id=id,
            name=name,
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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#create DatadogMonitorSsoConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#delete DatadogMonitorSsoConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#read DatadogMonitorSsoConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#update DatadogMonitorSsoConfiguration#update}.
        '''
        value = DatadogMonitorSsoConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
    @jsii.member(jsii_name="loginUrl")
    def login_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginUrl"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DatadogMonitorSsoConfigurationTimeoutsOutputReference":
        return typing.cast("DatadogMonitorSsoConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="datadogMonitorIdInput")
    def datadog_monitor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datadogMonitorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseApplicationIdInput")
    def enterprise_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enterpriseApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="singleSignOnEnabledInput")
    def single_sign_on_enabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "singleSignOnEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DatadogMonitorSsoConfigurationTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DatadogMonitorSsoConfigurationTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="datadogMonitorId")
    def datadog_monitor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datadogMonitorId"))

    @datadog_monitor_id.setter
    def datadog_monitor_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datadogMonitorId", value)

    @builtins.property
    @jsii.member(jsii_name="enterpriseApplicationId")
    def enterprise_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseApplicationId"))

    @enterprise_application_id.setter
    def enterprise_application_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enterpriseApplicationId", value)

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
    @jsii.member(jsii_name="singleSignOnEnabled")
    def single_sign_on_enabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleSignOnEnabled"))

    @single_sign_on_enabled.setter
    def single_sign_on_enabled(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "singleSignOnEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.datadogMonitorSsoConfiguration.DatadogMonitorSsoConfigurationConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "datadog_monitor_id": "datadogMonitorId",
        "enterprise_application_id": "enterpriseApplicationId",
        "single_sign_on_enabled": "singleSignOnEnabled",
        "id": "id",
        "name": "name",
        "timeouts": "timeouts",
    },
)
class DatadogMonitorSsoConfigurationConfig(cdktf.TerraformMetaArguments):
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
        datadog_monitor_id: builtins.str,
        enterprise_application_id: builtins.str,
        single_sign_on_enabled: builtins.str,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatadogMonitorSsoConfigurationTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param datadog_monitor_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#datadog_monitor_id DatadogMonitorSsoConfiguration#datadog_monitor_id}.
        :param enterprise_application_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#enterprise_application_id DatadogMonitorSsoConfiguration#enterprise_application_id}.
        :param single_sign_on_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#single_sign_on_enabled DatadogMonitorSsoConfiguration#single_sign_on_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#id DatadogMonitorSsoConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#name DatadogMonitorSsoConfiguration#name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#timeouts DatadogMonitorSsoConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DatadogMonitorSsoConfigurationTimeouts(**timeouts)
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
                datadog_monitor_id: builtins.str,
                enterprise_application_id: builtins.str,
                single_sign_on_enabled: builtins.str,
                id: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union["DatadogMonitorSsoConfigurationTimeouts", typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument datadog_monitor_id", value=datadog_monitor_id, expected_type=type_hints["datadog_monitor_id"])
            check_type(argname="argument enterprise_application_id", value=enterprise_application_id, expected_type=type_hints["enterprise_application_id"])
            check_type(argname="argument single_sign_on_enabled", value=single_sign_on_enabled, expected_type=type_hints["single_sign_on_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "datadog_monitor_id": datadog_monitor_id,
            "enterprise_application_id": enterprise_application_id,
            "single_sign_on_enabled": single_sign_on_enabled,
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
        if id is not None:
            self._values["id"] = id
        if name is not None:
            self._values["name"] = name
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
    def datadog_monitor_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#datadog_monitor_id DatadogMonitorSsoConfiguration#datadog_monitor_id}.'''
        result = self._values.get("datadog_monitor_id")
        assert result is not None, "Required property 'datadog_monitor_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enterprise_application_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#enterprise_application_id DatadogMonitorSsoConfiguration#enterprise_application_id}.'''
        result = self._values.get("enterprise_application_id")
        assert result is not None, "Required property 'enterprise_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def single_sign_on_enabled(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#single_sign_on_enabled DatadogMonitorSsoConfiguration#single_sign_on_enabled}.'''
        result = self._values.get("single_sign_on_enabled")
        assert result is not None, "Required property 'single_sign_on_enabled' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#id DatadogMonitorSsoConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#name DatadogMonitorSsoConfiguration#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DatadogMonitorSsoConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#timeouts DatadogMonitorSsoConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatadogMonitorSsoConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogMonitorSsoConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.datadogMonitorSsoConfiguration.DatadogMonitorSsoConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DatadogMonitorSsoConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#create DatadogMonitorSsoConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#delete DatadogMonitorSsoConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#read DatadogMonitorSsoConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#update DatadogMonitorSsoConfiguration#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#create DatadogMonitorSsoConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#delete DatadogMonitorSsoConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#read DatadogMonitorSsoConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/datadog_monitor_sso_configuration#update DatadogMonitorSsoConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogMonitorSsoConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogMonitorSsoConfigurationTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.datadogMonitorSsoConfiguration.DatadogMonitorSsoConfigurationTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[DatadogMonitorSsoConfigurationTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DatadogMonitorSsoConfigurationTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DatadogMonitorSsoConfigurationTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[DatadogMonitorSsoConfigurationTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DatadogMonitorSsoConfiguration",
    "DatadogMonitorSsoConfigurationConfig",
    "DatadogMonitorSsoConfigurationTimeouts",
    "DatadogMonitorSsoConfigurationTimeoutsOutputReference",
]

publication.publish()
