#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname			qtpurchasing
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Purchasing library
Summary(pl.UTF-8):	Biblioteka Qt5 Purchasing
Name:		qt5-%{orgname}
Version:	5.15.6
Release:	1
License:	LGPL v3+ or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	beef9ec9e04c49d53a9d18653f3b129b
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Purchasing library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Purchasing.

%package -n Qt5Purchasing
Summary:	The Qt5 Purchasing library
Summary(pl.UTF-8):	Biblioteka Qt5 Purchasing
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Network >= %{qtbase_ver}

%description -n Qt5Purchasing
Qt Purchasing is an add-on library that enables Qt applications to
support in-app purchases. It is a cross-platform library that
currently supports purchases made to the Mac App Store on OS X, App
Store on iOS, and Google Play on Android.

%description -n Qt5Purchasing -l pl.UTF-8
Qt Purchasing to biblioteka dodatkowa umożliwiająca obsługę zakupów
wewnątrz aplikacji z poziomu aplikacji Qt. Jest to biblioteka
wieloplatformowa; obecnie obsługuje zakupy wykonywane poprzez Mac App
Store na OS X, App Store na iOS oraz Google Play na Androidzie.

%package -n Qt5Purchasing-devel
Summary:	Qt5 Purchasing library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Purchasing - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Purchasing = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}

%description -n Qt5Purchasing-devel
Qt5 Purchasing library - development files.

%description -n Qt5Purchasing-devel -l pl.UTF-8
Biblioteka Qt5 Purchasing - pliki programistyczne.

%package doc
Summary:	Qt5 Purchasing documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Purchasing w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Purchasing documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Purchasing w formacie HTML.

%package doc-qch
Summary:	Qt5 Purchasing documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Purchasing w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Purchasing documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Purchasing w formacie QCH.

%package examples
Summary:	Qt5 Purchasing examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Purchasing
License:	BSD or commercial
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Purchasing examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Purchasing.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/purchasing

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Purchasing -p /sbin/ldconfig
%postun	-n Qt5Purchasing -p /sbin/ldconfig

%files -n Qt5Purchasing
%defattr(644,root,root,755)
%doc dist/changes-*
# R: Qt5Core
%attr(755,root,root) %{_libdir}/libQt5Purchasing.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Purchasing.so.5
%dir %{qt5dir}/qml/QtPurchasing
# R: Qt5Core Qt5Purchasing Qt5Qml
%attr(755,root,root) %{qt5dir}/qml/QtPurchasing/libdeclarative_purchasing.so
%{qt5dir}/qml/QtPurchasing/plugins.qmltypes
%{qt5dir}/qml/QtPurchasing/qmldir

%files -n Qt5Purchasing-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Purchasing.so
%{_libdir}/libQt5Purchasing.prl
%{_includedir}/qt5/QtPurchasing
%{_pkgconfigdir}/Qt5Purchasing.pc
%{_libdir}/cmake/Qt5Purchasing
%{qt5dir}/mkspecs/modules/qt_lib_purchasing.pri
%{qt5dir}/mkspecs/modules/qt_lib_purchasing_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtpurchasing

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtpurchasing.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
