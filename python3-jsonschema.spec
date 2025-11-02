#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (fails on some missing references as of 4.25.0)
%bcond_without	tests	# unit tests

%define		module	jsonschema
Summary:	An implementation of JSON Schema validation for Python 3
Summary(pl.UTF-8):	Implementacja sprawdzania poprawności schematu JSON dla Pythona 3
Name:		python3-%{module}
Version:	4.25.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jsonschema/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonschema/%{module}-%{version}.tar.gz
# Source0-md5:	94a6dbde3151edcf8e102e2fe229a498
URL:		https://pypi.org/project/jsonschema
BuildRequires:	python3-build
BuildRequires:	python3-hatch-fancy-pypi-readme
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
BuildRequires:	python3-attrs >= 22.2.0
BuildRequires:	python3-fqdn
BuildRequires:	python3-idna
BuildRequires:	python3-isoduration
BuildRequires:	python3-jsonpath-ng
BuildRequires:	python3-jsonpointer >= 1.14
BuildRequires:	python3-jsonschema-specifications >= 2023.03.6
BuildRequires:	python3-referencing >= 0.28.4
BuildRequires:	python3-rfc3339_validator
BuildRequires:	python3-rfc3986_validator >= 0.1.1
BuildRequires:	python3-rfc3987
BuildRequires:	python3-rfc3987_syntax >= 1.1.0
BuildRequires:	python3-rpds-py >= 0.7.1
BuildRequires:	python3-uri-template
BuildRequires:	python3-virtue
BuildRequires:	python3-webcolors >= 24.6.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-lxml
BuildRequires:	python3-sphinx_autoapi
BuildRequires:	python3-sphinx_autodoc_typehints
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_json_schema_spec
BuildRequires:	python3-sphinxcontrib-spelling
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jsonschema is an implementation of JSON Schema
(<https://json-schema.org/>) for Python.

%description -l pl.UTF-8
jsonschema to implementacja JSON Schema (<https://json-schema.org/>)
dla Pythona.

%prep
%setup -q -n %{module}-%{version}

install -d docs/_cache
cp -p %{py3_sitescriptdir}/sphinx_json_schema_spec/_cache/*.html docs/_cache

%build
%py3_build_pyproject

%if %{with tests} || %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
%endif

%if %{with tests}
JSON_SCHEMA_TEST_SUITE=$(pwd)/json \
PYTHONPATH=$(pwd)/build-3-test \
trial-3 jsonschema
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3-test \
%{__make} -C docs html \
	PYTHON=%{__python3}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jsonschema{,-3}
ln -sf jsonschema-3 $RPM_BUILD_ROOT%{_bindir}/jsonschema

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst COPYING README.rst
%attr(755,root,root) %{_bindir}/jsonschema-3
%{_bindir}/jsonschema
%{py3_sitescriptdir}/jsonschema
%{py3_sitescriptdir}/jsonschema-%{version}.dist-info
