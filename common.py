import subprocess
import pathlib
from dataclasses import fields

PROTO_TYPE_MAP = {
    str: "string",
    int: "int32",
    float: "double",
    bool: "bool",
}

def generate_python(path: str):
    p = pathlib.Path(path)
    return subprocess.run([
        "python3", "-m", "grpc_tools.protoc",
        f"-I{p.parent}",
        "--python_out=.",
        "--pyi_out=.",
        "--grpc_python_out=.",
        path
    ])

def generate_proto(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)

def proto_message_from_dataclass(cls):
    body = ""
    for i, field in enumerate(fields(cls), start=1):
        py_type = field.type
        proto_type = PROTO_TYPE_MAP.get(py_type, py_type.__name__)
        body += f"    {proto_type} {field.name} = {i};\n"

    return f"message {cls.__name__} {{\n{body}}}\n\n"

def proto_rpc(name, request_type, response_type):
    return f"    rpc {name} ({request_type}) returns ({response_type}) {{}}\n"

def proto_template(service_name, package, message_classes, rpcs):
    msg_text = "".join(
        proto_message_from_dataclass(m)
        for m in message_classes
    )

    rpc_text = "".join(proto_rpc(*rpc) for rpc in rpcs)

    return (
        'syntax = "proto3";\n'
        f"package {package};\n\n"
        f"{msg_text}"
        f"service {service_name} {{\n"
        f"{rpc_text}"
        "}\n"
    )
