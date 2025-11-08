import json

def schema_to_json(key, schema):
    schema = schema.copy()
    type = schema.get('type', 'string')
    required = schema.get('required', False)
    if 'required' in schema:
        del schema['required']
    if 'coerce' in schema:
        del schema['coerce']
    if 'dependencies' in schema:
        schema['dependencies'] = {
            'anyOf': schema['dependencies']
        }
    if type == 'dict':
        schema['type'] = 'object'
        if 'default' in schema:
            del schema['default']
        schema['additionalProperties'] = False
        schema['properties'] = {}
        required_fields = []
        if 'schema' in schema:
            for k, v in schema['schema'].items():
                r, j = schema_to_json(k, v)
                if r:
                    required_fields.append(k)
                schema['properties'][k] = j
            del schema['schema']
        if required_fields:
            schema['required'] = required_fields
        return required, schema
    elif type == 'list':
        schema['type'] = 'array'
        if 'schema' in schema:
            schema['items'] = {}
            if 'type' in schema['schema']:
                schema['items']['type'] = [schema['schema']['type']]
            elif 'anyof_type' in schema['schema']:
                schema['items']['type'] = schema['schema']['anyof_type']
            del schema['schema']
        if 'maxlength' in schema:
            schema['maxLength'] = schema['maxlength']
            del schema['maxlength']
        return required, schema
    elif type in ['string', 'integer', 'float']:
        if type == 'float':
            schema['type'] = 'number'
        if 'regex' in schema:
            schema['pattern'] = schema['regex']
            del schema['regex']
        if 'allowed' in schema:
            schema['enum'] = schema['allowed']
            del schema['allowed']
        return required, schema
    elif type == 'boolean':
        schema['type'] = ['boolean', 'string']
        schema['enum'] = ['yes', 'no', True, False]
        return required, schema
    elif isinstance(type, list):
        schema['anyOf'] = []
        for t in type:
            schema['anyOf'].append({ 'type': t })
        del schema['type']
        return required, schema


if __name__ == "__main__":
    import argparse
    import ecmcYamlSchema
    parser = argparse.ArgumentParser(description='Generate JSON schema from ecmcYamlSchema')
    parser.add_argument('--output', '-o', type=str, help='Output file (default: stdout)', default=None)
    args = parser.parse_args()

    schema_json = {
        "$schema": "https://json-schema.org/draft-07/schema",
        "title": "ecmcAxis",
        "description": "An ecmc axis object",
        "type": "object",
        "additionalProperties": False,
        "properties": {},
        "required": [],
        "if": {
            "properties": {
                "axis": {
                    "properties": {
                        "type": { "enum": list(k for k,v in ecmcYamlSchema.supportedAxisTypes.items() if v == 2) }
                    }
                }
            }
        },
        "then": {
            "not": {
                "required": ["drive", "controller"]
            }
        }
    }
    for key, value in ecmcYamlSchema.Schema.grandSchema.items():
        # obsolted?
        if key == 'axisPlc' or key == 'homing':
            continue
        req, j = schema_to_json(key, value)
        if req:
            schema_json['required'].append(key)
        if key == 'var':
            j['additionalProperties'] = True
        schema_json['properties'][key] = j

    # The python schema use "coerce" field to convert string to integer.
    # Here we have to deal it manually.
    axis_type = schema_json['properties']['axis']['properties']['type']
    axis_type['type'] = ['string', 'integer']
    axis_type_opt = []
    axis_type_opt += list(ecmcYamlSchema.supportedAxisTypes.keys())
    axis_type_opt += set(ecmcYamlSchema.supportedAxisTypes.values())
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(schema_json, f, indent=2)
    else:
        print(json.dumps(schema_json, indent=2))
