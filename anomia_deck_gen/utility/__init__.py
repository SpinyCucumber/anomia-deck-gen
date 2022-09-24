from typing import TypeVar, Generic, Dict, Callable

T = TypeVar("T")

class InvalidExtensionException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SingleDispatchLoader(Generic[T]):

    registry: Dict[str, Callable[[str], T]] = {}
    
    def register(self, ext: str):
        def wrapper(to_wrap):
            self.registry[ext] = to_wrap
            return to_wrap
        return wrapper

    def __call__(self, path: str) -> T:
        ext = path.split(".")[-1]
        loader = self.registry.get(ext, None)
        if loader == None:
            raise InvalidExtensionException(f"Invalid extension: \"{ext}\"")
        return loader(path)

__all__ = [
    "SingleDispatchLoader",
]