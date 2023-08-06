# -*- coding: utf-8 -*-
from __future__ import print_function
import textwrap

from dkfileutils.path import Path
from dkpkg.directory import Package
from yamldirs import create_files


def cmptxt(t):
    return textwrap.dedent(t).strip().replace('\\', '/')


def test_extra_args():
    p = Package('foo', version=42)
    assert p.version == 42


def test_is_django():
    files = """
        mypkg:
            mypkg:
                - models.py: ""
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg')
        assert p.is_django()
        assert p.django_models.endswith('.py')


def test_is_django_models_dir():
    files = """
        mypkg:
            mypkg:
                models:
                    - __init__.py: ""
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg')
        assert p.is_django()
        assert not p.django_models.endswith('.py')


def test_is_not_django():
    files = """
        mypkg:
            mypkg: []
                
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg')
        assert not p.is_django()
        assert p.django_models is None


def test_package_repr():
    files = """
        mypkg: []
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg')
        print('repr:\n', repr(p))
        correct = r"""
                        build {root}\mypkg\build
               build_coverage {root}\mypkg\build\coverage
                    build_dir {root}\mypkg\build
                   build_docs {root}\mypkg\build\docs
              build_lintscore {root}\mypkg\build\lintscore
                   build_meta {root}\mypkg\build\meta
                 build_pytest {root}\mypkg\build\pytest
                     coverage {root}\mypkg\build\coverage
                 coverage_dir {root}\mypkg\build\coverage
            django_models_dir {root}\mypkg\mypkg\models
             django_models_py {root}\mypkg\mypkg\models.py
                django_static {root}\mypkg\mypkg\static
             django_templates {root}\mypkg\mypkg\templates
                         docs {root}\mypkg\docs
                     docs_dir {root}\mypkg\docs
                lintscore_dir {root}\mypkg\build\lintscore
                     location {root}
                     meta_dir {root}\mypkg\build\meta
                         name mypkg
                  package_dir {root}\mypkg
                 package_name mypkg
                       public {root}\mypkg\public
                   public_dir {root}\mypkg\public
                   pyroot_dir {root}\mypkg
                   pytest_dir {root}\mypkg\build\pytest
                         root {root}\mypkg
                       source {root}\mypkg\mypkg
                   source_dir {root}\mypkg\mypkg
                    source_js {root}\mypkg\js
                  source_less {root}\mypkg\less
                   static_dir {root}\mypkg\mypkg\static
                templates_dir {root}\mypkg\mypkg\templates
                        tests {root}\mypkg\tests
                    tests_dir {root}\mypkg\tests
                     tests_js {root}\mypkg\tests\js
                """.format(root=r)
        print("CORRECT:\n", correct)
        a = cmptxt(repr(p))
        b = cmptxt(correct)
        # print("A:", a[1050:1400])
        # print("B:", b[1050:1400])
        # assert a[:1100] == b[:1100]
        # assert a[:1150] == b[:1150]
        # assert a[:1200] == b[:1200]
        # assert a[:1600] == b[:1600]
        # print("LEN:A", len(a), len(b))
        # assert a == b
        assert cmptxt(repr(p)) == cmptxt(correct)


def test_write_ini():
    files = """
        mypkg: []
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg')
        assert cmptxt(p.write_ini('foo', 'dkbuild')) == cmptxt(r"""
            [dkbuild]
            root = {root}\mypkg
            location = {root}
            name = mypkg
            docs = {root}\mypkg\docs
            tests = {root}\mypkg\tests
            source = {root}\mypkg\mypkg
            source_js = {root}\mypkg\js
            source_less = {root}\mypkg\less
            build = {root}\mypkg\build
            build_coverage = {root}\mypkg\build\coverage
            build_docs = {root}\mypkg\build\docs
            build_lintscore = {root}\mypkg\build\lintscore
            build_meta = {root}\mypkg\build\meta
            build_pytest = {root}\mypkg\build\pytest
            django_templates = {root}\mypkg\mypkg\templates
            django_static = {root}\mypkg\mypkg\static        
        """.format(root=r))


def test_package_override():
    files = """
        mypkg: []
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg', build=r/'build', source=r/'mypkg/src')
        assert p.location == r
        assert p.root == r / 'mypkg'
        assert p.docs == r / 'mypkg/docs'
        assert p.name == 'mypkg'
        assert p.source == r / 'mypkg/src'
        assert p.source_js == r / 'mypkg/js'
        assert p.source_less == r / 'mypkg/less'
        assert p.django_templates == r / 'mypkg/src/templates'
        assert p.django_static == r / 'mypkg/src/static'
        assert p.build == r / 'build'
        assert p.build_coverage == r / 'build/coverage'
        assert p.build_docs == r / 'build/docs'
        assert p.build_lintscore == r / 'build/lintscore'
        assert p.build_meta == r / 'build/meta'
        assert p.build_pytest == r / 'build/pytest'
        assert p.tests == r / 'mypkg/tests'

        p.make_missing()

        assert p.docs.exists()
        assert p.source.exists()
        assert p.source_js.exists()
        assert p.source_less.exists()
        assert p.build.exists()
        assert p.build_coverage.exists()
        assert p.build_lintscore.exists()
        assert p.build_coverage.exists()
        assert p.build_pytest.exists()
        assert p.django_templates.exists()
        assert p.django_static.exists()
        assert p.tests.exists()
        assert p.is_django()


def test_package_override_name():
    files = """
        my-pkg: []
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('my-pkg', name='foo')
        assert p.location == r
        assert p.root == r / 'my-pkg'
        assert p.docs == r / 'my-pkg/docs'
        assert p.name == 'foo'
        assert p.source == r / 'my-pkg/foo'
        assert p.source_js == r / 'my-pkg/js'
        assert p.source_less == r / 'my-pkg/less'
        assert p.django_templates == r / 'my-pkg/foo/templates'
        assert p.django_static == r / 'my-pkg/foo/static'
        assert p.build == r / 'my-pkg/build'
        assert p.build_coverage == r / 'my-pkg/build/coverage'
        assert p.build_docs == r / 'my-pkg/build/docs'
        assert p.build_lintscore == r / 'my-pkg/build/lintscore'
        assert p.build_meta == r / 'my-pkg/build/meta'
        assert p.build_pytest == r / 'my-pkg/build/pytest'
        assert p.tests == r / 'my-pkg/tests'

        p.make_missing()

        assert p.docs.exists()
        assert p.source.exists()
        assert p.source_js.exists()
        assert p.source_less.exists()
        assert p.build.exists()
        assert p.build_coverage.exists()
        assert p.build_lintscore.exists()
        assert p.build_coverage.exists()
        assert p.build_pytest.exists()
        assert p.django_templates.exists()
        assert p.django_static.exists()
        assert p.tests.exists()
        assert p.is_django()


def test_package_default():
    files = """
        mypkg: []
    """
    with create_files(files) as r:
        r = Path(r)
        print('root', r)
        p = Package('mypkg')
        assert p.location == r
        assert p.root == r / 'mypkg'
        assert p.docs == r / 'mypkg/docs'
        assert p.name == 'mypkg'
        assert p.source == r / 'mypkg/mypkg'
        assert p.source_js == r / 'mypkg/js'
        assert p.source_less == r / 'mypkg/less'
        assert p.django_templates == r / 'mypkg/mypkg/templates'
        assert p.django_static == r / 'mypkg/mypkg/static'
        assert p.build == r / 'mypkg/build'
        assert p.build_coverage == r / 'mypkg/build/coverage'
        assert p.build_docs == r / 'mypkg/build/docs'
        assert p.build_lintscore == r / 'mypkg/build/lintscore'
        assert p.build_meta == r / 'mypkg/build/meta'
        assert p.build_pytest == r / 'mypkg/build/pytest'
        assert p.tests == r / 'mypkg/tests'

        p.make_missing()

        assert p.docs.exists()
        assert p.source.exists()
        assert p.source_js.exists()
        assert p.source_less.exists()
        assert p.build.exists()
        assert p.build_coverage.exists()
        assert p.build_lintscore.exists()
        assert p.build_coverage.exists()
        assert p.build_pytest.exists()
        assert p.django_templates.exists()
        assert p.django_static.exists()
        assert p.tests.exists()
