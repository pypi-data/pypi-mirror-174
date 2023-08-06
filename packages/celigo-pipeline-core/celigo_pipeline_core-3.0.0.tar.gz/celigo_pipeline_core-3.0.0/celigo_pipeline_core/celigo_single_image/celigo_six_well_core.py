import importlib.resources as pkg_resources
import os
from pathlib import Path
import pwd
import shutil
import subprocess

from aics_pipeline_uploaders import CeligoUploader
from jinja2 import Environment, PackageLoader
from lkaccess import LabKey, QueryFilter, contexts
import pandas as pd

from .. import pipelines
from ..postgres_db_functions import add_to_table
from .celigo_image import CeligoImage


class CeligoSixWellCore(CeligoImage):
    """This Class provides utility functions for the Celigo
    pipeline to prepare single celigo images.

    """

    def __init__(
        self, raw_image_path: str, env: str = "stg", working_dir: str = ""
    ) -> None:
        """Constructor.

        Parameters
        ----------
        raw_image_path : str
            Raw celigo image path. This path is used to copy a version of the image to SLURM for
            processing.
        """

        # Directory Name, used to create working directory.
        self.env = env
        self.tempdirname = Path(raw_image_path).with_suffix("").name
        if self.env == "prod":
            self.lk = LabKey(server_context=contexts.PROD)
        elif self.env == "stg":
            self.lk = LabKey(server_context=contexts.STAGE)
        else:
            raise Exception("Not a valid env. Must be [prod, stg]")

        # Working Directory Creation
        if working_dir == "":
            if not os.path.exists(
                f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}"
            ):
                os.mkdir(f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}")
            self.working_dir = Path(
                f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}"
            )
        else:
            if not os.path.exists(f"{working_dir}/{self.tempdirname}"):
                os.mkdir(f"{working_dir}/{self.tempdirname}")
            self.working_dir = Path(f"{working_dir}/{self.tempdirname}")

        # Copying Image to working directory.
        self.raw_image_path = Path(raw_image_path)
        shutil.copyfile(
            self.raw_image_path, f"{self.working_dir}/{self.raw_image_path.name}"
        )
        self.image_path = Path(f"{self.working_dir}/{self.raw_image_path.name}")

        # Creating pipeline paths for templates
        with pkg_resources.path(
            pipelines, "6_well_rescaleandcrop_cellprofilerpipeline_v2.0.cppipe"
        ) as p:
            self.rescale_pipeline_path = p
        with pkg_resources.path(
            pipelines, "6_well_confluency_cellprofilerpipeline_v2.1.cppipe"
        ) as p:
            self.cellprofiler_pipeline_path = p

    def downsample(self):
        """downsample raw images for higher processing speed and streamlining of
        later steps

        Returns
        -------
        tuple[int,pathlib.Path]
            A list of namedtuples, The first of which being the SLURM job ID and the second
            being the desired output Path.
        """

        # Generates filelist for resize pipeline
        with open(self.working_dir / "resize_filelist.txt", "w+") as rfl:
            rfl.write(str(self.image_path) + "\n")
        self.resize_filelist_path = self.working_dir / "resize_filelist.txt"

        # Defines variables for bash script
        script_config = {
            "memory": "80G",
            "filelist_path": str(self.resize_filelist_path),
            "output_path": str(self.working_dir),
            "pipeline_path": str(self.rescale_pipeline_path),
        }

        # Generates script_body from existing templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_core", package_path="templates"
            )
        )
        script_body = jinja_env.get_template("resize_cellprofiler_template.j2").render(
            script_config
        )

        # Creates bash script locally.
        with open(self.working_dir / "resize.sh", "w+") as rsh:
            rsh.write(script_body)

        # Runs resize on slurm
        output = subprocess.run(
            ["ssh", "slurm-master", "sbatch", f"{str(self.working_dir)}/resize.sh"],
            check=True,
            capture_output=True,
        )

        # Sets path to resized image to image path for future use
        self.image_path = (
            self.image_path.parent
            / f"{self.image_path.with_suffix('').name}_RescaleAndCrop.tiff"
        )

        job_ID = int(output.stdout.decode("utf-8").split(" ")[-1][:-1])
        return job_ID, self.image_path

    def run_ilastik(self):
        """Applies the Ilastik Pipeline processing to the downsampled image to
        produce a Probability map of the prior image.

        Returns
        -------
        tuple[int,pathlib.Path]
            A list of namedtuples, The first of which being the SLURM job ID and the second
            being the desired output Path.
        """

        # Parameters to input to bash script template
        script_config = {
            "memory": "60G",
            "image_path": f"'{str( self.image_path)}'",
            "output_path": f"'{str(self.image_path.with_suffix(''))}_Probabilities.tiff'",
        }

        # Generates script for SLURM submission from templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_core", package_path="templates"
            )
        )
        script_body = jinja_env.get_template("6_well_ilastik_template.j2").render(
            script_config
        )
        with open(self.working_dir / "ilastik.sh", "w+") as rsh:
            rsh.write(script_body)

        # Submit bash script ilastik.sh on SLURM
        output = subprocess.run(
            ["ssh", "slurm-master", "sbatch", f"{str(self.working_dir)}/ilastik.sh"],
            check=True,
            capture_output=True,
        )

        # Creates filelist.txt
        with open(self.working_dir / "filelist.txt", "w+") as rfl:
            rfl.write(str(self.image_path) + "\n")
            rfl.write(str(self.image_path.with_suffix("")) + "_Probabilities.tiff")

        self.filelist_path = self.working_dir / "filelist.txt"
        job_ID = int(output.stdout.decode("utf-8").split(" ")[-1][:-1])
        return job_ID, Path(f"{self.image_path.with_suffix('')}_Probabilities.tiff")

    def run_cellprofiler(self):
        """Applies the Cell Profiler Pipeline processing to the downsampled image using the Ilastik
        probabilities to produce a outlined cell profile and a series of metrics

        Returns
        -------
        tuple[int,pathlib.Path]
            A list of namedtuples, The first of which being the SLURM job ID and the second
            being the desired output Path.
        """

        # Parameters to input to bash script template.
        script_config = {
            "filelist_path": str(self.filelist_path),
            "output_dir": str(self.working_dir / "cell_profiler_outputs"),
            "pipeline_path": str(self.cellprofiler_pipeline_path),
            "memory": "50G",
        }

        # Generates script for SLURM submission from templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_core", package_path="templates"
            )
        )

        script_body = jinja_env.get_template("cellprofiler_template.j2").render(
            script_config
        )

        with open(self.working_dir / "cellprofiler.sh", "w+") as rsh:
            rsh.write(script_body)

        # Submit bash script cellprofiler.sh on SLURM
        output = subprocess.run(
            [
                "ssh",
                "slurm-master",
                "sbatch",
                f"{str(self.working_dir)}/cellprofiler.sh",
            ],
            check=True,
            capture_output=True,
        )

        # Set output path
        self.cell_profiler_output_path = self.working_dir / "cell_profiler_outputs"

        # Splits job id int from output
        job_ID = int(output.stdout.decode("utf-8").split(" ")[-1][:-1])

        return (
            job_ID,
            [
                Path(
                    f"{script_config['output_dir']}/{self.image_path.with_suffix('').name}_outlines.png"
                ),
                Path(f"{script_config['output_dir']}/ImageDATA.csv"),
            ],
        )

    def upload_metrics(self, conn, table: str) -> str:
        """Uploads the metrics from the cell profiler pipeline run and comnbines them with
        the Images Metadata. Then Uploads metrics to postgres database.

        Parameters
        ----------
        postgres_password: str
            To access the postgres database a password is needed.

        table_name: str = '"Celigo_96_Well_Data_Test"'
            There are many tables in the Microscopy DB. This parameter specifies which table
            to insert metrics into.

        Returns
        -------
        self.raw_image_path.name
            returns the original files name. This return is used to index 'table_name' in the
            future in order to insert additional metrics.
        """
        celigo_image = CeligoUploader(
            self.raw_image_path, file_type="temp", env=self.env
        )
        self.metadata = celigo_image.metadata["microscopy"]

        # Building Metric Output from Cellprofiler outputs
        ImageDATA = pd.read_csv(self.cell_profiler_output_path / "ImageDATA.csv")

        # formatting
        ImageDATA["Metadata_DateString"] = (
            self.metadata["celigo"]["scan_date"]
            + " "
            + self.metadata["celigo"]["scan_time"]
        )

        ImageDATA["barcode"] = self.metadata["plate_barcode"]
        ImageDATA["Metadata_Well"] = celigo_image.well
        ImageDATA["Experiment ID"] = self.raw_image_path.name
        ImageDATA["row"] = int(celigo_image.row) - 1
        ImageDATA["col"] = int(celigo_image.col) - 1

        result = ImageDATA.drop(columns=["ImageNumber"])
        result = result.fillna(-1)
        add_to_table(conn, result, table)

        confluency = (
            ImageDATA["AreaOccupied_AreaOccupied_Colony"].mean()
            / ImageDATA["AreaOccupied_AreaOccupied_WellObjects"].mean()
        )
        if not self.lk.select_rows_as_list(
            "assayscustom",
            "HamiltonWellConfluency",
            filter_array=[
                QueryFilter("WellId", celigo_image.well_id),
                QueryFilter("ScanTime", str(celigo_image.datetime) + ".000"),
            ],
        ):
            row = {
                "WellId": celigo_image.well_id,
                "ScanTime": celigo_image.datetime,
                "Confluency": confluency,
            }
            self.lk.insert_rows("assayscustom", "HamiltonWellConfluency", rows=[row])
        return self.raw_image_path.name
