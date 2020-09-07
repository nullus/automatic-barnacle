from pathlib import Path
from typing import List, Optional, Tuple, Union


class Local:
    """
    Manage local filesystem directory for metadata

    Will search parent directories for .barnacles/ and create it in current
    working directory otherwise
    """

    directory_name = '.barnacles'

    def __init__(self) -> None:
        super().__init__()
        self._path = self.search(from_=Path().absolute())
        if self._path is None:
            self._path = Path(self.directory_name).absolute()
            # Will raise if any issues are encountered
            self._path.mkdir()

    @property
    def root(self):
        return self._path.parent

    def path(self, to: Union[List[str], Tuple[str]] = ()) -> Path:
        return self._path.joinpath(*to)

    def uri(self, to: Union[List[str], Tuple[str]] = ()) -> str:
        return self.path(to).as_uri()

    @classmethod
    def search(cls, from_: Path) -> Optional[Path]:
        path = from_.joinpath(cls.directory_name)
        if path.is_dir():
            return path
        else:
            if from_.parent == from_:
                # Terminate search once root (relative or absolute) is reached
                return None
            else:
                return cls.search(from_.parent)
