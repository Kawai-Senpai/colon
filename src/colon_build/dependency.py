import logging
from .core import parse_package_xml, is_system_dependency
import os

logger = logging.getLogger(__name__)

def resolve_dependencies(packages):
    logger.info("Starting dependency resolution")
    build_order = []
    packages_to_process = packages.copy()  # Work with a copy to preserve original
    
    while packages_to_process:
        progress_made = False
        logger.debug(f"Packages remaining: {[os.path.basename(p) for p in packages_to_process]}")
        
        for pkg in packages_to_process[:]:  # Iterate over a copy to allow removal
            dependencies = parse_package_xml(pkg)
            logger.debug(f"Checking dependencies for {os.path.basename(pkg)}")
            
            # Consider a package ready if all its deps are either in build_order or are system packages
            if all(dep in build_order or is_system_dependency(dep) for dep in dependencies):
                logger.info(f"Adding {os.path.basename(pkg)} to build order")
                build_order.append(pkg)
                packages_to_process.remove(pkg)
                progress_made = True
        
        if not progress_made:
            # If no progress was made in this iteration, we might have a circular dependency
            remaining = ', '.join(os.path.basename(p) for p in packages_to_process)
            logger.error(f"Circular dependency detected in: {remaining}")
            raise RuntimeError(f"Circular dependency detected or unresolvable dependencies in packages: {remaining}")
    
    logger.info("Dependency resolution completed successfully")
    return build_order
