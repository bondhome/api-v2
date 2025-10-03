#!/usr/bin/env python3
import sys
import yaml
import json
from pathlib import Path
from openapi_spec_validator import openapi_v30_spec_validator, openapi_v31_spec_validator

def resolve_json_pointer(obj, pointer):
    """Resolve a JSON pointer like '/description' or '/schemas/User'"""
    if not pointer or pointer == '#':
        return obj
    if pointer.startswith('#/'):
        pointer = pointer[2:]
    parts = pointer.split('/')
    result = obj
    for part in parts:
        if isinstance(result, dict):
            if part not in result:
                raise KeyError(f"'{part}' does not exist in keys: {list(result.keys())}")
            result = result[part]
        elif isinstance(result, list):
            result = result[int(part)]
        else:
            raise ValueError(f"Cannot resolve pointer {pointer}")
    return result

def resolve_refs(obj, base_path, file_cache=None):
    """Recursively resolve $ref references in a dict/list"""
    if file_cache is None:
        file_cache = {}

    if isinstance(obj, dict):
        if '$ref' in obj and len(obj) == 1:
            # This is a reference object
            ref_str = obj['$ref']

            if ref_str.startswith('#/'):
                # Internal reference - can't resolve here, let validator handle it
                return obj
            elif '#/' in ref_str:
                # External file reference with JSON pointer
                file_part, pointer_part = ref_str.split('#/', 1)
                ref_file = base_path / file_part

                # Cache file contents to avoid re-reading
                cache_key = str(ref_file.resolve())
                if cache_key not in file_cache:
                    with open(ref_file, 'r') as f:
                        file_cache[cache_key] = yaml.safe_load(f)

                ref_content = file_cache[cache_key]
                # Resolve the JSON pointer
                resolved = resolve_json_pointer(ref_content, pointer_part)
                return resolve_refs(resolved, ref_file.parent, file_cache)
            else:
                # External file reference without pointer
                ref_file = base_path / ref_str
                cache_key = str(ref_file.resolve())
                if cache_key not in file_cache:
                    with open(ref_file, 'r') as f:
                        file_cache[cache_key] = yaml.safe_load(f)
                ref_content = file_cache[cache_key]
                return resolve_refs(ref_content, ref_file.parent, file_cache)
        else:
            # Regular dict - recurse into values
            return {k: resolve_refs(v, base_path, file_cache) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve_refs(item, base_path, file_cache) for item in obj]
    else:
        return obj

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_with_refs.py <spec_file>")
        sys.exit(1)

    spec_file = Path(sys.argv[1])

    try:
        # Load the spec
        with open(spec_file, 'r') as f:
            spec_dict = yaml.safe_load(f)

        # Resolve all external file references
        spec_dict = resolve_refs(spec_dict, spec_file.parent)

        # Detect version
        openapi_version = spec_dict.get('openapi', spec_dict.get('swagger', ''))

        if openapi_version.startswith('3.0'):
            validator = openapi_v30_spec_validator
        elif openapi_version.startswith('3.1'):
            validator = openapi_v31_spec_validator
        else:
            raise ValueError(f"Unsupported OpenAPI version: {openapi_version}")

        # DEBUG: Save resolved spec for inspection
        # with open('/tmp/resolved_spec.json', 'w') as f:
        #     json.dump(spec_dict, f, indent=2)

        # Validate the spec
        validator.validate(spec_dict)
        print(f"{spec_file}: OK")

    except Exception as e:
        print(f"{spec_file}: Validation Error:", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
