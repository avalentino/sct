# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""
CLI Radiometric Analysis commands
---------------------------------
"""
import logging
import sys
import time
from pathlib import Path

import art
import click
from arepyextras.quality.core.custom_logger import CustomFormatterFileHandler
from arepyextras.quality.radiometric_analysis.support import radiometric_profiles_to_netcdf

import sct.analyses.radiometric_analysis as ra
from sct.configuration.sct_configuration import SCTConfiguration

# syncing with logger
log = logging.getLogger("quality_analysis")

# creating a decorator to pass a SCTConfiguration dataclass object between commands
share_config = click.make_pass_decorator(SCTConfiguration)


@click.group(
    context_settings=dict(
        help_option_names=["-h", "--help"],
    )
)
@click.pass_context
def radiometric_analysis(config):
    """Block-wise Radiometric Analysis"""
    pass


@radiometric_analysis.command("nesz")
@click.option(
    "--product",
    "-p",
    required=True,
    type=click.Path(path_type=Path, exists=True, dir_okay=True),
    help="Path to the product to be analyzed",
)
@click.option(
    "--output_directory",
    "-out",
    required=True,
    default=None,
    type=click.Path(path_type=Path, exists=True, dir_okay=True),
    help="Path to the folder where to save output data",
)
@click.option(
    "--graphs",
    "-g",
    default=False,
    is_flag=True,
    type=bool,
    help="Flag to generate graphical output at the end of the analysis",
)
@share_config
def radiometric_analysis_nesz(config: SCTConfiguration, product: Path, output_directory: Path, graphs: bool):
    """Noise Equivalent Sigma-Zero radiometric analysis"""

    # saving log file to output folder
    if config.general.save_log:
        logging_file_handler = logging.FileHandler(output_directory.joinpath("sct_ra_analysis.log"))
        logging_file_handler.setFormatter(CustomFormatterFileHandler())
        log.addHandler(logging_file_handler)

    config_ra = config.radiometric_analysis

    if graphs:
        try:
            from arepyextras.quality.radiometric_analysis.graphical_output import radiometric_2D_hist_plot

        except ImportError:
            log.critical('Install graphs requirements "pip install sct[graphs]"')
            sys.exit(1)

    log.info(f"Selected product is: {product}")

    click.echo("\n")
    txt = art.text2art("NESZ   Analysis", font="doom")
    click.echo(txt + "\n")

    start = time.perf_counter_ns()
    output = ra.nesz_analysis(product_path=product, config=config_ra)

    # saving configuration used to output folder as .toml file
    if config.general.save_config_copy:
        config.dump_to_toml(out_file=output_directory.joinpath("analysis_config.toml"), selected="radiometry")

    if graphs:
        log.info("Saving results to netCDF and plotting graphs...")
    else:
        log.info("Saving results to netCDF format...")

    tag = "NESZ"
    for item in output:
        radiometric_profiles_to_netcdf(data=item, out_path=output_directory, tag=tag)

        # graphical output management
        if graphs:
            radiometric_2D_hist_plot(
                data=item,
                out_dir=output_directory,
                title=f"{tag.upper()} Profiles {item.swath} {item.polarization.name}",
            )

    elapsed = (time.perf_counter_ns() - start) / 1e9
    log.info(f"NESZ Analysis completed in {elapsed} s.")


@radiometric_analysis.command("gamma")
@click.option(
    "--product",
    "-p",
    required=True,
    type=click.Path(path_type=Path, exists=True, dir_okay=True),
    help="Path to the product to be analyzed",
)
@click.option(
    "--output_directory",
    "-out",
    required=True,
    default=None,
    type=click.Path(path_type=Path, exists=True, dir_okay=True),
    help="Path to the folder where to save output data",
)
@click.option(
    "--graphs",
    "-g",
    default=False,
    is_flag=True,
    type=bool,
    help="Flag to generate graphical output at the end of the analysis",
)
@share_config
def radiometric_analysis_gamma(config: SCTConfiguration, product: Path, output_directory: Path, graphs: bool):
    """Gamma-Zero Profiles radiometric analysis"""

    # saving log file to output folder
    if config.general.save_log:
        logging_file_handler = logging.FileHandler(output_directory.joinpath("sct_ra_analysis.log"))
        logging_file_handler.setFormatter(CustomFormatterFileHandler())
        log.addHandler(logging_file_handler)

    config_ra = config.radiometric_analysis

    if graphs:
        try:
            from arepyextras.quality.radiometric_analysis.graphical_output import radiometric_2D_hist_plot

        except ImportError:
            log.critical('Install graphs requirements "pip install sct[graphs]"')
            sys.exit(1)

    log.info(f"Selected product is: {product}")

    click.echo("\n")
    txt = art.text2art("Gamma   Profiles   Analysis", font="doom")
    click.echo(txt + "\n")

    start = time.perf_counter_ns()
    output = ra.gamma_analysis(product_path=product, config=config_ra)

    # saving configuration used to output folder as .toml file
    if config.general.save_config_copy:
        config.dump_to_toml(out_file=output_directory.joinpath("analysis_config.toml"), selected="radiometry")

    if graphs:
        log.info("Saving results to netCDF and plotting graphs...")
    else:
        log.info("Saving results to netCDF format...")

    tag = "GAMMA"
    for item in output:
        radiometric_profiles_to_netcdf(data=item, out_path=output_directory, tag=tag)

        # graphical output management
        if graphs:
            radiometric_2D_hist_plot(
                data=item,
                out_dir=output_directory,
                title=f"{tag.upper()} Profiles {item.swath} {item.polarization.name}",
            )

    elapsed = (time.perf_counter_ns() - start) / 1e9
    log.info(f"Gamma Profiles Analysis completed in {elapsed} s.")


@radiometric_analysis.command("scalloping")
@click.option(
    "--product",
    "-p",
    required=True,
    type=click.Path(path_type=Path, exists=True, dir_okay=True),
    help="Path to the product to be analyzed",
)
@click.option(
    "--output_directory",
    "-out",
    required=True,
    default=None,
    type=click.Path(path_type=Path, exists=True, dir_okay=True),
    help="Path to the folder where to save output data",
)
@click.option(
    "--graphs",
    "-g",
    default=False,
    is_flag=True,
    type=bool,
    help="Flag to generate graphical output at the end of the analysis",
)
@share_config
def radiometric_analysis_scalloping(config: SCTConfiguration, product: Path, output_directory: Path, graphs: bool):
    """Scalloping Profiles radiometric analysis"""

    # saving log file to output folder
    if config.general.save_log:
        logging_file_handler = logging.FileHandler(output_directory.joinpath("sct_ra_analysis.log"))
        logging_file_handler.setFormatter(CustomFormatterFileHandler())
        log.addHandler(logging_file_handler)

    config_ra = config.radiometric_analysis

    if graphs:
        try:
            from arepyextras.quality.radiometric_analysis.graphical_output import radiometric_2D_hist_plot

        except ImportError:
            log.critical('Install graphs requirements "pip install sct[graphs]"')
            sys.exit(1)

    log.info(f"Selected product is: {product}")

    click.echo("\n")
    txt = art.text2art("Scalloping   Profiles   Analysis", font="doom")
    click.echo(txt + "\n")

    start = time.perf_counter_ns()
    output = ra.scalloping_analysis(product_path=product, config=config_ra)

    # saving configuration used to output folder as .toml file
    if config.general.save_config_copy:
        config.dump_to_toml(out_file=output_directory.joinpath("analysis_config.toml"), selected="radiometry")

    if graphs:
        log.info("Saving results to netCDF and plotting graphs...")
    else:
        log.info("Saving results to netCDF format...")

    tag = "SCALLOPING"
    for item in output:
        radiometric_profiles_to_netcdf(data=item, out_path=output_directory, tag=tag)

        # graphical output management
        if graphs:
            radiometric_2D_hist_plot(
                data=item,
                out_dir=output_directory,
                title=f"{tag.upper()} Profiles {item.swath} {item.polarization.name}",
            )

    elapsed = (time.perf_counter_ns() - start) / 1e9
    log.info(f"Scalloping Profiles Analysis completed in {elapsed} s.")
