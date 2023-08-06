'''
# `kubernetes_env`

Refer to the Terraform Registory for docs: [`kubernetes_env`](https://www.terraform.io/docs/providers/kubernetes/r/env).
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


class Env(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.Env",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/kubernetes/r/env kubernetes_env}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        api_version: builtins.str,
        container: builtins.str,
        env: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[str, typing.Any]]]],
        kind: builtins.str,
        metadata: typing.Union["EnvMetadata", typing.Dict[str, typing.Any]],
        field_manager: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/kubernetes/r/env kubernetes_env} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_version: Resource API version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#api_version Env#api_version}
        :param container: Name of the container for which we are updating the environment variables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#container Env#container}
        :param env: env block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#env Env#env}
        :param kind: Resource Kind. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#kind Env#kind}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#metadata Env#metadata}
        :param field_manager: Set the name of the field manager for the specified environment variables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_manager Env#field_manager}
        :param force: Force overwriting environments that were created or edited outside of Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#force Env#force}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#id Env#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
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
                api_version: builtins.str,
                container: builtins.str,
                env: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[str, typing.Any]]]],
                kind: builtins.str,
                metadata: typing.Union["EnvMetadata", typing.Dict[str, typing.Any]],
                field_manager: typing.Optional[builtins.str] = None,
                force: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
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
        config = EnvConfig(
            api_version=api_version,
            container=container,
            env=env,
            kind=kind,
            metadata=metadata,
            field_manager=field_manager,
            force=force,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        *,
        name: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param namespace: The namespace of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#namespace Env#namespace}
        '''
        value = EnvMetadata(name=name, namespace=namespace)

        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="resetFieldManager")
    def reset_field_manager(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldManager", []))

    @jsii.member(jsii_name="resetForce")
    def reset_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForce", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> "EnvEnvList":
        return typing.cast("EnvEnvList", jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "EnvMetadataOutputReference":
        return typing.cast("EnvMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="containerInput")
    def container_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["EnvEnv"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["EnvEnv"]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldManagerInput")
    def field_manager_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldManagerInput"))

    @builtins.property
    @jsii.member(jsii_name="forceInput")
    def force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "forceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional["EnvMetadata"]:
        return typing.cast(typing.Optional["EnvMetadata"], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value)

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "container"))

    @container.setter
    def container(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value)

    @builtins.property
    @jsii.member(jsii_name="fieldManager")
    def field_manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldManager"))

    @field_manager.setter
    def field_manager(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldManager", value)

    @builtins.property
    @jsii.member(jsii_name="force")
    def force(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "force"))

    @force.setter
    def force(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "force", value)

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
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_version": "apiVersion",
        "container": "container",
        "env": "env",
        "kind": "kind",
        "metadata": "metadata",
        "field_manager": "fieldManager",
        "force": "force",
        "id": "id",
    },
)
class EnvConfig(cdktf.TerraformMetaArguments):
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
        api_version: builtins.str,
        container: builtins.str,
        env: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[str, typing.Any]]]],
        kind: builtins.str,
        metadata: typing.Union["EnvMetadata", typing.Dict[str, typing.Any]],
        field_manager: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_version: Resource API version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#api_version Env#api_version}
        :param container: Name of the container for which we are updating the environment variables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#container Env#container}
        :param env: env block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#env Env#env}
        :param kind: Resource Kind. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#kind Env#kind}
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#metadata Env#metadata}
        :param field_manager: Set the name of the field manager for the specified environment variables. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_manager Env#field_manager}
        :param force: Force overwriting environments that were created or edited outside of Terraform. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#force Env#force}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#id Env#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(metadata, dict):
            metadata = EnvMetadata(**metadata)
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
                api_version: builtins.str,
                container: builtins.str,
                env: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["EnvEnv", typing.Dict[str, typing.Any]]]],
                kind: builtins.str,
                metadata: typing.Union["EnvMetadata", typing.Dict[str, typing.Any]],
                field_manager: typing.Optional[builtins.str] = None,
                force: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument field_manager", value=field_manager, expected_type=type_hints["field_manager"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_version": api_version,
            "container": container,
            "env": env,
            "kind": kind,
            "metadata": metadata,
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
        if field_manager is not None:
            self._values["field_manager"] = field_manager
        if force is not None:
            self._values["force"] = force
        if id is not None:
            self._values["id"] = id

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
    def api_version(self) -> builtins.str:
        '''Resource API version.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#api_version Env#api_version}
        '''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container(self) -> builtins.str:
        '''Name of the container for which we are updating the environment variables.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#container Env#container}
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def env(self) -> typing.Union[cdktf.IResolvable, typing.List["EnvEnv"]]:
        '''env block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#env Env#env}
        '''
        result = self._values.get("env")
        assert result is not None, "Required property 'env' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["EnvEnv"]], result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''Resource Kind.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#kind Env#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metadata(self) -> "EnvMetadata":
        '''metadata block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#metadata Env#metadata}
        '''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("EnvMetadata", result)

    @builtins.property
    def field_manager(self) -> typing.Optional[builtins.str]:
        '''Set the name of the field manager for the specified environment variables.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_manager Env#field_manager}
        '''
        result = self._values.get("field_manager")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Force overwriting environments that were created or edited outside of Terraform.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#force Env#force}
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#id Env#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_from": "valueFrom"},
)
class EnvEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
        value_from: typing.Optional[typing.Union["EnvEnvValueFrom", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a C_IDENTIFIER. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param value: Variable references $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#value Env#value}
        :param value_from: value_from block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#value_from Env#value_from}
        '''
        if isinstance(value_from, dict):
            value_from = EnvEnvValueFrom(**value_from)
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                value: typing.Optional[builtins.str] = None,
                value_from: typing.Optional[typing.Union["EnvEnvValueFrom", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument value_from", value=value_from, expected_type=type_hints["value_from"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value
        if value_from is not None:
            self._values["value_from"] = value_from

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the environment variable. Must be a C_IDENTIFIER.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Variable references $(VAR_NAME) are expanded using the previous defined environment variables in the container and any service environment variables.

        If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. Defaults to "".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#value Env#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_from(self) -> typing.Optional["EnvEnvValueFrom"]:
        '''value_from block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#value_from Env#value_from}
        '''
        result = self._values.get("value_from")
        return typing.cast(typing.Optional["EnvEnvValueFrom"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvList",
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
    def get(self, index: jsii.Number) -> "EnvEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EnvEnvOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[EnvEnv]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[EnvEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[EnvEnv]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[EnvEnv]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EnvEnvOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvOutputReference",
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

    @jsii.member(jsii_name="putValueFrom")
    def put_value_from(
        self,
        *,
        config_map_key_ref: typing.Optional[typing.Union["EnvEnvValueFromConfigMapKeyRef", typing.Dict[str, typing.Any]]] = None,
        field_ref: typing.Optional[typing.Union["EnvEnvValueFromFieldRef", typing.Dict[str, typing.Any]]] = None,
        resource_field_ref: typing.Optional[typing.Union["EnvEnvValueFromResourceFieldRef", typing.Dict[str, typing.Any]]] = None,
        secret_key_ref: typing.Optional[typing.Union["EnvEnvValueFromSecretKeyRef", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_map_key_ref: config_map_key_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#config_map_key_ref Env#config_map_key_ref}
        :param field_ref: field_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_ref Env#field_ref}
        :param resource_field_ref: resource_field_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#resource_field_ref Env#resource_field_ref}
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#secret_key_ref Env#secret_key_ref}
        '''
        value = EnvEnvValueFrom(
            config_map_key_ref=config_map_key_ref,
            field_ref=field_ref,
            resource_field_ref=resource_field_ref,
            secret_key_ref=secret_key_ref,
        )

        return typing.cast(None, jsii.invoke(self, "putValueFrom", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValueFrom")
    def reset_value_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueFrom", []))

    @builtins.property
    @jsii.member(jsii_name="valueFrom")
    def value_from(self) -> "EnvEnvValueFromOutputReference":
        return typing.cast("EnvEnvValueFromOutputReference", jsii.get(self, "valueFrom"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueFromInput")
    def value_from_input(self) -> typing.Optional["EnvEnvValueFrom"]:
        return typing.cast(typing.Optional["EnvEnvValueFrom"], jsii.get(self, "valueFromInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

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
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[EnvEnv, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[EnvEnv, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[EnvEnv, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[EnvEnv, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFrom",
    jsii_struct_bases=[],
    name_mapping={
        "config_map_key_ref": "configMapKeyRef",
        "field_ref": "fieldRef",
        "resource_field_ref": "resourceFieldRef",
        "secret_key_ref": "secretKeyRef",
    },
)
class EnvEnvValueFrom:
    def __init__(
        self,
        *,
        config_map_key_ref: typing.Optional[typing.Union["EnvEnvValueFromConfigMapKeyRef", typing.Dict[str, typing.Any]]] = None,
        field_ref: typing.Optional[typing.Union["EnvEnvValueFromFieldRef", typing.Dict[str, typing.Any]]] = None,
        resource_field_ref: typing.Optional[typing.Union["EnvEnvValueFromResourceFieldRef", typing.Dict[str, typing.Any]]] = None,
        secret_key_ref: typing.Optional[typing.Union["EnvEnvValueFromSecretKeyRef", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_map_key_ref: config_map_key_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#config_map_key_ref Env#config_map_key_ref}
        :param field_ref: field_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_ref Env#field_ref}
        :param resource_field_ref: resource_field_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#resource_field_ref Env#resource_field_ref}
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#secret_key_ref Env#secret_key_ref}
        '''
        if isinstance(config_map_key_ref, dict):
            config_map_key_ref = EnvEnvValueFromConfigMapKeyRef(**config_map_key_ref)
        if isinstance(field_ref, dict):
            field_ref = EnvEnvValueFromFieldRef(**field_ref)
        if isinstance(resource_field_ref, dict):
            resource_field_ref = EnvEnvValueFromResourceFieldRef(**resource_field_ref)
        if isinstance(secret_key_ref, dict):
            secret_key_ref = EnvEnvValueFromSecretKeyRef(**secret_key_ref)
        if __debug__:
            def stub(
                *,
                config_map_key_ref: typing.Optional[typing.Union["EnvEnvValueFromConfigMapKeyRef", typing.Dict[str, typing.Any]]] = None,
                field_ref: typing.Optional[typing.Union["EnvEnvValueFromFieldRef", typing.Dict[str, typing.Any]]] = None,
                resource_field_ref: typing.Optional[typing.Union["EnvEnvValueFromResourceFieldRef", typing.Dict[str, typing.Any]]] = None,
                secret_key_ref: typing.Optional[typing.Union["EnvEnvValueFromSecretKeyRef", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument config_map_key_ref", value=config_map_key_ref, expected_type=type_hints["config_map_key_ref"])
            check_type(argname="argument field_ref", value=field_ref, expected_type=type_hints["field_ref"])
            check_type(argname="argument resource_field_ref", value=resource_field_ref, expected_type=type_hints["resource_field_ref"])
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[str, typing.Any] = {}
        if config_map_key_ref is not None:
            self._values["config_map_key_ref"] = config_map_key_ref
        if field_ref is not None:
            self._values["field_ref"] = field_ref
        if resource_field_ref is not None:
            self._values["resource_field_ref"] = resource_field_ref
        if secret_key_ref is not None:
            self._values["secret_key_ref"] = secret_key_ref

    @builtins.property
    def config_map_key_ref(self) -> typing.Optional["EnvEnvValueFromConfigMapKeyRef"]:
        '''config_map_key_ref block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#config_map_key_ref Env#config_map_key_ref}
        '''
        result = self._values.get("config_map_key_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromConfigMapKeyRef"], result)

    @builtins.property
    def field_ref(self) -> typing.Optional["EnvEnvValueFromFieldRef"]:
        '''field_ref block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_ref Env#field_ref}
        '''
        result = self._values.get("field_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromFieldRef"], result)

    @builtins.property
    def resource_field_ref(self) -> typing.Optional["EnvEnvValueFromResourceFieldRef"]:
        '''resource_field_ref block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#resource_field_ref Env#resource_field_ref}
        '''
        result = self._values.get("resource_field_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromResourceFieldRef"], result)

    @builtins.property
    def secret_key_ref(self) -> typing.Optional["EnvEnvValueFromSecretKeyRef"]:
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#secret_key_ref Env#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        return typing.cast(typing.Optional["EnvEnvValueFromSecretKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromConfigMapKeyRef",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class EnvEnvValueFromConfigMapKeyRef:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key to select. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#key Env#key}
        :param name: Name of the referent. More info: http://kubernetes.io/docs/user-guide/identifiers#names. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param optional: Specify whether the ConfigMap or its key must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#optional Env#optional}
        '''
        if __debug__:
            def stub(
                *,
                key: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                optional: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The key to select.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#key Env#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: http://kubernetes.io/docs/user-guide/identifiers#names.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Specify whether the ConfigMap or its key must be defined.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#optional Env#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromConfigMapKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromConfigMapKeyRefOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromConfigMapKeyRefOutputReference",
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

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

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
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromConfigMapKeyRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromConfigMapKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnvEnvValueFromConfigMapKeyRef],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[EnvEnvValueFromConfigMapKeyRef]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromFieldRef",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "field_path": "fieldPath"},
)
class EnvEnvValueFromFieldRef:
    def __init__(
        self,
        *,
        api_version: typing.Optional[builtins.str] = None,
        field_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_version: Version of the schema the FieldPath is written in terms of, defaults to "v1". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#api_version Env#api_version}
        :param field_path: Path of the field to select in the specified API version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_path Env#field_path}
        '''
        if __debug__:
            def stub(
                *,
                api_version: typing.Optional[builtins.str] = None,
                field_path: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument field_path", value=field_path, expected_type=type_hints["field_path"])
        self._values: typing.Dict[str, typing.Any] = {}
        if api_version is not None:
            self._values["api_version"] = api_version
        if field_path is not None:
            self._values["field_path"] = field_path

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''Version of the schema the FieldPath is written in terms of, defaults to "v1".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#api_version Env#api_version}
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_path(self) -> typing.Optional[builtins.str]:
        '''Path of the field to select in the specified API version.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_path Env#field_path}
        '''
        result = self._values.get("field_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromFieldRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromFieldRefOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromFieldRefOutputReference",
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

    @jsii.member(jsii_name="resetApiVersion")
    def reset_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersion", []))

    @jsii.member(jsii_name="resetFieldPath")
    def reset_field_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldPath", []))

    @builtins.property
    @jsii.member(jsii_name="apiVersionInput")
    def api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldPathInput")
    def field_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldPathInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiVersion"))

    @api_version.setter
    def api_version(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersion", value)

    @builtins.property
    @jsii.member(jsii_name="fieldPath")
    def field_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldPath"))

    @field_path.setter
    def field_path(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromFieldRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromFieldRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EnvEnvValueFromFieldRef]) -> None:
        if __debug__:
            def stub(value: typing.Optional[EnvEnvValueFromFieldRef]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EnvEnvValueFromOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromOutputReference",
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

    @jsii.member(jsii_name="putConfigMapKeyRef")
    def put_config_map_key_ref(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key to select. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#key Env#key}
        :param name: Name of the referent. More info: http://kubernetes.io/docs/user-guide/identifiers#names. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param optional: Specify whether the ConfigMap or its key must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#optional Env#optional}
        '''
        value = EnvEnvValueFromConfigMapKeyRef(key=key, name=name, optional=optional)

        return typing.cast(None, jsii.invoke(self, "putConfigMapKeyRef", [value]))

    @jsii.member(jsii_name="putFieldRef")
    def put_field_ref(
        self,
        *,
        api_version: typing.Optional[builtins.str] = None,
        field_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_version: Version of the schema the FieldPath is written in terms of, defaults to "v1". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#api_version Env#api_version}
        :param field_path: Path of the field to select in the specified API version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#field_path Env#field_path}
        '''
        value = EnvEnvValueFromFieldRef(api_version=api_version, field_path=field_path)

        return typing.cast(None, jsii.invoke(self, "putFieldRef", [value]))

    @jsii.member(jsii_name="putResourceFieldRef")
    def put_resource_field_ref(
        self,
        *,
        resource: builtins.str,
        container_name: typing.Optional[builtins.str] = None,
        divisor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource: Resource to select. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#resource Env#resource}
        :param container_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#container_name Env#container_name}.
        :param divisor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#divisor Env#divisor}.
        '''
        value = EnvEnvValueFromResourceFieldRef(
            resource=resource, container_name=container_name, divisor=divisor
        )

        return typing.cast(None, jsii.invoke(self, "putResourceFieldRef", [value]))

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key of the secret to select from. Must be a valid secret key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#key Env#key}
        :param name: Name of the referent. More info: http://kubernetes.io/docs/user-guide/identifiers#names. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param optional: Specify whether the Secret or its key must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#optional Env#optional}
        '''
        value = EnvEnvValueFromSecretKeyRef(key=key, name=name, optional=optional)

        return typing.cast(None, jsii.invoke(self, "putSecretKeyRef", [value]))

    @jsii.member(jsii_name="resetConfigMapKeyRef")
    def reset_config_map_key_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigMapKeyRef", []))

    @jsii.member(jsii_name="resetFieldRef")
    def reset_field_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldRef", []))

    @jsii.member(jsii_name="resetResourceFieldRef")
    def reset_resource_field_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceFieldRef", []))

    @jsii.member(jsii_name="resetSecretKeyRef")
    def reset_secret_key_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKeyRef", []))

    @builtins.property
    @jsii.member(jsii_name="configMapKeyRef")
    def config_map_key_ref(self) -> EnvEnvValueFromConfigMapKeyRefOutputReference:
        return typing.cast(EnvEnvValueFromConfigMapKeyRefOutputReference, jsii.get(self, "configMapKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="fieldRef")
    def field_ref(self) -> EnvEnvValueFromFieldRefOutputReference:
        return typing.cast(EnvEnvValueFromFieldRefOutputReference, jsii.get(self, "fieldRef"))

    @builtins.property
    @jsii.member(jsii_name="resourceFieldRef")
    def resource_field_ref(self) -> "EnvEnvValueFromResourceFieldRefOutputReference":
        return typing.cast("EnvEnvValueFromResourceFieldRefOutputReference", jsii.get(self, "resourceFieldRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRef")
    def secret_key_ref(self) -> "EnvEnvValueFromSecretKeyRefOutputReference":
        return typing.cast("EnvEnvValueFromSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="configMapKeyRefInput")
    def config_map_key_ref_input(
        self,
    ) -> typing.Optional[EnvEnvValueFromConfigMapKeyRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromConfigMapKeyRef], jsii.get(self, "configMapKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldRefInput")
    def field_ref_input(self) -> typing.Optional[EnvEnvValueFromFieldRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromFieldRef], jsii.get(self, "fieldRefInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceFieldRefInput")
    def resource_field_ref_input(
        self,
    ) -> typing.Optional["EnvEnvValueFromResourceFieldRef"]:
        return typing.cast(typing.Optional["EnvEnvValueFromResourceFieldRef"], jsii.get(self, "resourceFieldRefInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(self) -> typing.Optional["EnvEnvValueFromSecretKeyRef"]:
        return typing.cast(typing.Optional["EnvEnvValueFromSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFrom]:
        return typing.cast(typing.Optional[EnvEnvValueFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EnvEnvValueFrom]) -> None:
        if __debug__:
            def stub(value: typing.Optional[EnvEnvValueFrom]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromResourceFieldRef",
    jsii_struct_bases=[],
    name_mapping={
        "resource": "resource",
        "container_name": "containerName",
        "divisor": "divisor",
    },
)
class EnvEnvValueFromResourceFieldRef:
    def __init__(
        self,
        *,
        resource: builtins.str,
        container_name: typing.Optional[builtins.str] = None,
        divisor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param resource: Resource to select. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#resource Env#resource}
        :param container_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#container_name Env#container_name}.
        :param divisor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#divisor Env#divisor}.
        '''
        if __debug__:
            def stub(
                *,
                resource: builtins.str,
                container_name: typing.Optional[builtins.str] = None,
                divisor: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument divisor", value=divisor, expected_type=type_hints["divisor"])
        self._values: typing.Dict[str, typing.Any] = {
            "resource": resource,
        }
        if container_name is not None:
            self._values["container_name"] = container_name
        if divisor is not None:
            self._values["divisor"] = divisor

    @builtins.property
    def resource(self) -> builtins.str:
        '''Resource to select.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#resource Env#resource}
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#container_name Env#container_name}.'''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def divisor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#divisor Env#divisor}.'''
        result = self._values.get("divisor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromResourceFieldRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromResourceFieldRefOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromResourceFieldRefOutputReference",
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

    @jsii.member(jsii_name="resetContainerName")
    def reset_container_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerName", []))

    @jsii.member(jsii_name="resetDivisor")
    def reset_divisor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDivisor", []))

    @builtins.property
    @jsii.member(jsii_name="containerNameInput")
    def container_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="divisorInput")
    def divisor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "divisorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceInput")
    def resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceInput"))

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerName"))

    @container_name.setter
    def container_name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerName", value)

    @builtins.property
    @jsii.member(jsii_name="divisor")
    def divisor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "divisor"))

    @divisor.setter
    def divisor(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "divisor", value)

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resource", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromResourceFieldRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromResourceFieldRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnvEnvValueFromResourceFieldRef],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[EnvEnvValueFromResourceFieldRef]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name", "optional": "optional"},
)
class EnvEnvValueFromSecretKeyRef:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        optional: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param key: The key of the secret to select from. Must be a valid secret key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#key Env#key}
        :param name: Name of the referent. More info: http://kubernetes.io/docs/user-guide/identifiers#names. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param optional: Specify whether the Secret or its key must be defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#optional Env#optional}
        '''
        if __debug__:
            def stub(
                *,
                key: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                optional: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if name is not None:
            self._values["name"] = name
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The key of the secret to select from. Must be a valid secret key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#key Env#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the referent. More info: http://kubernetes.io/docs/user-guide/identifiers#names.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Specify whether the Secret or its key must be defined.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#optional Env#optional}
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvEnvValueFromSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvEnvValueFromSecretKeyRefOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvEnvValueFromSecretKeyRefOutputReference",
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

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOptional")
    def reset_optional(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptional", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionalInput")
    def optional_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "optionalInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

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
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "optional"))

    @optional.setter
    def optional(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optional", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvEnvValueFromSecretKeyRef]:
        return typing.cast(typing.Optional[EnvEnvValueFromSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EnvEnvValueFromSecretKeyRef],
    ) -> None:
        if __debug__:
            def stub(value: typing.Optional[EnvEnvValueFromSecretKeyRef]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-kubernetes.env.EnvMetadata",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class EnvMetadata:
    def __init__(
        self,
        *,
        name: builtins.str,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The name of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        :param namespace: The namespace of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#namespace Env#namespace}
        '''
        if __debug__:
            def stub(
                *,
                name: builtins.str,
                namespace: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#name Env#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/kubernetes/r/env#namespace Env#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvMetadataOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-kubernetes.env.EnvMetadataOutputReference",
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

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

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
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EnvMetadata]:
        return typing.cast(typing.Optional[EnvMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EnvMetadata]) -> None:
        if __debug__:
            def stub(value: typing.Optional[EnvMetadata]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Env",
    "EnvConfig",
    "EnvEnv",
    "EnvEnvList",
    "EnvEnvOutputReference",
    "EnvEnvValueFrom",
    "EnvEnvValueFromConfigMapKeyRef",
    "EnvEnvValueFromConfigMapKeyRefOutputReference",
    "EnvEnvValueFromFieldRef",
    "EnvEnvValueFromFieldRefOutputReference",
    "EnvEnvValueFromOutputReference",
    "EnvEnvValueFromResourceFieldRef",
    "EnvEnvValueFromResourceFieldRefOutputReference",
    "EnvEnvValueFromSecretKeyRef",
    "EnvEnvValueFromSecretKeyRefOutputReference",
    "EnvMetadata",
    "EnvMetadataOutputReference",
]

publication.publish()
