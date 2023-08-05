from pathlib import Path
import yaml


version = '22.0.1'


def to_str(
    data: any,
) -> str:
    try:
        return yaml.dump(
            data,
            Dumper = yaml.CDumper,
        )
    except AttributeError:
        return yaml.dump(
            data,
            Dumper = yaml.Dumper,
        )



def to_file(
    data: any,
    file_path: str | Path,
) -> None:
    Path(file_path).parent.mkdir(
        exist_ok = True,
        parents = True,
    )
    with open(
        file_path,
        'w'
    ) as file:
        file.write(
            to_str(
                data,
            )
        )


def read_str(
    data: str,
) -> any:
    try:
        return yaml.load(
            data,
            Loader = yaml.CLoader,
        )
    except AttributeError:
        return yaml.load(
            data,
            Loader = yaml.Loader,
        )


def read_file(
    file_path: str | Path
):
    with open(
        file_path,
        'r',
    ) as file:
        return read_str(
            file
        )
