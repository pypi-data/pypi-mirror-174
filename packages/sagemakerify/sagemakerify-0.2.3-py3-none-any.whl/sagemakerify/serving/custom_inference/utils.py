import os
import json
import pickle
import tarfile
import pandas as pd
from io import BytesIO


def _load_file(file):
    def load(filename, f):
        basename = os.path.basename(filename)
        if basename.endswith(".csv"):
            return pd.read_csv(BytesIO(f.read()))
        elif basename.endswith(".csv.gzip") or basename.endswith(".csv.gz"):
            return pd.read_csv(BytesIO(f.read()), compression="gzip")
        elif basename.endswith(".json") or basename.endswith(".data"):
            return json.load(f)
        elif (
            basename.endswith(".parquet")
            or basename.endswith(".parquet.gzip")
            or basename.endswith(".parquet.gz")
        ):
            return pd.read_parquet(BytesIO(f.read()))
        else:
            return pickle.load(f)

    if os.path.basename(file).endswith(".tar.gz"):
        with tarfile.open(file, "r:gz") as tar:
            filename = tar.getnames()[0]
            f = tar.extractfile(filename)
            return load(filename, f)
    else:
        with open(file, "rb") as f:
            return load(file, f)


def load_model_files(model_dir):
    output_prefix = "output_"
    ids = [
        int(dir.replace(output_prefix, ""))
        for dir in os.listdir(model_dir)
        if dir.startswith(output_prefix)
    ]
    ids.sort()

    elements = []
    for id in ids:
        output_path = os.path.join(model_dir, f"{output_prefix}{id}")
        output_data_filename = os.path.join(output_path, f"{output_prefix}{id}.data")
        files = os.listdir(output_path)

        if os.path.isfile(output_data_filename):
            output_data = _load_file(output_data_filename)
            elements.append(output_data["value"])
        else:
            elements.append(_load_file(os.path.join(output_path, files[0])))

    return tuple(elements)
