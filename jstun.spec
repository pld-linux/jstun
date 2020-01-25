# Conditional build:
%bcond_without	source		# don't build source jar


Summary:	A Java-based STUN server
Summary(pl.UTF-8):	Serwer STUN napisany w języku Java.
Name:		jstun
Version:	0.7.3
Release:	1
License:	GPL v2 or Apache v2
Group:		Development/Languages/Java
Source0:	http://jstun.javawi.de/%{name}-%{version}.src.tar.gz
# Source0-md5:	0e2e0c5d52ba339a33472fc3a492e96d
Source1:	%{name}.sysconfig
Source2:	%{name}.init
Source3:	%{name}.sh
URL:		http://jstun.javawi.de
BuildRequires:	ant
BuildRequires:	jar
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{with source}
BuildRequires:	rpmbuild(macros) >= 1.555
%endif
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	java-slf4j
Requires:	jpackage-utils
Requires:	rc-scripts
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
"JSTUN" is a Java-based STUN (Simple Traversal of User Datagram
Protocol (UDP) Through Network Address Translation (NAT))
implementation. STUN provides a mean for applications to discover the
presence and type of firewalls or NATs between them and the public
internet. Additionally, in presence of a NAT STUN can be used by
applications to learn the public Internet Protocol (IP) address
assigned to the NAT.

So far, most of the message headers and attributes as standardized in
RFC 3489 are part of "JSTUN". The current "JSTUN" version also
includes a STUN client and a STUN server.

%package source
Summary:	Source code of %{name}
Summary(pl.UTF-8):	Kod źródłowy %{name}
Group:		Documentation

%description source
Source code of %{name}.

%description source -l pl.UTF-8
Kod źródłowy %{name}.

%prep
%setup -q -n STUN

%build
export JAVA_HOME="%{java_home}"

export CLASSPATH

cd build
%ant
cd ..

cd src
%if %{with source}
%jar cf ../%{name}.src.jar $(find -name '*.java')
%endif
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install -d $RPM_BUILD_ROOT%{_sbindir}

install -d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

# jars
cp -a target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{name}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{name}.src.jar

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/jstun

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi


%files
%defattr(644,root,root,755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%attr(755,root,root) %{_sbindir}/jstun
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%if %{with source}
%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{name}.src.jar
%endif
