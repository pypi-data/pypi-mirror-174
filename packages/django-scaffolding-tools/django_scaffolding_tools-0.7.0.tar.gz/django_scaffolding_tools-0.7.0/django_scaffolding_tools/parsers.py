import ast
import re
from operator import itemgetter
from pathlib import Path
from typing import Dict, Any, List, Callable, Tuple

import humps
from ast2json import ast2json

from django_scaffolding_tools.enums import NativeDataType, PatternType, ASTDataType


def to_snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('__([A-Z])', r'_\1', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def transform_dict_to_model_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    model_list = list()
    for key, model in data.items():
        model_list.append(model)
        for att in model['attributes']:
            if not att['native']:
                model_list += transform_dict_to_model_list(att['value'])
    return sorted(model_list, key=itemgetter('level'), reverse=True)


def parse_var_name(var_name: str) -> Tuple[str, bool]:
    """Transforms a variable to snake case from pascal and camel case."""
    if humps.is_snakecase(var_name):
        new_var_name = var_name
    elif humps.is_camelcase(var_name):
        new_var_name = humps.decamelize(var_name)
    elif humps.is_pascalcase(var_name):
        new_var_name = humps.depascalize(var_name)
    else:
        raise Exception('Unsupported casing.')
    return new_var_name, new_var_name != var_name


def parse_dict(data: Dict[str, Any], model_name: str = 'Model', level: int = 0,
               value_item_level: int = 0) -> Dict[str, Any]:
    """Parses a dictionary containing data to create a basic Model dictionary"""
    parsed_dict: dict[str, dict[Any, Any] | list[Any]] = dict()
    key_name = to_snake_case(model_name)
    parsed_dict[key_name] = dict()
    parsed_dict[key_name]['name'] = model_name
    parsed_dict[key_name]['level'] = level
    parsed_dict[key_name]['attributes'] = list()
    for key, item in data.items():
        variable_name, add_alias = parse_var_name(key)

        item_data = {'name': variable_name, 'value': item, 'supported': False, 'native': True, 'many': False}
        if add_alias:
            item_data['alias'] = key
        data_type = item.__class__.__name__
        if data_type in NativeDataType.to_list():
            item_data['data_type'] = data_type
            item_data['supported'] = True
            if data_type == NativeDataType.STRING.value:
                item_data['length'] = len(item)
        elif isinstance(item, dict):
            pascalized_model_name = humps.pascalize(key)
            item_data['data_type'] = pascalized_model_name
            item_data['value'] = parse_dict(item, model_name=pascalized_model_name, level=level + 1)
            item_data['supported'] = True
            item_data['native'] = False
        elif isinstance(item, list):
            value_item_level += 1
            for value_item in item:
                model_name = f'ValueItem{value_item_level}'
                item_data['data_type'] = model_name
                item_data['value'] = parse_dict(value_item, model_name=model_name, level=level + 1,
                                                value_item_level= value_item_level + 1)
                item_data['supported'] = True
                item_data['native'] = False
                item_data['many'] = True
        else:
            item_data['data_type'] = data_type

        parsed_dict[key_name]['attributes'].append(item_data)
    return parsed_dict


def parse_for_patterns(model_list: List[Dict[str, Any]],
                       pattern_functions: List[Callable[[str], PatternType]]) -> List[Dict[str, Any]]:
    for model in model_list:
        for attribute in model['attributes']:
            if attribute['data_type'] == NativeDataType.STRING:
                for pattern_function in pattern_functions:
                    pattern = pattern_function(attribute['value'])
                    if pattern is not None:
                        attribute['pattern_type'] = pattern
                        break
    return model_list


SERIALIZER_FIELDS = {
    NativeDataType.STRING: {'field': 'CharField'},
    NativeDataType.INTEGER: {'field': 'IntegerField'},
    NativeDataType.FLOAT: {'field': 'FloatField'},
    NativeDataType.DATE: {'field': 'DateField'},
    NativeDataType.DATETIME: {'field': 'DatetimeField'},
    PatternType.DATE: {'field': 'DateField'},
    PatternType.DATETIME: {'field': 'DatetimeField'},
    PatternType.URL: {'field': 'UrlField'},
    PatternType.EMAIL: {'field': 'EmailField'},
}


def parse_file_for_ast_classes(filename: Path) -> Dict[str, Any]:
    with open(filename, 'r') as py_file:
        content = py_file.read()
        node = ast.parse(content)
    node_dict = ast2json(node)
    return node_dict


def parse_for_django_classes(module: Dict[str, Any]) -> Dict[str, any]:
    module_content = dict()
    django_classes = list()
    module_content['classes'] = django_classes

    for content in module['body']:
        if content.get('_type') == ASTDataType.CLASS:
            model = dict()
            model['name'] = content.get('name')
            model['attributes'] = list()
            for class_content in content['body']:
                if class_content.get('_type') == ASTDataType.ASSIGN:
                    variable = dict()
                    variable['name'] = class_content['targets'][0]['id']
                    variable['keywords'] = list()
                    try:
                        func_ = class_content['value']['func']
                        data_type = func_.get('attr')
                        if data_type is None:
                            data_type = func_.get('id')
                        variable['data_type'] = data_type
                    except KeyError:
                        print(f'With variable {variable["name"]}')
                    try:
                        for keyword in class_content['value']['keywords']:
                            keyword_data = dict()
                            keyword_data['name'] = keyword['arg']
                            value_type = keyword['value']['_type']
                            keyword_data['value_type_TMP'] = value_type

                            if value_type == ASTDataType.CONSTANT:
                                keyword_value = keyword['value'].get('value')
                            elif value_type == ASTDataType.NAME:
                                keyword_value = keyword['value'].get('id')
                            elif value_type == ASTDataType.ATTRIBUTE:
                                keyword_value = keyword['value'].get('attr')
                            elif value_type == ASTDataType.CALL and keyword_data['name'] == 'help_text':
                                if len(keyword['value'].get('args')) > 0:
                                    call_args_type = keyword['value']['args'][0]['_type']
                                    if call_args_type == ASTDataType.CONSTANT:
                                        keyword_value = keyword['value']['args'][0].get('value')

                            keyword_data['value'] = keyword_value
                            variable['keywords'].append(keyword_data)
                    except KeyError:
                        print(f'Error with variable {model["name"]}.{variable["name"]}')
                    model['attributes'].append(variable)
            django_classes.append(model)
    return module_content
