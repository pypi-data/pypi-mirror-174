from flamapy.core.transformations import Transformation

from flamapy.metamodels.dn_metamodel.models import (DependencyNetwork, Package,
                                 RequirementFile, Version)

from copy import copy


class SerializeNetwork(Transformation):

    '''
    SerializeNetwork(
        source_model: dict
    )
    '''

    source_model: dict
    destination_model: DependencyNetwork | None = None

    def __init__(self, **kwargs) -> None:
        valid_keys = [
            'source_model',
        ]
        for key in valid_keys:
            setattr(self, key, kwargs.get(key))

    def transform(self) -> None:
        self.source_model['requirement_files'] = [self.transform_requirement_file(req_file) for req_file in self.source_model['requirement_files']]
        self.destination_model = DependencyNetwork(**self.source_model)

    def transform_requirement_file(self, requirement_file: dict) -> RequirementFile:
        requirement_file['packages'] = [self.transform_package(package) for package in requirement_file['packages']]
        req_file = RequirementFile(**requirement_file)
        return req_file

    def transform_package(self, package: dict) -> Package:
        raw_versions = copy(package['versions'])
        package['versions'] = []
        new_package = Package(**package)
        versions = []
        for version in raw_versions:
            new_version = self.transform_version(version)
            versions.append(new_version)
        new_package.versions = versions
        return new_package

    def transform_version(self, version: dict) -> Version:
        raw_packages = copy(version['packages'])
        version['packages'] = []
        new_version = Version(**version)
        packages = []
        for package in raw_packages:
            new_package = self.transform_package(package)
            packages.append(new_package)
        new_version.packages = packages
        return new_version