import subprocess
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PackageInfo:
    name: str
    version: Optional[str]
    dependencies: List[Tuple[str, Optional[str]]]
    summary: str = ""
    home_page: str = ""
    author: str = ""
    license: str = ""
    location: str = ""
    requires: str = ""
    required_by: str = ""

    def __str__(self):
        version_str = f"=={self.version}" if self.version else ""
        return f"{self.name}{version_str}"

class DependencyAnalyzer:
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.cache: Dict[str, PackageInfo] = {}

    def parse_requirements(self, file_path: str) -> Dict[str, Optional[str]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist.")
        
        dependencies = {}
        version_pattern = re.compile(r'^([^=<>~!]+)(?:[=<>~!]=?|@)(.+)$')
        
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                    
                match = version_pattern.match(line)
                if match:
                    package, version = match.groups()
                    dependencies[package.strip()] = version.strip()
                else:
                    dependencies[line] = None
                    
        return dependencies

    def fetch_package_info(self, package_name: str) -> Optional[PackageInfo]:
        if package_name in self.cache:
            return self.cache[package_name]
            
        try:
            result = subprocess.run(
                ["pip", "show", package_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.warning(f"Error fetching info for {package_name}: {result.stderr}")
                return None

            info_dict = {}
            for line in result.stdout.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    info_dict[key.strip()] = value.strip()

            dependencies = []
            if "Requires" in info_dict:
                deps = info_dict.get("Requires", "").split(",")
                for dep in (d.strip() for d in deps if d.strip()):
                    dep_version = self.fetch_installed_version(dep)
                    dependencies.append((dep, dep_version))

            package_info = PackageInfo(
                name=package_name,
                version=info_dict.get("Version"),
                dependencies=dependencies,
                summary=info_dict.get("Summary", ""),
                home_page=info_dict.get("Home-page", ""),
                author=info_dict.get("Author", ""),
                license=info_dict.get("License", ""),
                location=info_dict.get("Location", ""),
                requires=info_dict.get("Requires", ""),
                required_by=info_dict.get("Required-by", "")
            )
            
            self.cache[package_name] = package_info
            return package_info
            
        except Exception as e:
            logger.error(f"Error processing package {package_name}: {e}")
            return None

    def fetch_installed_version(self, package_name: str) -> Optional[str]:
        package_info = self.fetch_package_info(package_name)
        return package_info.version if package_info else None

    def build_dependency_tree(self, requirements: Dict[str, Optional[str]], max_depth: int = 5) -> Dict[str, dict]:
        tree = {}
        visited = set()
        
        def process_package(package: str, depth: int) -> None:
            if depth <= 0 or package in visited:
                return
                
            visited.add(package)
            package_info = self.fetch_package_info(package)
            
            if not package_info:
                return
                
            package_key = str(package_info)
            tree[package_key] = {
                "dependencies": [],
                "info": {
                    "summary": package_info.summary,
                    "home_page": package_info.home_page,
                    "author": package_info.author,
                    "license": package_info.license,
                    "location": package_info.location,
                    "requires": package_info.requires,
                    "required_by": package_info.required_by
                }
            }
            
            for dep_name, dep_version in package_info.dependencies:
                dep_str = f"{dep_name}=={dep_version}" if dep_version else dep_name
                tree[package_key]["dependencies"].append(dep_str)
                process_package(dep_name, depth - 1)
                
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(process_package, package, max_depth)
                for package in requirements.keys()
            ]
            for future in futures:
                future.result()
                
        return tree

    def visualize_dependencies(self, tree: Dict[str, dict], output_file: str = "dependency_graph.png", figsize: Tuple[int, int] = (12, 8)):
        G = nx.DiGraph()
        
        for package, info in tree.items():
            G.add_node(package)
            for dep in info["dependencies"]:
                G.add_edge(package, dep)
        
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        nx.draw(G, pos,
                with_labels=True,
                node_color='lightblue',
                node_size=2000,
                font_size=8,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                arrowsize=20)
        
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Dependency graph saved to {output_file}")
        
        return G

def main():
    try:
        analyzer = DependencyAnalyzer()
        requirements_file = "requirements.txt"
        
        requirements = analyzer.parse_requirements(requirements_file)
        print("\nTop-Level Dependencies:")
        for package, version in requirements.items():
            print(f"  {package}: {version or 'latest'}")
        
        dependency_tree = analyzer.build_dependency_tree(requirements)
        print("\nDependency Tree with Package Info:")
        print(json.dumps(dependency_tree, indent=2))
        
        graph = analyzer.visualize_dependencies(dependency_tree)
        print("\nVisualization saved as 'dependency_graph.png'")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()