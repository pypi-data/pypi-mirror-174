from flamapy.core.operations import Operation
from flamapy.metamodels.dn_metamodel.models import DependencyNetwork, Version


class NetworkInfo(Operation):

    def __init__(self) -> None:
        self.result: dict[str, int] = {
            'direct_dependencies': 0,
            'indirect_dependencies': 0,
            'direct_cves': 0,
            'indirect_cves': 0,
            'constraints': 0
        }
        self.direct_dependencies: list = []
        self.indirect_dependencies: list = []
        self.direct_cves: list = []
        self.indirect_cves: list = []

    def get_result(self) -> dict[str, int]:
        return self.result

    def execute(self, model: DependencyNetwork) -> None:
        for requirement_file in model.requirement_files:
            self.result['constraints'] += len(requirement_file.packages)
            for package in requirement_file.packages:
                if package.name not in self.direct_dependencies:
                    self.direct_dependencies.append(package.name)
                for version in package.versions:
                    for cve in version.cves:
                        if cve['id'] not in self.direct_cves: self.direct_cves.append(cve['id'])
                    self.indirect(version)
        self.result['direct_dependencies'] = len(self.direct_dependencies)
        self.result['indirect_dependencies'] = len(self.indirect_dependencies)
        self.result['direct_cves'] = len(self.direct_cves)
        self.result['indirect_cves'] = len(self.indirect_cves)

    def indirect(self, parent_version: Version) -> None:
        if hasattr(parent_version, 'packages'):
            self.result['constraints'] += len(parent_version.packages)
            for package in parent_version.packages:
                if package.name not in self.indirect_dependencies:
                    self.indirect_dependencies.append(package.name)
                for version in package.versions:
                    for cve in version.cves:
                        if cve['id'] not in self.indirect_cves: self.indirect_cves.append(cve['id'])
                    self.indirect(version)