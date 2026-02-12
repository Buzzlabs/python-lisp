import common
import pathlib
import inspect
import importlib
from dataclasses import is_dataclass, fields
from typing import get_type_hints

def defproto(*, use: str, path: str):
    """
    use="generate"  -> generate proto from nested dataclasses
    use="existing"  -> use existing proto file
    """

    if use not in {"generate", "existing"}:
        raise ValueError("use must be 'generate' or 'existing'")

    def decorator(cls):
        proto_path = pathlib.Path(path)

        if use == "generate":

            # Collect nested dataclasses
            message_classes = [
                obj for obj in cls.__dict__.values()
                if isinstance(obj, type) and is_dataclass(obj)
            ]

            # Collect RPC methods via type annotations
            rpcs = []

            for name, fn in inspect.getmembers(cls, inspect.isfunction):
                hints = get_type_hints(fn)

                if "return" not in hints:
                    continue

                # Expect: def Method(self, request: RequestType, context) -> ResponseType
                params = list(hints.items())

                # Skip "return" entry
                param_types = [
                    t for k, t in hints.items() if k != "return"
                ]

                if len(param_types) < 1:
                    continue

                request_type = param_types[0].__name__
                response_type = hints["return"].__name__

                rpcs.append((name, request_type, response_type))

            content = proto_template(
                cls.__name__,
                proto_path.stem,
                message_classes,
                rpcs
            )

            generate_proto(path, content)

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

        servicer_name = cls.__name__ + "Servicer"
        superclass = getattr(pb2_grpc, servicer_name)

        # Create final service class
        new_cls = type(
            cls.__name__,
            (superclass,),
            dict(cls.__dict__)
        )

        # Inject generated message classes
        for attr in dir(pb2):
            obj = getattr(pb2, attr)
            if isinstance(obj, type):
                setattr(new_cls, attr, obj)

        return new_cls

    return decorator

@defproto(use="existing", path="../protos/helloworld.proto")
class Greeter:

    def SayHello(self, request, context):
        return self.HelloReply(
            message=f"Hello, {request.name}!"
        )

print("\n--- Verification (Greeter / Decorator / Existing Mode) ---")

print("Base classes:")
print(Greeter.__bases__)  # Should include GreeterServicer

print("\nInjected message classes:")
print("Has HelloRequest:", hasattr(Greeter, "HelloRequest"))
print("Has HelloReply:", hasattr(Greeter, "HelloReply"))

print("\nTesting method call:")
service = Greeter()
req = service.HelloRequest(name="Alice")
res = service.SayHello(req, None)
print("Response:", res.message)

print("\nCheck that generated files exist:")
print(pathlib.Path("helloworld_pb2.py").exists())
print(pathlib.Path("helloworld_pb2_grpc.py").exists())
