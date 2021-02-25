Name: fccAddModule
Version: 1
Release: 1
Summary: Creates module and assembly files in the flexible content format
License: MIT

%description
Creates module and assembly files in the flexible content format

%build
pyinstaller --onefile ~/fccAddModule/addModule.py

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/dist/addModule %{buildroot}%{_bindir}/fccAddModule

%files
%{_bindir}/fccAddModule