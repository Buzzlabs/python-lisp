import common
import pathlib
import inspect
import importlib
from dataclasses import dataclass, is_dataclass
from typing import get_type_hints

class ProtoMeta(type):
    """
    Usage:

    class MyService(metaclass=ProtoMeta,
                    use="generate",
                    path="file.proto"):
        ...
    """

    def __new__(mcls, name, bases, namespace, *, use, path):
        if use not in {"generate", "existing"}:
            raise ValueError("use must be 'generate' or 'existing'")

        proto_path = pathlib.Path(path)

        # Create the initial class first (so nested dataclasses are real)
        cls = super().__new__(mcls, name, bases, dict(namespace))

        if use == "generate":

            # Collect nested dataclasses
            message_classes = [
                obj for obj in namespace.values()
                if isinstance(obj, type) and is_dataclass(obj)
            ]

            # Collect RPC methods via type annotations
            rpcs = []

            for attr_name, attr_value in namespace.items():
                if not callable(attr_value):
                    continue

                hints = get_type_hints(attr_value)
                if "return" not in hints:
                    continue

                param_types = [
                    t for k, t in hints.items() if k != "return"
                ]

                if not param_types:
                    continue

                request_type = param_types[0].__name__
                response_type = hints["return"].__name__

                rpcs.append((attr_name, request_type, response_type))

            content = common.proto_template(
                name,
                proto_path.stem,
                message_classes,
                rpcs
            )

            common.generate_proto(path, content)

        if use == "existing":
            if not proto_path.exists():
                raise ValueError(f"Proto file does not exist: {path}")

        result = common.generate_python(path)
        if result.returncode != 0:
            raise RuntimeError("Could not generate Python files.")

        module_name = proto_path.stem + "_pb2"
        grpc_module_name = proto_path.stem + "_pb2_grpc"

        pb2 = importlib.import_module(module_name)
        pb2_grpc = importlib.import_module(grpc_module_name)

        servicer_name = name + "Servicer"
        superclass = getattr(pb2_grpc, servicer_name)

        # Create final service class inheriting from generated Servicer
        final_cls = super().__new__(
            mcls,
            name,
            (superclass,),
            dict(cls.__dict__)
        )

        # Inject generated message classes
        for attr in dir(pb2):
            obj = getattr(pb2, attr)
            if isinstance(obj, type):
                setattr(final_cls, attr, obj)

        return final_cls

class Dismisser(
    metaclass=ProtoMeta,
    use="generate",
    path="goodbyeworld.proto"
):

    @dataclass
    class GoodbyeRequest:
        name: str

    @dataclass
    class GoodbyeReply:
        message: str

    def SayGoodbye(
        self,
        request: GoodbyeRequest,
        context
    ) -> GoodbyeReply:
        return self.GoodbyeReply(
            message=f"Goodbye, {request.name}!"
        )

print("\n--- Verification ---")

print("Base classes:")
print(Dismisser.__bases__)  # Should include DismisserServicer

print("\nInjected message classes:")
print("Has GoodbyeRequest:", hasattr(Dismisser, "GoodbyeRequest"))
print("Has GoodbyeReply:", hasattr(Dismisser, "GoodbyeReply"))

print("\nTesting method call:")
service = Dismisser()
req = service.GoodbyeRequest(name="Alice")
res = service.SayGoodbye(req, None)
print("Response:", res.message)

print("\nCheck that proto file exists:")
print(pathlib.Path("goodbyeworld.proto").exists())
