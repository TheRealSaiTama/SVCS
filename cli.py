import click
import os
from pathlib import Path
from filetracker import FileTracker
from versionmanager import VersionManager
from diffengine import DiffEngine

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    path = Path.cwd()
    ctx.obj['tracker'] = FileTracker(path)
    ctx.obj['vm'] = VersionManager(path)
    ctx.obj['diff'] = DiffEngine()

@cli.command()
@click.pass_context
def init(ctx):
    tracker = ctx.obj['tracker']
    click.echo(f"Initialized empty SVCS repository in {tracker.vcs}")

@cli.command()
@click.argument('msg')
@click.pass_context
def commit(ctx, msg):
    vm = ctx.obj['vm']
    tracker = ctx.obj['tracker']
    
    states = tracker.get_file_states()
    tracker.save_file_states(states)
    
    vid = vm.create_version(msg)
    click.echo(f"Created version {vid}")

@cli.command()
@click.pass_context
def status(ctx):
    tracker = ctx.obj['tracker']
    status = tracker.get_status()
    
    click.echo("File status:")
    
    if not any(status.values()):
        click.echo("  No changes detected")
        return
    
    if status['modified']:
        click.echo("\nModified files:")
        for f in status['modified']:
            click.echo(f"  {f}")
    
    if status['added']:
        click.echo("\nNew files:")
        for f in status['added']:
            click.echo(f"  {f}")
    
    if status['deleted']:
        click.echo("\nDeleted files:")
        for f in status['deleted']:
            click.echo(f"  {f}")

@cli.command()
@click.argument('vid')
@click.pass_context
def checkout(ctx, vid):
    vm = ctx.obj['vm']
    try:
        manifest = vm.checkout_version(vid)
        click.echo(f"Restored version {vid} - '{manifest['message']}'")
    except ValueError as e:
        click.echo(f"Error: {str(e)}")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")

@cli.command()
@click.pass_context
def log(ctx):
    vm = ctx.obj['vm']
    versions = vm.get_versions()
    
    if not versions:
        click.echo("No versions found. Create one with 'svcs commit'")
        return
    
    click.echo("Version history:")
    for ver in reversed(versions):
        date = ver['timestamp'].split('T')[0]
        click.echo(f"Version: {ver['id']} ({date})")
        click.echo(f"  Message: {ver['message']}")
        click.echo(f"  Files: {len(ver['files'])}")
        click.echo("")

@cli.command()
@click.option('--file', '-f', help='Show diff for a specific file')
@click.argument('v1id', required=False)
@click.argument('v2id', required=False)
@click.pass_context
def diff(ctx, file, v1id, v2id):
    vm = ctx.obj['vm']
    diff = ctx.obj['diff']
    
    if not v1id and not v2id:
        versions = vm.get_versions()
        if not versions:
            click.echo("No versions found to compare")
            return
        
        latest = versions[-1]['id']
        v1id = latest
        v2id = 'working'
    
    elif v1id and not v2id:
        v2id = 'working'
    
    path = Path.cwd()
    
    if v2id == 'working':
        vdir = os.path.join(path, '.svcs', 'versions', v1id)
        
        if not os.path.exists(vdir):
            click.echo(f"Version {v1id} not found")
            return
        
        if file:
            v1 = os.path.join(vdir, file)
            v2 = os.path.join(path, file)
            
            if not os.path.exists(v1):
                click.echo(f"File {file} not found in version {v1id}")
                return
                
            if not os.path.exists(v2):
                click.echo(f"File {file} not found in working directory")
                return
            
            try:
                result = diff.file_diff(v1, v2)
                click.echo(result)
            except Exception as e:
                click.echo(f"Error comparing files: {str(e)}")
        else:
            click.echo(f"Comparing version {v1id} with working copy:")
            
            tracker = ctx.obj['tracker']
            status = tracker.get_status()
            
            if status['modified']:
                click.echo("\nModified files:")
                for mfile in status['modified']:
                    v1 = os.path.join(vdir, mfile)
                    v2 = os.path.join(path, mfile)
                    
                    if os.path.exists(v1) and os.path.exists(v2):
                        try:
                            click.echo(f"\n--- {mfile} ---")
                            result = diff.file_diff(v1, v2)
                            click.echo(result)
                        except Exception as e:
                            click.echo(f"Error comparing {mfile}: {str(e)}")
            
            if status['added']:
                click.echo("\nAdded files:")
                for newf in status['added']:
                    click.echo(f"  {newf}")
            
            if status['deleted']:
                click.echo("\nDeleted files:")
                for delf in status['deleted']:
                    click.echo(f"  {delf}")
    else:
        v1dir = os.path.join(path, '.svcs', 'versions', v1id)
        v2dir = os.path.join(path, '.svcs', 'versions', v2id)
        
        if not os.path.exists(v1dir):
            click.echo(f"Version {v1id} not found")
            return
            
        if not os.path.exists(v2dir):
            click.echo(f"Version {v2id} not found")
            return
        
        if file:
            v1 = os.path.join(v1dir, file)
            v2 = os.path.join(v2dir, file)
            
            if not os.path.exists(v1) and not os.path.exists(v2):
                click.echo(f"File {file} not found in either version")
                return
                
            if not os.path.exists(v1):
                click.echo(f"File {file} added in version {v2id}")
                return
                
            if not os.path.exists(v2):
                click.echo(f"File {file} deleted in version {v2id}")
                return
            
            try:
                result = diff.file_diff(v1, v2)
                if result:
                    click.echo(result)
                else:
                    click.echo(f"No changes in {file} between versions")
            except Exception as e:
                click.echo(f"Error comparing files: {str(e)}")
        else:
            click.echo(f"Comparing version {v1id} with version {v2id}:")
            
            changes = vm.compare_versions(v1id, v2id)
            
            if changes['modified']:
                click.echo("\nModified files:")
                for mfile in changes['modified']:
                    v1 = os.path.join(v1dir, mfile)
                    v2 = os.path.join(v2dir, mfile)
                    
                    if os.path.exists(v1) and os.path.exists(v2):
                        try:
                            click.echo(f"\n--- {mfile} ---")
                            result = diff.file_diff(v1, v2)
                            click.echo(result)
                        except Exception as e:
                            click.echo(f"Error comparing {mfile}: {str(e)}")
            
            if changes['added']:
                click.echo("\nAdded files:")
                for newf in changes['added']:
                    click.echo(f"  {newf}")
            
            if changes['removed']:
                click.echo("\nRemoved files:")
                for delf in changes['removed']:
                    click.echo(f"  {delf}")

if __name__ == '__main__':
    cli()