from typing import TypeVar, Generic, Dict, Callable

T = TypeVar("T")

class SingleDispatchLoader(Generic[T]):

    registry: Dict[str, Callable[[str], T | None]] = {}
    
    def register(self, ext: str):
        def wrapper(to_wrap):
            self.registry[ext] = to_wrap
            return to_wrap
        return wrapper

    def __call__(self, path: str) -> T | None:
        ext = path.split(".")[-1]
        loader = self.registry.get(ext)
        if loader:
            return loader(path)

__all__ = [
    "Loader",
    "SingleDispatchLoader",
]