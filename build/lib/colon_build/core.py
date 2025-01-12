import os
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def find_packages(src_dir):
    logger.info(f"Scanning for packages in {src_dir}")
    packages = []
    for root, dirs, files in os.walk(src_dir):
        if 'package.xml' in files:
            logger.debug(f"Found package at: {root}")
            packages.append(root)
    logger.debug(f"Discovered packages: {[os.path.basename(p) for p in packages]}")
    return packages

def parse_package_xml(package_path):
    logger.debug(f"Parsing package.xml in {package_path}")
    try:
        tree = ET.parse(os.path.join(package_path, 'package.xml'))
        root = tree.getroot()
        dependencies = [dep.text for dep in root.findall('.//depend')]
        logger.debug(f"Found dependencies for {os.path.basename(package_path)}: {dependencies}")
        return dependencies
    except ET.ParseError as e:
        logger.error(f"Failed to parse package.xml in {package_path}: {str(e)}")
        raise

def is_system_dependency(dep_name):
    """Check if a dependency is a system/external package."""
    # Common ROS2 and system package prefixes
    system_prefixes = ['ros2', 'rclcpp', 'rclpy', 'std_msgs', 'geometry_msgs', 'sensor_msgs', 
                    'builtin_interfaces', 'rosidl', 'ament', 'launch']
    return any(dep_name.startswith(prefix) for prefix in system_prefixes)

def detect_build_system(package_path):
    """Detect whether the package uses CMake or Python setup."""
    logger.debug(f"Detecting build system for {os.path.basename(package_path)}")
    
    # Check for CMake
    if os.path.exists(os.path.join(package_path, 'CMakeLists.txt')):
        logger.info(f"CMake build system detected for {os.path.basename(package_path)}")
        return 'cmake'
    
    # Check for Python
    if any(os.path.exists(os.path.join(package_path, f)) 
            for f in ['setup.py', 'pyproject.toml']):
        logger.info(f"Python build system detected for {os.path.basename(package_path)}")
        return 'python'
    
    logger.warning(f"Could not detect build system for {os.path.basename(package_path)}")
    return 'unknown'

def setup_workspace(workspace_path):
    """Set up workspace directories."""
    logger.info(f"Setting up workspace structure in {workspace_path}")
    install_dir = os.path.join(workspace_path, 'install')
    os.makedirs(install_dir, exist_ok=True)
    return install_dir

def generate_setup_files(workspace_path):
    """Generate workspace setup files."""
    install_dir = os.path.join(workspace_path, 'install')
    setup_bash_content = f"""#!/bin/bash

WORKSPACE_ROOT="{os.path.abspath(workspace_path)}"
INSTALL_DIR="$WORKSPACE_ROOT/install"

# Source ROS2 environment if not already sourced
if [ -z "$ROS_DISTRO" ]; then
    echo "Warning: ROS2 environment not sourced"
fi

# Extend environment variables
export PYTHONPATH="$INSTALL_DIR/lib/python3.8/site-packages:$PYTHONPATH"
export PATH="$INSTALL_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$INSTALL_DIR/lib:$LD_LIBRARY_PATH"

# Source package-specific setup files
for setup_file in "$INSTALL_DIR"/share/*/local_setup.bash; do
    if [ -f "$setup_file" ]; then
        source "$setup_file"
    fi
done
"""
    
    with open(os.path.join(install_dir, 'setup.bash'), 'w') as f:
        f.write(setup_bash_content)
    os.chmod(os.path.join(install_dir, 'setup.bash'), 0o755)
    
    logger.info(f"Generated setup files in {install_dir}")
