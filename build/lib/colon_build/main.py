import argparse
import logging
import os
from .core import find_packages, setup_workspace, generate_setup_files
from .dependency import resolve_dependencies
from .build import build_package, install_package

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def find_workspace_root(start_path=None):
    """Find the workspace root by looking for 'src' directory."""
    if start_path is None:
        start_path = os.getcwd()
    
    current = os.path.abspath(start_path)
    while True:
        if os.path.exists(os.path.join(current, 'src')):
            return current
        parent = os.path.dirname(current)
        if parent == current:  # Reached root directory
            return None
        current = parent

def build_command(args):
    """Handle the 'build' subcommand."""
    logger = logging.getLogger(__name__)

    # Find workspace root if not specified
    workspace_path = args.workspace or find_workspace_root()
    if not workspace_path:
        logger.error("Not in a ROS2 workspace. Please run from within a workspace or specify path.")
        return 1

    logger.info(f"Starting build process in workspace: {workspace_path}")
    
    # Setup workspace structure
    install_dir = setup_workspace(workspace_path)
    
    logger.info("Discovering packages...")
    packages = find_packages(os.path.join(workspace_path, 'src'))
    if not packages:
        logger.error("No packages found in workspace")
        return 1
    logger.info(f"Found {len(packages)} packages")
    
    try:
        logger.info("Resolving dependencies...")
        build_order = resolve_dependencies(packages)
        logger.info(f"Build order determined: {[os.path.basename(p) for p in build_order]}")

        for i, package in enumerate(build_order, 1):
            logger.info(f"Processing package {i}/{len(build_order)}: {os.path.basename(package)}")
            try:
                logger.info(f"Building {package}...")
                build_package(package, install_dir)
                logger.info(f"Installing {package}...")
                install_package(package, install_dir)
                logger.info(f"Successfully completed {package}")
            except Exception as e:
                logger.error(f"Failed to process {package}: {str(e)}")
                return 1

        # Generate workspace setup files
        generate_setup_files(workspace_path)
        logger.info(f"Build complete! Source {os.path.join(install_dir, 'setup.bash')} to use the workspace")
        return 0
    except Exception as e:
        logger.error(f"Build failed: {str(e)}")
        return 1

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Colon - A ROS2 Build Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build the workspace')
    build_parser.add_argument('workspace', nargs='?', type=str, 
                             help='path to the workspace (optional if run from within workspace)')
    build_parser.add_argument('-v', '--verbose', action='store_true', 
                            help='Enable verbose output')
    
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.command == 'build':
        return build_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    exit(main())
