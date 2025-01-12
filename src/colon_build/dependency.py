import logging
from .core import parse_package_xml, is_system_dependency
import os

logger = logging.getLogger(__name__)

def resolve_dependencies(packages):
    logger.info("Starting dependency resolution")
    build_order = []
    packages_to_process = packages.copy()
    
    for pkg in packages_to_process:
        dependencies = parse_package_xml(pkg)
        local_deps = [dep for dep in dependencies 
                        if not is_system_dependency(dep)]
        
        if not local_deps:  # If all dependencies are system dependencies
            build_order.append(pkg)
        else:
            logger.error(f"Unexpected local dependencies found: {local_deps}")
            raise RuntimeError(f"Unexpected local dependencies in {os.path.basename(pkg)}: {local_deps}")
    
    logger.info("Dependency resolution completed successfully")
    return build_order
