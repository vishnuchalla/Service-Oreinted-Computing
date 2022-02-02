from protocheck.bspl import load_file, model, strip_latex, load_protocols
from protocheck.verification import paths, refinement
import fire
import json
from .commands import Commands, register_commands
from . import node_red


def handle_projection(role_name, *files, filter=".*", verbose=False):
    """
    Project a protocol to the perspective of a single role

    Args:
      role_name: The name of the role to project the protocols to
      files: Paths to the specification files, each containing one or more protocols
      filter: A regular expression to select a subset of protocols from the specification files
      verbose: Print more detail about steps taken
      debug: Print debug information
    """
    projections = []
    for protocol in load_protocols(files, filter=filter):
        schema = protocol.schema
        if verbose:
            print(schema)

        role = protocol.roles.get(role_name)
        if not role:
            raise LookupError("Role not found", role_name)

        projections.append(protocol.projection(role))

    for p in projections:
        print(p.format())


def handle_json(*files, indent=4):
    """
    Print a JSON representation of each protocol

    Args:
      files: Paths to specification files, each containing one or more protocols
      indent: How many spaces to indent each level of the JSON structure
    """
    for protocol in load_protocols(files):
        print(json.dumps(protocol.to_dict(), indent=indent))


def handle_ast(path, indent=2):
    """
    Print the parsed AST for the specification in PATH

    Args:
      path: The path for the specification file, containing one or more protocols
      indent: How many spaces to indent each level of the AST
    """
    with open(path) as file:
        raw = file.read()
        raw = strip_latex(raw)

        spec = model.parse(raw, rule_name="document")

        def remove_parseinfo(d):
            if not isinstance(d, (dict, list)):
                return d
            if isinstance(d, list):
                return [remove_parseinfo(v) for v in d]
            return {
                k: remove_parseinfo(v) for k, v in d.items() if k not in {"parseinfo"}
            }

        for p in spec:
            print(json.dumps(remove_parseinfo(p.asjson()), indent=indent))


def check_syntax(*files, quiet=False, debug=False):
    """
    Parse each file, printing any syntax errors found

    Args:
      quiet: Don't output anything for correct files
      debug: Print stack trace for errors
    """
    for f in files:
        if not quiet:
            print(f"{f}:")
        try:
            load_file(f)
        except Exception as e:
            if debug:
                raise e
            if quiet:
                print(f"{f}:")
            print(f"  {e}")
        else:
            if not quiet:
                print("  Syntax: correct")


register_commands(
    {
        "ast": handle_ast,
        "json": handle_json,
        "check-syntax": check_syntax,
        "load-file": load_file,
    }
)


def main():
    fire.Fire(Commands, name="bspl")


if __name__ == "__main__":
    main()
