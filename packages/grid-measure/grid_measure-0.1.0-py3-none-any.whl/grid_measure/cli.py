from pathlib import Path
from cloup import command, help_option, version_option, option, Path as PathType
from . import __version__


@command("grid_measure", help="Measure scale of a grid paper.")
@help_option("-h", "--help")
@version_option(
    __version__,
    "-v",
    "--version",
)
@option(
    "-i",
    "--image_dir",
    type=PathType(
        exists=True,
        file_okay=False,
        dir_okay=True,
        path_type=Path,
    ),
    help="Directory containing images to be measured.",
    required=True,
)
@option(
    "-o",
    "--out_file",
    type=PathType(
        exists=False,
        file_okay=True,
        dir_okay=False,
        path_type=Path,
    ),
    help="Output CSV file.",
    required=True,
)
def cli(image_dir: Path, out_file: Path):
    import pandas as pd
    import skimage.io
    from tqdm import tqdm
    from .defaults import IMAGE_FILE_EXTENSIONS
    from .core import get_scale_mm

    image_files = []
    for ext in IMAGE_FILE_EXTENSIONS:
        image_files.extend(list(image_dir.glob(f"[!._]*.{ext}")))

    scales_mm = []

    for img_f in tqdm(image_files):
        img = skimage.io.imread(img_f)
        try:
            scale_mm = get_scale_mm(img)
        except:
            scale_mm = None
        scales_mm.append(scale_mm)

    image_names = [f.name for f in image_files]
    df = pd.DataFrame(dict(image=image_names, px_per_mm=scales_mm))
    df.to_csv(out_file, index=False)
