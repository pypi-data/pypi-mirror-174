import importlib.resources
import json
import uuid
from pathlib import Path
from string import Formatter
from types import ModuleType
from typing import Dict, Set, Union

import yaml

from atc.singleton import Singleton

from ..atc_exceptions import AtcException


class NoSuchPropertyException(AtcException):
    pass


# recursive type definition of the details object
TcDetails = Dict[str, Union[str, "TcDetails"]]


class TableConfigurator(metaclass=Singleton):
    _unique_id: str
    _raw_resource_details: Dict[str, TcDetails]
    _is_debug: bool
    _extra_config: Dict[str, str]

    # this dict contains all details for all resources
    table_details: Dict[str, str]

    def __init__(self, resource_path: Union[str, ModuleType] = None):
        self._unique_id = uuid.uuid4().hex
        self.clear_all_configurations()

        if resource_path:
            self.add_resource_path(resource_path)

    def clear_all_configurations(self):
        self._raw_resource_details = dict()
        self._extra_config = dict()
        self._is_debug = False
        self.table_details = dict()

    ############################################
    # the core logic of this class is contained
    # in the following methods
    ############################################

    def get_extra_details(self) -> Dict[str, str]:
        """get all special substitutions not based on resources"""
        extras = {
            "ID": f"__{self._unique_id}" if self._is_debug else "",
            "MNT": "tmp" if self._is_debug else "mnt",
        }
        extras.update(self._extra_config)
        return extras

    def _get_item(self, table_id: str) -> Dict[str, str]:
        """item dictionary where release-debug and alias loops are resolved"""
        # this stack allows us to detect alias loop
        stack = {table_id}

        value: TcDetails = self._raw_resource_details[table_id]

        while set(value.keys()) in [{"release", "debug"}, {"alias"}]:
            if set(value.keys()) == {"release", "debug"}:
                # Handle the case of differentiated release and debug tables
                if self._is_debug:
                    value = value["debug"]
                else:
                    value = value["release"]

            if set(value.keys()) == {"alias"}:  # allow alias of alias
                new_id = value["alias"]
                if new_id in stack:
                    raise ValueError(f"Alias loop at key {new_id}")
                stack.add(new_id)
                value = self._raw_resource_details[new_id]

        # we are finished resolving a possible route of aliases
        return value

    def _get_unsubstituted_item_property(self, table_id: str, property: str) -> str:
        """item property where release-debug and alias loops are resolved"""
        value = self._get_item(table_id)

        if property in value:
            return value[property]
        else:
            raise NoSuchPropertyException(property)

    def _get_item_property(
        self, table_id: str, property: str, _forbidden_keys: Set[str] = None
    ) -> str:
        """Get the full item property, fully resolved and substituted."""
        raw_string = self._get_unsubstituted_item_property(table_id, property)

        # some items are not strings, then the rest of this function makes no sense
        if not isinstance(raw_string, str):
            return raw_string

        replacements = self.get_extra_details()
        # get all keys used in the raw_string, such as using {MyDb} will get "MyDb"
        format_keys = [i[1] for i in Formatter().parse(raw_string) if i[1] is not None]
        # subtract all extra keys from the set, e.g. take out "ENV"
        other_resource_keys = set(format_keys) - set(replacements.keys())

        # the forbidden-keys logic allows us to detect reference loops.
        # no key that is in the upstream of a property is allowed in the string
        # substitutions of this property.
        _forbidden_keys = _forbidden_keys or set()
        _forbidden_keys.add(f"{table_id}_{property}")
        if property == "name":
            _forbidden_keys.add(table_id)
        if any(key in _forbidden_keys for key in other_resource_keys):
            raise ValueError(
                f"Substitution loop at table {table_id} property {property}"
            )

        # every key that is not in the special properties and not forbidden
        # should refer to another resource. If it does not an exception will occur.
        for key in other_resource_keys:
            try:
                # maybe we have a case of reference to property, let's try:

                id_part, property_part = key.rsplit("_", 1)
                # will raise ValueError if there are too few parts

                value = self._get_item_property(id_part, property_part, _forbidden_keys)
                # raises ValueError if it does not exist

                replacements[key] = value
                continue
            except ValueError:
                pass

            # bare key references are to 'name' which _must_ exist in this case
            replacements[key] = self._get_item_property(key, "name", _forbidden_keys)

        return raw_string.format(**replacements)

    def add_resource_path(self, resource_path: Union[str, ModuleType]) -> None:
        backup_details = self._raw_resource_details.copy()
        try:
            for file_name in importlib.resources.contents(resource_path):
                extension = Path(file_name).suffix
                if extension in [".json", ".yaml", ".yml"]:
                    with importlib.resources.path(
                        resource_path, file_name
                    ) as file_path:
                        with open(file_path) as file:
                            update = (
                                json.load(file)
                                if extension == ".json"
                                else yaml.load(file, Loader=yaml.FullLoader)
                            )
                            if not isinstance(update, dict):
                                raise ValueError(f"document in {file_path} is no dict.")

                            for key, value in update.items():
                                if not isinstance(value, dict):
                                    raise ValueError(
                                        f"value {key} in {file_path} is no dict."
                                    )
                                self._raw_resource_details[key] = value

            # try re-building all details
            self.table_details = dict()
            self.get_all_details()
        except:  # noqa: E722  we re-raise the exception, so bare except is ok.
            # this piece makes it so that the TableConfigurator can still be used
            # if any exception raised by the above code is caught.
            self._raw_resource_details = backup_details
            raise

    ############################################
    # all methods below are interface and convenience methods
    ############################################

    def set_extra(self, **kwargs: str):
        """Add extra replacement keys for your resources.
        for example call .set_extra(ENV='prod')"""
        self._extra_config.update(kwargs)
        self.table_details = dict()

    def set_debug(self):
        """Select debug tables. {ID} will be replaced with a guid"""
        self.reset(debug=True)

    def set_prod(self):
        """Select production tables. {ID} will be replaced with a empty string"""
        self.reset(debug=False)

    def __reset(self, debug: bool) -> None:
        self._is_debug = debug
        self.table_details = dict()

    def reset(self, *, debug: bool = False):
        """
        Resets table names and table SQL. Enables or disables debug mode
        (used for unit tests and integration tests).
        :param debug: False -> release tables, True -> debug tables.
        :param kwargs: additional keys to be substituted in names and paths
        """
        self.__reset(debug)

    def is_debug(self):
        """
        Return True if table names and table SQL specify debug table,
        False if release tables
        """
        return self._is_debug

    def get_unique_id_length(self):
        """
        Return the character length of the UUID identifier inserted into
        names with the {ID} tag
        """
        return len(self._unique_id)

    def register(self, key: str, value: TcDetails):
        """
        Register a new table.
        """
        if not isinstance(value, dict):
            raise ValueError("value is no dict")
        self._raw_resource_details[key] = value
        self.table_details = dict()

    def table_property(
        self, table_id: str, property_name: str, default_value: str = None
    ):
        """
        Return the table property (e.g. name, path, format, etc.)
            for the specified table id.
        :param table_id: Table id in the .json or .yaml files.
        :param property_name: Name of the property to read (e.g. "name", "path", etc.)
        :param default_value: Optional default value of the property
            if the property is missing.
        :return: str: property value
        """
        property_value = self.get_all_details().get(
            f"{table_id}_{property_name}", default_value
        )

        if property_value is None:
            raise ValueError(
                f"property '{property_name}' for table identifier '{table_id}' is empty"
            )
        return property_value

    def table_name(self, table_id: str):
        """
        Return the table name for the specified table id.
        :param table_id: Table id in the .json or .yaml files.
        :return: str: table name
        """
        return self.table_property(table_id, "name")

    def table_path(self, table_id: str):
        """
        Return the table path for the specified table id.
        :param table_id: Table id in the .json or .yaml files.
        :return: str: table path
        """
        return self.table_property(table_id, "path")

    def get_all_details(self):
        """
        Return a dictionary containing every resource detail fully resolved.
        e.g. a resource that looks like this:
        MyTableDetail:
            name: mytablename
            path: my/table/path
        will appear with three keys:
            - "MyTableDetail"
            - "MyTableDetail_name"
            - "MyTableDetail_path"
        all substitutions will be fully resolved.
        """
        if not self.table_details:
            self.table_details = dict()

            for table_id in self._raw_resource_details.keys():
                # add the name as the bare key
                try:
                    self.table_details[table_id] = self._get_item_property(
                        table_id, "name"
                    )
                except NoSuchPropertyException:
                    pass

                # add every propety as a _property part
                for property_name in set(self._get_item(table_id).keys()):
                    try:
                        self.table_details[
                            f"{table_id}_{property_name}"
                        ] = self._get_item_property(table_id, property_name)
                    except NoSuchPropertyException:
                        pass

        return self.table_details
