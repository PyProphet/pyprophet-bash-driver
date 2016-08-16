# encoding: utf-8
from __future__ import print_function

import os


import pkg_resources  # part of setuptools
version = tuple(map(int, pkg_resources.require("pyprophet-bash")[0].version.split(".")))


from pyprophet_cli.common_options import (data_folder, data_filename_pattern, job_count,
                                          sample_factor, extra_group_columns, lambda_,
                                          statistics_mode)

from click import option, echo, Path

# overwrite some options, work and result folder do not have to exist:

work_folder = option("--work-folder",
                     help="folder for intermediate results which are needed by following processing steps",
                     type=Path(file_okay=False, dir_okay=True, readable=True, writable=True),
                     required=False, default=None)

result_folder = option("--result-folder",
                       help="folder for final results",
                       type=Path(file_okay=False, dir_okay=True, writable=True),
                       required=False, default=None)

# other options:

job_slot_limit = option("--job-slot-limit",
                        help="maximum number of jobs that are allowed to run at any one time",
                        type=int,
                        default=32
                        )


extra_args_prepare = option("--extra-args-prepare", default="",
                            help="extra args for calling prepare command")
extra_args_subsample = option("--extra-args-subsample", default="",
                              help="extra args for calling subsample command")
extra_args_learn = option("--extra-args-learn", default="",
                          help="extra args for calling learn command")
extra_args_apply_weights = option("--extra-args-apply-weights", default="",
                                  help="extra args for calling apply-weights command")

extra_args_score = option("--extra-args-score", default="",
                          help="extra args for calling score command")

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    echo("%d.%d.%d" % version)
    ctx.exit()

print_version = option("--version", is_flag=True, callback=print_version, expose_value=False,
                       is_eager=True, help="print version of bash plugin")


def _options():

    options = [data_folder, data_filename_pattern, job_count, sample_factor,
               job_slot_limit, statistics_mode,
               result_folder, work_folder,
               extra_group_columns, lambda_,
               print_version,
               extra_args_prepare,
               extra_args_subsample,
               extra_args_learn,
               extra_args_apply_weights,
               extra_args_score,
               ]
    return options


def _run_workflow(job):

    from run_on_bash import run_workflow

    (output,
     result_folder,
     work_folder) = run_workflow(job.work_folder, job.result_folder, job.data_folder, job.data_filename_pattern,
                                 job.job_count, job.sample_factor, job.job_slot_limit,
                                 job.statistics_mode,
                                 job.lambda_, job.extra_group_columns,
                                 job.extra_args_prepare,
                                 job.extra_args_subsample, job.extra_args_learn,
                                 job.extra_args_apply_weights, job.extra_args_score,
                                 callback=None, logger=job.logger)


def config():

    options = _options()
    help_ = """runs full pyprophet-cli workflow on BASH.
    """
    return "run_on_bash", options, _run_workflow, help_
