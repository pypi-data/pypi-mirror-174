import argparse
import logging
import os
import pwd
import sys
import traceback

from celigo_pipeline_core.celigo_orchestration import (
    run_all_dir,
)

log = logging.getLogger()


class Args(argparse.Namespace):
    def __init__(self):
        super().__init__()
        self.debug = False
        self.image_path = str()
        self.postgres_password = str()
        self.__parse()

    def __parse(self):
        p = argparse.ArgumentParser(
            prog="CeligoPipeline",
            description="generates Cell Profiler Output metrics from Celigo Images in a directory ",
        )

        p.add_argument(
            "--dir_path",
            dest="dir_path",
            type=str,
            help="directory of Image file locations on local computer (Images for Processing)",
            required=True,
        )

        p.add_argument(
            "--debug",
            help="Enable debug mode",
            default=False,
            required=False,
            action="store_true",
        )

        # make array with options
        p.add_argument(
            "--env",
            type=str,
            help="Environment that data will be stored to('prod, 'stg', default is 'stg')",
            default="stg",
            required=False,
        )
        p.add_argument(
            "--chunk_size",
            type=int,
            help="Number of files to process in parallel",
            default=30,
            required=False,
        )
        p.add_argument(
            "--env_vars",
            type=str,
            help="path to .env file",
            default=f"/home/{pwd.getpwuid(os.getuid())[0]}/.env",
            required=False,
        )
        p.add_argument(
            "--working_dir",
            type=str,
            help="working directory to copy files, default is home directory on isilon",
            default="",
            required=False,
        )
        p.add_argument(
            "--keep_outputs",
            action="store_true",
            help="Keep outputs in working directory, default is False",
            default=False,
            required=False,
        )
        p.add_argument(
            "--ignore_upload",
            action="store_false",
            help="Upload metrics to FMS,LK,POSTGRES etc...",
            default=True,
            required=False,
        )
        p.parse_args(namespace=self)

    ###############################################################################


def main():
    args = Args()
    debug = args.debug

    try:
        run_all_dir(
            dir_path=args.dir_path,
            chunk_size=args.chunk_size,
            env=args.env,
            env_vars=args.env_vars,
            working_dir=args.working_dir,
            keep_outputs=args.keep_outputs,
            upload=args.ignore_upload,
        )

    except Exception as e:
        log.error("=============================================")
        if debug:
            log.error("\n\n" + traceback.format_exc())
            log.error("=============================================")
        log.error("\n\n" + str(e) + "\n")
        log.error("=============================================")
        sys.exit(1)


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
