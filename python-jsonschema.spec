#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	jsonschema
Summary:	An implementation of JSON Schema validation for Python
Name:		python-%{module}
Version:	2.4.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/j/jsonschema/%{module}-%{version}.tar.gz
# Source0-md5:	661f85c3d23094afbb9ac3c0673840bf
URL:		http://pypi.python.org/pypi/jsonschema
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-argparse
BuildRequires:	python-mock
BuildRequires:	python-modules
BuildRequires:	python-nose
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-nose
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jsonschema is JSON Schema validator currently based on
<http://tools.ietf.org/html/draft-zyp-json-schema-03>.

%package -n python3-%{module}
Summary:	An implementation of JSON Schema validation for Python
Group:		Libraries/Python

%description -n python3-%{module}
jsonschema is JSON Schema validator currently based on
<http://tools.ietf.org/html/draft-zyp-json-schema-03>.

%prep
%setup -q -n %{module}-%{version}

set -- *
install -d py3
cp -a "$@" py3
find py3 -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%if %{with python3}
cd py3
	%{__python3} setup.py build
cd ..
%endif
%{__python} setup.py build

%if %{with tests}
%if %{with python3}
cd py3
%{_bindir}/nosetests-%{py3_ver} -v
cd ..
%endif
%{_bindir}/nosetests-%{py_ver} -v
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
cd py3
%{__python3} setup.py install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ..
%endif

%if %{with python2}
%{__python} setup.py install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst COPYING
%attr(755,root,root) %{_bindir}/jsonschema
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst COPYING
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
