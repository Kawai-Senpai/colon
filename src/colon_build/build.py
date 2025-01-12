import os
import logging
import subprocess
from .core import detect_build_system

logger = logging.getLogger(__name__)

def build_cmake_package(package_path, install_dir):
    """Build a CMake-based package."""
    logger.info(f"Building CMake package: {os.path.basename(package_path)}")
    build_dir = os.path.join(package_path, 'build')
    os.makedirs(build_dir, exist_ok=True)
    
    try:
        logger.info("Running CMake configuration...")
        subprocess.run([
            'cmake', package_path, 
            '-B', build_dir,
            f'-DCMAKE_INSTALL_PREFIX={install_dir}'
        ], check=True, capture_output=True, text=True)
        
        logger.info("Running CMake build...")
        result = subprocess.run(['cmake', '--build', build_dir], check=True,
                                capture_output=True, text=True)
        logger.debug(f"Build output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"CMake build failed: {str(e)}")
        logger.error(f"Command output:\n{e.output}")
        raise

def build_python_package(package_path, install_dir):
    """Build a Python-based package."""
    logger.info(f"Building Python package: {os.path.basename(package_path)}")
    try:
        result = subprocess.run([
            'python', 'setup.py', 'build',
            '--build-base', os.path.join(package_path, 'build'),
            '--build-lib', os.path.join(install_dir, 'lib/python3.8/site-packages')
        ], cwd=package_path, check=True, capture_output=True, text=True)
        logger.debug(f"Build output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Python build failed: {str(e)}")
        logger.error(f"Command output:\n{e.output}")
        raise

def build_package(package_path, install_dir):
    """Build a package using the appropriate build system."""
    build_system = detect_build_system(package_path)
    
    if build_system == 'cmake':
        build_cmake_package(package_path, install_dir)
    elif build_system == 'python':
        build_python_package(package_path, install_dir)
    else:
        raise ValueError(f"Unsupported or unknown build system for {package_path}")

def install_cmake_package(package_path, install_dir):
    """Install a CMake-based package."""
    logger.info(f"Installing CMake package: {os.path.basename(package_path)}")
    build_dir = os.path.join(package_path, 'build')
    try:
        result = subprocess.run(['cmake', '--install', build_dir], check=True,
                            capture_output=True, text=True)
        logger.debug(f"Install output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"CMake installation failed: {str(e)}")
        logger.error(f"Command output:\n{e.output}")
        raise

def install_python_package(package_path):
    """Install a Python-based package."""
    logger.info(f"Installing Python package: {os.path.basename(package_path)}")
    try:
        result = subprocess.run(['pip', 'install', '--no-deps', '.'],
                            cwd=package_path, check=True, capture_output=True, text=True)
        logger.debug(f"Install output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Python installation failed: {str(e)}")
        logger.error(f"Command output:\n{e.output}")
        raise

def install_package(package_path, install_dir):
    """Install a package using the appropriate build system."""
    build_system = detect_build_system(package_path)
    
    if build_system == 'cmake':
        install_cmake_package(package_path, install_dir)
    elif build_system == 'python':
        # Python packages are installed during build
        pass
    else:
        raise ValueError(f"Unsupported or unknown build system for {package_path}")
