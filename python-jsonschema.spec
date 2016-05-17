#
# Conditional build:
%bcond_without	tests	# nose tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	jsonschema
Summary:	An implementation of JSON Schema validation for Python 2
Summary(pl.UTF-8):	Implementacja sprawdzania poprawności schematu JSON dla Pythona 2
Name:		python-%{module}
Version:	2.5.1
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/jsonschema/
Source0:	https://pypi.python.org/packages/source/j/jsonschema/%{module}-%{version}.tar.gz
# Source0-md5:	374e848fdb69a3ce8b7e778b47c30640
URL:		https://pypi.python.org/pypi/jsonschema
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
%if "%{py_ver}" < "2.7"
BuildRequires:	python-argparse
BuildRequires:	python-repoze.lru
%endif
%if "%{py_ver}" >= "2.7"
BuildRequires:	python-functools32
%endif
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
BuildRequires:	python-vcversioner
%if %{with tets}
BuildRequires:	python-mock
BuildRequires:	python-nose
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-vcversioner
%if %{with tests}
BuildRequires:	python3-nose
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jsonschema is JSON Schema validator currently based on
<http://tools.ietf.org/html/draft-zyp-json-schema-03>.

%description -l pl.UTF-8
jsonschema to walidator schematów JSON oparty na dokumencie
<http://tools.ietf.org/html/draft-zyp-json-schema-03>.

%package -n python3-%{module}
Summary:	An implementation of JSON Schema validation for Python 3
Summary(pl.UTF-8):	Implementacja sprawdzania poprawności schematu JSON dla Pythona 3
Group:		Libraries/Python

%description -n python3-%{module}
jsonschema is JSON Schema validator currently based on
<http://tools.ietf.org/html/draft-zyp-json-schema-03>.

%description -n python3-%{module} -l pl.UTF-8
jsonschema to walidator schematów JSON oparty na dokumencie
<http://tools.ietf.org/html/draft-zyp-json-schema-03>.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%{_bindir}/nosetests-%{py_ver} -v
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{_bindir}/nosetests-%{py3_ver} -v
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jsonschema{,-3}

# pythonegg dependency generator resolves conditionals for requires() based on
# python version that runs the generator, not the version egg is targeted;
# avoid generation of python3egg(functools32) dependency for python 3
%{__sed} -i -e "/^\\[:python_version=='2.[67]']/,/^$/d" $RPM_BUILD_ROOT%{py3_sitescriptdir}/jsonschema-%{version}-py*.egg-info/requires.txt
%endif

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jsonschema{,-2}
ln -sf jsonschema-2 $RPM_BUILD_ROOT%{_bindir}/jsonschema
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst COPYING README.rst
%attr(755,root,root) %{_bindir}/jsonschema
%attr(755,root,root) %{_bindir}/jsonschema-2
%{py_sitescriptdir}/jsonschema
%{py_sitescriptdir}/jsonschema-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG.rst COPYING README.rst
%attr(755,root,root) %{_bindir}/jsonschema-3
%{py3_sitescriptdir}/jsonschema
%{py3_sitescriptdir}/jsonschema-%{version}-py*.egg-info
%endif
