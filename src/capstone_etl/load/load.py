import os
import pandas as pd

OUTPUT_DIR = "data/processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_dataframe(df: pd.DataFrame, filename: str) -> None:
    """
    Persist final transformed dataset to disk.

    Parameters
    ----------
    df : pd.DataFrame
        Clean engineered dataset from transform stage.
    filename : str
        Output filename to write (csv format).
    """

    path = os.path.join(OUTPUT_DIR, filename)

    df.to_csv(path, index=False)

    # Basic validation
    if not os.path.exists(path):
        raise RuntimeError("Load failed: output file was not written")

    if os.path.getsize(path) == 0:
        raise RuntimeError("Load failed: output file is empty")

    print(f"✅ Dataset successfully loaded to {path}")
