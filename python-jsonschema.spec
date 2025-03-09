#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	jsonschema
Summary:	An implementation of JSON Schema validation for Python 2
Summary(pl.UTF-8):	Implementacja sprawdzania poprawności schematu JSON dla Pythona 2
Name:		python-%{module}
# keep 3.x here for python2 support
Version:	3.2.0
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/jsonschema/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonschema/%{module}-%{version}.tar.gz
# Source0-md5:	f1a0b5011f05a02a8dee1070cd10a26d
# https://json-schema.org/draft-07/json-schema-validation.html (differrent email hashes generated on each download)
Source1:	json-schema-validation.html
# Source1-md5:	e920693b4c00338d439f0a2240218bcf
Patch0:		%{name}-webcolors.patch
Patch1:		%{name}-nonet.patch
URL:		https://pypi.python.org/pypi/jsonschema
%if %{with python2}
BuildRequires:	python-functools32
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
BuildRequires:	python-vcversioner >= 2.16.0.0
%if %{with tests}
BuildRequires:	python-attrs >= 17.4.0
BuildRequires:	python-idna
BuildRequires:	python-importlib_metadata
BuildRequires:	python-jsonpointer >= 1.14
BuildRequires:	python-pyrsistent >= 0.14.0
BuildRequires:	python-rfc3987
BuildRequires:	python-six >= 1.11.0
BuildRequires:	python-strict_rfc3339
BuildRequires:	python-twisted
BuildRequires:	python-webcolors
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
BuildRequires:	python3-vcversioner >= 2.16.0.0
%if %{with tests}
BuildRequires:	python3-attrs >= 17.4.0
BuildRequires:	python3-idna
%if "%{py3_ver}" < "3.8"
BuildRequires:	python-importlib_metadata
%endif
BuildRequires:	python3-jsonpointer >= 1.14
BuildRequires:	python3-pyrsistent >= 0.14.0
BuildRequires:	python3-rfc3987
BuildRequires:	python3-six >= 1.11.0
# optional, but tests fail if python3-isodate is installed and strict_rfc3339 isn't
BuildRequires:	python3-strict_rfc3339
BuildRequires:	python3-twisted
BuildRequires:	python3-webcolors
%endif
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
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jsonschema is an implementation of JSON Schema
(<https://json-schema.org/>) for Python.

%description -l pl.UTF-8
jsonschema to implementacja JSON Schema (<https://json-schema.org/>)
dla Pythona.

%package -n python3-%{module}
Summary:	An implementation of JSON Schema validation for Python 3
Summary(pl.UTF-8):	Implementacja sprawdzania poprawności schematu JSON dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
jsonschema is an implementation of JSON Schema
(<https://json-schema.org/>) for Python.

%description -n python3-%{module} -l pl.UTF-8
jsonschema to implementacja JSON Schema (<https://json-schema.org/>)
dla Pythona.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1

install -d docs/_cache
cp -p %{SOURCE1} docs/_cache/spec.html

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
trial-2 jsonschema
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
trial-3 jsonschema
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	PYTHON="%{__python3}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jsonschema{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jsonschema{,-3}
ln -sf jsonschema-3 $RPM_BUILD_ROOT%{_bindir}/jsonschema
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst COPYING README.rst
%attr(755,root,root) %{_bindir}/jsonschema-2
%{py_sitescriptdir}/jsonschema
%{py_sitescriptdir}/jsonschema-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG.rst COPYING README.rst
%attr(755,root,root) %{_bindir}/jsonschema
%attr(755,root,root) %{_bindir}/jsonschema-3
%{py3_sitescriptdir}/jsonschema
%{py3_sitescriptdir}/jsonschema-%{version}-py*.egg-info
%endif
