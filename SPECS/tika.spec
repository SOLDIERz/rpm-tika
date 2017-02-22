Name:		tika		
Version:	1.14
Release:	1%{?dist}
Summary:	The Apache Tika toolkit detects and extracts metadata and text from over a thousand different file types

Group:		Applications/Productivity
License:	Apache Software License 2.0 / ASL 2.0
URL:		https://tika.apache.org
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.sysconf
Source2:	%{name}-server.service

BuildRequires:	maven
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	systemd
Requires:		java-1.8.0-openjdk
Requires:		java-1.8.0-openjdk-headless
BuildArch:		noarch

%description
The Apache Tika toolkit detects and extracts metadata and text from over a thousand different file types (such as PPT, XLS, and PDF). All of these file types can be parsed through a single interface, making Tika useful for search engine indexing, content analysis, translation, and much more. You can find the latest release on the download page. Please see the Getting Started page for more information on how to start using Tika.


%package app
Summary: combines tika-core and tika-parsers with a GUI and a command line interface
Group: Applications/Productivity

%description app
Tika application. Combines tika-core, tika-parsers and all the external parser libraries into a single runnable jar with a GUI and a command line interface.


%package batch
Summary: Apache Tika is a toolkit for detecting and extracting metadata
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description batch
Apache Tika is a toolkit for detecting and extracting metadata and
structured text content from various documents using existing parser
libraries.


%package bundle
Summary: OSGi bundle that contains the tika-parsers component and all its upstream dependencies that aren't OSGI bundles by themselves
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description bundle
OSGi bundle that contains the tika-parsers component and all its upstream dependencies that aren't OSGI bundles by themselves. This bundle exports no packages, only the Parser and Detector services from the tika-parsers component.



%package example
Summary: This module contains examples of how to use Apache Tika.
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description example
%{summary}.


%package java7
Summary: Java-7 reliant components, including FileTypeDetector implementations
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description java7
%{summary}.


%package langdetect
Summary: This is the language detection Apache Tika toolkit.
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description langdetect
%{summary}.


%package parsers
Summary: Apache Tika is a toolkit for detecting and extracting metadata and structured text content from various documents using existing parser libraries.
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description parsers
%{summary}.


%package serialization
Summary: Apache Tika is a toolkit for detecting and extracting metadata and structured text content from various documents using existing parser libraries.
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description serialization
%{summary}.


%package server
Summary: Tika JAX-RS REST application. This is a Jetty web server running Tika REST services.
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description server
%{summary}.


%package translate
Summary: This is the translate Apache Tika toolkit. Translator implementations may depend on web services.
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description translate
%{summary}.


%package xmp
Summary: Converts Tika metadata to XMP
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}

%description xmp
%{summary}.


%prep
%setup -q

%build
mvn clean install -Dmaven.test.skip=true

%install


#Creating Application Directory for Tika
%{__mkdir} -p %{buildroot}/opt/%{name}-%{version}

#Installing tika .jar files 
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-app/target/tika-app-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-batch/target/tika-batch-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-bundle/target/tika-bundle-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-core/target/tika-core-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-example/target/tika-example-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-java7/target/tika-java7-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-langdetect/target/tika-langdetect-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-parsers/target/tika-parsers-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-serialization/target/tika-serialization-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-server/target/tika-server-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-translate/target/tika-translate-%{version}.jar %{buildroot}/opt/%{name}-%{version}/
%{__install} -m 644 -p %{_builddir}/%{name}-%{version}/tika-xmp/target/tika-xmp-%{version}.jar %{buildroot}/opt/%{name}-%{version}/

#Creating Folder for tika sysconfig
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig

#Installing tika sysonfig files (includes JAVA_OPTS)
%{__install} -m 644 -p %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

#Creating systemd folder for tika-server.service
%{__mkdir} -p %{buildroot}/%{_unitdir}

#Installing tika-server service
%{__install} -m 644 -p %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-server.service

%post
%systemd_post %{name}-server.service

%preun
%systemd_preun %{name}-server.service

%postun
if [ "$(ls -A /opt/%{name}-%{version})" ]; then
    #do nothing
else
    #clenaup app directory
    %{__rm} -rf /opt/%{name}-%{version}
fi

%systemd_postun_with_restart %{name}-server.service
/bin/systemctl daemon-reload 2> /dev/null



%files
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-core-%{version}.jar

%files app
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-app-%{version}.jar

%files batch
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-batch-%{version}.jar

%files bundle
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-bundle-%{version}.jar

%files example
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-example-%{version}.jar

%files java7
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-java7-%{version}.jar

%files langdetect
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-langdetect-%{version}.jar

%files parsers
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-parsers-%{version}.jar

%files serialization
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-serialization-%{version}.jar

%files server
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-server-%{version}.jar
%{_unitdir}/%{name}-server.service
%{_sysconfdir}/sysconfig/%{name}

%files translate
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-translate-%{version}.jar

%files xmp
%defattr(-,root,root,-)
/opt/%{name}-%{version}/tika-xmp-%{version}.jar



%changelog
* Mon Feb 20 2017 Marcel Fuhrmann <github@mfsystems.me> - 1.14-1
- inital release
