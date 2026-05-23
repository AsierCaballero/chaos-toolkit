"""CLI entry point for chaos-toolkit."""

import logging
import sys

import click

from chaos_toolkit.config import load_config
from chaos_toolkit.runner import (
    run_experiment,
    list_experiments,
    get_experiment_status,
    get_experiment_logs,
    describe_experiment,
)

logger = logging.getLogger(__name__)


@click.group()
@click.option("--config", "-c", default="~/.chaos/config.yaml", help="Config file path")
@click.option("--namespace", "-n", default="default", help="Kubernetes namespace")
@click.option("--verbose", "-v", is_flag=True)
@click.pass_context
def cli(ctx, config, namespace, verbose):
    """Chaos Toolkit — manage LitmusChaos experiments from your terminal."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)
    ctx.obj["namespace"] = namespace


@cli.command()
@click.argument("manifest", type=click.Path(exists=True))
@click.option("--duration", default=60, type=int, help="Experiment duration in seconds")
@click.option("--wait/--no-wait", default=True, help="Wait for completion")
@click.pass_context
def run(ctx, manifest, duration, wait):
    """Run a chaos experiment from a manifest file."""
    ns = ctx.obj["namespace"]
    result = run_experiment(manifest, ns, duration, wait)
    if result["success"]:
        click.echo(f"{result['name']} — {result['verdict']}")
    else:
        click.echo(f"Error: {result.get('error', 'unknown')}", err=True)
        sys.exit(1)


@cli.command("list")
@click.pass_context
def list_cmd(ctx):
    """List all chaos experiments in the namespace."""
    experiments = list_experiments(ctx.obj["namespace"])
    if not experiments:
        click.echo("No experiments found.")
        return
    from tabulate import tabulate
    click.echo(tabulate(experiments, headers="keys", tablefmt="simple"))


@cli.command()
@click.argument("name")
@click.pass_context
def status(ctx, name):
    """Get experiment status and verdict."""
    result = get_experiment_status(name, ctx.obj["namespace"])
    if not result:
        click.echo(f"Experiment '{name}' not found.", err=True)
        sys.exit(1)
    for k, v in result.items():
        click.echo(f"{k:<12} {v}")


@cli.command()
@click.argument("name")
@click.pass_context
def logs(ctx, name):
    """Fetch experiment pod logs."""
    click.echo(get_experiment_logs(name, ctx.obj["namespace"]))


@cli.command("describe")
@click.argument("name")
@click.pass_context
def describe_cmd(ctx, name):
    """Show the full experiment manifest."""
    manifest = describe_experiment(name, ctx.obj["namespace"])
    if not manifest:
        click.echo(f"Experiment '{name}' not found.", err=True)
        sys.exit(1)
    click.echo(manifest)


@cli.command("templates")
def templates_cmd():
    """List available experiment templates."""
    from chaos_toolkit.experiments import TEMPLATES
    from tabulate import tabulate
    rows = [{"name": k, "description": v["description"]} for k, v in TEMPLATES.items()]
    click.echo(tabulate(rows, headers="keys", tablefmt="simple"))

