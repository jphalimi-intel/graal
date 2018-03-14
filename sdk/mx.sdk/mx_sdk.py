#
# commands.py - the GraalVM specific commands
#
# ----------------------------------------------------------------------------------------------------
#
# Copyright (c) 2017, Oracle and/or its affiliates. All rights reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# This code is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 only, as
# published by the Free Software Foundation.
#
# This code is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# version 2 for more details (a copy is included in the LICENSE file that
# accompanied this code).
#
# You should have received a copy of the GNU General Public License version
# 2 along with this work; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Please contact Oracle, 500 Oracle Parkway, Redwood Shores, CA 94065 USA
# or visit www.oracle.com if you need additional information or have any
# questions.
#
# ----------------------------------------------------------------------------------------------------

import mx
import os
import shutil

_suite = mx.suite('sdk')

def javadoc(args, vm=None):
    """build the Javadoc for all API packages"""
    mx.javadoc(['--unified', '--exclude-packages', 'org.graalvm.polyglot.tck'] + args)
    javadoc_dir = os.sep.join([_suite.dir, 'javadoc'])
    shutil.move(os.sep.join([javadoc_dir, 'index.html']), os.sep.join([javadoc_dir, 'overview-frames.html']))
    shutil.copy(os.sep.join([javadoc_dir, 'overview-summary.html']), os.sep.join([javadoc_dir, 'index.html']))


class LauncherConfig(object):
    def __init__(self, jar_distributions, main_class, build_args):
        """
        :type jar_distributions: list[str]
        :type main_class: str
        :type build_args: list[str]
        """
        self.jar_distributions = jar_distributions
        self.main_class = main_class
        self.build_args = build_args

        assert isinstance(self.jar_distributions, list)
        assert isinstance(self.build_args, list)


class GraalVmComponent(object):
    def __init__(self, name, id, documentation_files, license_files, third_party_license_files,
                 provided_executables=None, boot_jars=None):
        """
        :type name: str
        :type id: str
        :type documentation_files: list[str]
        :type license_files: list[str]
        :type third_party_license_files: list[str]
        :type provided_executables: list[str]
        :type boot_jars: list[str]
        """
        self.name = name
        self.id = id
        self.documentation_files = documentation_files
        self.license_files = license_files
        self.third_party_license_files = third_party_license_files
        self.provided_executables = provided_executables or []
        self.boot_jars = boot_jars or []

        assert isinstance(self.documentation_files, list)
        assert isinstance(self.license_files, list)
        assert isinstance(self.third_party_license_files, list)
        assert isinstance(self.provided_executables, list)
        assert isinstance(self.boot_jars, list)


class GraalVmTruffleComponent(GraalVmComponent):
    def __init__(self, name, id, documentation_files, license_files, third_party_license_files, truffle_jars,
                 support_distributions=None, launcher_configs=None, provided_executables=None,
                 polyglot_library_build_args=None, boot_jars=None):
        """
        :type truffle_jars: list[str]
        :type support_distributions: list[str]
        :type launcher_configs: list[LauncherConfig]
        :type polyglot_library_build_args: list[str]
        """
        super(GraalVmTruffleComponent, self).__init__(name, id, documentation_files, license_files,
                                                      third_party_license_files, provided_executables, boot_jars)

        self.truffle_jars = truffle_jars
        self.support_distributions = support_distributions or []
        self.launcher_configs = launcher_configs or []
        self.polyglot_library_build_args = polyglot_library_build_args or []

        assert isinstance(self.truffle_jars, list)
        assert isinstance(self.support_distributions, list)
        assert isinstance(self.launcher_configs, list)
        assert isinstance(self.polyglot_library_build_args, list)

class GraalVmLanguage(GraalVmTruffleComponent):
    pass


class GraalVmTool(GraalVmTruffleComponent):
    pass


class GraalVmJvmciComponent(GraalVmComponent):
    def __init__(self, name, id, documentation_files, license_files, third_party_license_files, jvmci_jars,
                 provided_executables=None, boot_jars=None):
        """
        :type jvmci_jars: list[str]
        """
        super(GraalVmJvmciComponent, self).__init__(name, id, documentation_files, license_files,
                                                    third_party_license_files, provided_executables, boot_jars)

        self.jvmci_jars = jvmci_jars or []

        assert isinstance(jvmci_jars, list)


class GraalVmJdkComponent(GraalVmComponent):
    pass


_graalvm_components = []

def register_component(component):
    """
    :type component: GraalVmComponent
    """
    assert not any((c for c in _graalvm_components if c.name == component.name and isinstance(component, c.__class__)))
    _graalvm_components.append(component)


def graalvm_components():
    """
    :rtype: list[GraalVmComponent]
    """
    return _graalvm_components


mx.update_commands(_suite, {
    'javadoc' : [javadoc, '[SL args|@VM options]'],
})
