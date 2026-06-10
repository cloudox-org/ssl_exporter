%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name:    ssl_exporter
Version: 2.4.3
Release: 1%{?dist}
Summary: Prometheus exporter for SSL certificates.
License: ASL 2.0
URL:     https://github.com/ribbybibby/ssl_exporter

Source0: https://github.com/ribbybibby/ssl_exporter/releases/download/v%{version}/%{name}_%{version}_linux_amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default
Source3: https://raw.githubusercontent.com/ribbybibby/%{name}/v%{version}/examples/%{name}.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Prometehus exporter that exports metrics for certificates collected from TCP
probes, local files or Kubernetes secrets. The metrics are labelled with fields
from the certificate, which allows for informational dashboards and flexible
alert routing.

%prep
%setup -q -D -c %{name}_%{version}_linux_amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yml


%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yml

%changelog
* Wed Jun 10 2026 Ivan Garcia <igarcia@cloudox.org> - 2.4.3
- Initial packaging for the 2.4.3 branch
