#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	jsonschema
Summary:	An implementation of JSON Schema validation for Python 2
Summary(pl.UTF-8):	Implementacja sprawdzania poprawności schematu JSON dla Pythona 2
Name:		python3-%{module}
# keep 3.x here for python2 support
Version:	4.23.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/jsonschema/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonschema/%{module}-%{version}.tar.gz
# Source0-md5:	a2cb5fee4da011118708ab275b34f30b
# https://json-schema.org/draft-07/json-schema-validation.html (differrent email hashes generated on each download)
Source1:	json-schema-validation.html
# Source1-md5:	e920693b4c00338d439f0a2240218bcf
URL:		https://pypi.python.org/pypi/jsonschema
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-vcversioner >= 2.16.0.0
BuildRequires:	python3-hatchling
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatch-fancy-pypi-readme
%if %{with tests}
BuildRequires:	python3-attrs >= 17.4.0
BuildRequires:	python3-idna
BuildRequires:	python3-jsonpointer >= 1.14
BuildRequires:	python3-pyrsistent >= 0.14.0
BuildRequires:	python3-rfc3987
BuildRequires:	python3-six >= 1.11.0
# optional, but tests fail if python3-isodate is installed and strict_rfc3339 isn't
BuildRequires:	python3-strict_rfc3339
BuildRequires:	python3-twisted
BuildRequires:	python3-webcolors
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-certifi
BuildRequires:	python3-lxml
BuildRequires:	python3-pyrsistent
BuildRequires:	python3-sphinxcontrib-spelling
%endif
Requires:	python3-modules >= 1:3.6
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
cp -p %{SOURCE1} docs/_cache/spec.html

%build
%py3_build_pyproject

%if %{with tests}
PYTHONPATH=$(pwd) \
trial-3 jsonschema
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
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
%attr(755,root,root) %{_bindir}/jsonschema
%attr(755,root,root) %{_bindir}/jsonschema-3
%{py3_sitescriptdir}/jsonschema
%{py3_sitescriptdir}/jsonschema-%{version}.dist-info
