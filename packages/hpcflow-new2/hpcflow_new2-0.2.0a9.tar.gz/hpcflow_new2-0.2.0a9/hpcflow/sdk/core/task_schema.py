from dataclasses import dataclass, field
import json
from sys import implementation
from typing import List, Optional, Union

from hpcflow.sdk.core.actions import Action
from hpcflow.sdk.core.errors import MissingActionsError, TaskSchemaMissingParameterError
from hpcflow.sdk.core.json_like import ChildObjectSpec, JSONLike
from hpcflow.sdk.core.parameters import (
    Parameter,
    ParameterPropagationMode,
    SchemaInput,
    SchemaOutput,
    SchemaParameter,
)

from hpcflow.sdk.core.utils import (
    FromSpecMissingObjectError,
    check_valid_py_identifier,
)


@dataclass
class TaskObjective(JSONLike):
    name: str

    def __post_init__(self):
        self.name = check_valid_py_identifier(self.name)


class TaskSchema(JSONLike):

    # TODO: build comprehensive test suite for TaskSchema
    # - decide how schema inputs and outputs are linked to action inputs and outputs?
    # - should the appearance of parameters in the actions determined schema inputs/outputs
    #   - still need to define e.g. defaults, so makes sense to keep inputs/outputs as schema
    #     parameters, and then verify that all action parameters are taken from schema parameters.
    # - should command files be listed as part of the schema? probably, yes.
    app = None
    _validation_schema = "task_schema_spec_schema.yaml"
    _hash_value = None
    _child_objects = (
        ChildObjectSpec(name="objective", class_name="TaskObjective"),
        ChildObjectSpec(name="inputs", class_name="SchemaInput", is_multiple=True),
        ChildObjectSpec(name="outputs", class_name="SchemaOutput", is_multiple=True),
        ChildObjectSpec(name="actions", class_name="Action", is_multiple=True),
    )

    def __init__(
        self,
        objective: Union[TaskObjective, str],
        actions: List[Action],
        method: Optional[str] = None,
        implementation: Optional[str] = None,
        inputs: Optional[List[Union[Parameter, SchemaInput]]] = None,
        outputs: Optional[List[Union[Parameter, SchemaOutput]]] = None,
        version: Optional[str] = None,
        _hash_value: Optional[str] = None,
    ):
        self.objective = objective
        self.actions = actions
        self.method = method
        self.implementation = implementation
        self.inputs = inputs or []
        self.outputs = outputs or []
        self._hash_value = _hash_value

        self._validate()
        self.version = version

        # if version is not None:  # TODO: this seems fragile
        #     self.assign_versions(
        #         version=version,
        #         app_data_obj_list=self.app.task_schemas
        #         if self.app.is_data_files_loaded
        #         else [],
        #     )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"objective={self.objective.name!r}, "
            f"input_types={self.input_types!r}, "
            f"output_types={self.output_types!r}"
            f")"
        )

    def _validate(self):

        if isinstance(self.objective, str):
            self.objective = TaskObjective(self.objective)

        if self.method:
            self.method = check_valid_py_identifier(self.method)
        if self.implementation:
            self.implementation = check_valid_py_identifier(self.implementation)

        # coerce Parameters to SchemaInputs
        for idx, i in enumerate(self.inputs):
            if isinstance(i, Parameter):
                self.inputs[idx] = SchemaInput(i)

        # coerce Parameters to SchemaOutputs
        for idx, i in enumerate(self.outputs):
            if isinstance(i, Parameter):
                self.outputs[idx] = SchemaOutput(i)

        # TEMP: maybe don't need this check? Could be useful for testing to allow no actions?
        # if not self.actions:
        #     raise MissingActionsError("A task schema must define at least one Action.")

    @property
    def name(self):
        out = (
            f"{self.objective.name}"
            f"{f'_{self.method}' if self.method else ''}"
            f"{f'_{self.implementation}' if self.implementation else ''}"
        )
        return out

    @property
    def input_types(self):
        return tuple(i.typ for i in self.inputs)

    @property
    def output_types(self):
        return tuple(i.typ for i in self.outputs)

    @property
    def provides_parameters(self):
        return tuple(
            i
            for i in self.inputs + self.outputs
            if i.propagation_mode != ParameterPropagationMode.NEVER
        )

    @classmethod
    def get_by_key(cls, key):
        """Get a config-loaded task schema from a key."""
        return cls.app.task_schemas[key]

    def get_parameter_dependence(self, parameter: SchemaParameter):
        """Find if/where a given parameter is used by the schema's actions."""
        out = {"input_file_writers": [], "commands": []}
        for act_idx, action in enumerate(self.actions):
            deps = action.get_parameter_dependence(parameter)
            for key in out:
                out[key].extend((act_idx, i) for i in deps[key])
        return out

    def get_key(self):
        return (str(self.objective), self.method, self.implementation)
