Summary: A RFC 1413 ident protocol daemon
Name: authd
Version: 1.4.3
Release: 30%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: https://fedorahosted.org/authd/
Obsoletes: pidentd <= 3.2
Provides: pidentd = 3.2
Requires(post): openssl
Source0: http://fedorahosted.org/releases/a/u/authd/authd-1.4.3.tar.gz
Patch0: authd-1.4.3-gcc4.patch
Patch1: authd-1.4.3-disable.patch
Patch2: authd-1.4.3-ipv6-mapping.patch
Patch3: authd-1.4.3-locale.patch
Patch4: authd-1.4.3-longopt-identifier.patch
Patch5: authd-1.4.3-jiffies64.patch
Patch6: authd-1.4.3-valist.patch
Patch7: authd-1.4.3-cflags.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel gettext
Requires: xinetd

%description
authd is a small and fast RFC 1413 ident protocol daemon
with both xinetd server and interactive modes that
supports IPv6 and IPv4 as well as the more popular features
of pidentd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .ipv6map
%patch3 -p1 -b .locale
%patch4 -p1
%patch5 -p1 -b .jiffies64
%patch6 -p1 -b .valist
%patch7 -p1 -b .cflags
sed -i -e "s|/etc|%{_sysconfdir}|" config.h

%build
CFLAGS=$RPM_OPT_FLAGS make prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/xinetd.d

install -m 644 xinetd.conf.auth ${RPM_BUILD_ROOT}%{_sysconfdir}/xinetd.d/auth
sed -i -e 's|/usr/local|/usr|' ${RPM_BUILD_ROOT}%{_sysconfdir}/xinetd.d/auth

touch ${RPM_BUILD_ROOT}%{_sysconfdir}/ident.key

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/adduser -s /sbin/nologin -u 98 -r -d '/' ident 2>/dev/null || true
/usr/bin/openssl rand -base64 -out %{_sysconfdir}/ident.key 32
echo CHANGE THE LINE ABOVE TO A PASSPHRASE >> %{_sysconfdir}/ident.key
/bin/chown ident:ident %{_sysconfdir}/ident.key
chmod o-rw %{_sysconfdir}/ident.key

%postun
service xinetd reload

%files -f authd.lang
%defattr(-,root,root,-)
%verify(not md5 size mtime user group) %config(noreplace) %attr(640, root, root) %{_sysconfdir}/ident.key
%doc COPYING README.html rfc1413.txt
%config(noreplace) %{_sysconfdir}/xinetd.d/auth
%{_sbindir}/in.authd

%changelog
* Mon Jun 14 2010 Roman Rakus <rrakus@redhat.com> - 1.4.3-30
- Use only once defattr macro
  Resolves: #596150

* Wed Feb 24 2010 Roman Rakus <rrakus@redhat.com> - 1.4.3-29
- Use RPM_OPT_FLAGS for CFLAGS in build section

* Fri Dec 11 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.4.3-28.1
- Rebuilt for RHEL 6

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.3-28
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Roman Rakus <rrakus@redhat.com> - 1.4.3-26
- get back to older version of jiffies64 patch

* Tue Mar 31 2009 Roman Rakus <rrakus@redhat.com> - 1.4.3-25
- Fixed source tag

* Tue Mar 31 2009 Roman Rakus <rrakus@redhat.com> - 1.4.3-24
- Fixed using valist with log option on.
  Resolves: #446844
- user ident has home dir set to /
  Resolves: #458144

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.3-22
- rebuild with new openssl

* Wed Jul 23 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-21
- Corrected config directive for ident.key to noreplace
- Fixed some typos in specfile

* Tue Apr 29 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-20
- another corrections of jiffies64 patch

* Wed Mar 26 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-19
- corrected jiffies64 patch

* Thu Mar  6 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-18
- corrected Source0
- corrected link in URL
- source added to svn on fedorahosted

* Wed Mar  5 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-16
- fixed Source0

* Wed Mar  5 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-15
- added dist tag
- added URL

* Tue Feb 26 2008 Roman Rakus <rrakus@redhat.com> - 1.4.3-14
- fix 234262 bug

* Wed Feb 13 2008 Jan Safranek <jsafrane@redhat.com> - 1.4.3-13
- fix rpmlint errors

* Tue Feb 12 2008 Jan Safranek <jsafrane@redhat.com> - 1.4.3-12
- fix build with new gcc

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.4.3-11
- Rebuild for deps

* Wed Sep 19 2007 Ondrej Dvoracek <odvorace@redhat.com> - 1.4.3-10
- corrected illegal identifier in longopt enumeration (#245436)
- corrected summary and license

* Mon Jul 24 2006 Martin Stransky <stransky@redhat.com> - 1.4.3-9
- added locale patch (#199721)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.3-8.1
- rebuild

* Sun May 28 2006 Martin Stransky <stransky@redhat.com> - 1.4.3-8
- added gettext dependency (#193350)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.3-7.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Martin Stransky <stransky@redhat.com> - 1.4.3-7
- re-tag

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.3-6.devel.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 8  2005 Martin Stransky <stransky@redhat.com>
- rebuilt

* Thu Jun 24 2005 Martin Stransky <stransky@redhat.com> - 1.4.3-5.devel
- add xinetd to Prereq
- fix for #150502 (authd doesn't map IPv6 to IPv4 from xinetd)

* Fri Apr  8 2005 Martin Stransky <stransky@redhat.com> - 1.4.3-4.devel
- clear last update

* Fri Apr  8 2005 Martin Stransky <stransky@redhat.com> - 1.4.3-3.devel
- delete user "ident" after uninstalation

* Thu Apr  7 2005 Martin Stransky <stransky@redhat.com> - 1.4.3-2.devel
- in.authd disabled by default (#151905)

* Mon Mar  7 2005 Martin Stransky <stransky@redhat.com> - 1.4.3-1.devel
- update to 1.4.3
- gcc4.0 patch
- add post-uninstall reconfiguration (#150460)

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Fri Oct 15 2004 Adrian Havill <havill@redhat.com> - 1.4.2-8
- tweak setting of uid/gid for key file so systems with no prior
  ident user/group don't generate a warning (#135837)

* Thu Oct 14 2004 Adrian Havill <havill@redhat.com> - 1.4.2-4
- slightly better error checking for insane cases
- tweak of the openssl requires dependency loop (#131291)
- as ident.key is created in %%post, tweak so verify passes (#131530)
- make the uid/gid for ident conform to the past (#135752)

* Wed Jul 28 2004 Adrian Havill <havill@redhat.com> - 1.4.1-1
- only scan for ESTABLISHED connections
- extra debug output for crypto

* Mon Jul 26 2004 Adrian Havill <havill@redhat.com> - 1.4.0-1
- revise makefile; don't over-optimize as gcc can produce bad code
- ptr cleanup when multiquery and missing /proc/net/tcp*
- improve create_opt (error handling, debugging, identifiers)
- add --prefix option for matching IPv4 to IPv6

* Tue Jul 13 2004 Adrian Havill <havill@redhat.com> - 1.3.4-1
- retry reading proc with pauses to reduce false negatives
- match IPv4 addresses against IPv6 compatibility addresses

* Mon Jul 12 2004 Adrian Havill <havill@redhat.com> - 1.3.3-1
- use gnu *_unlocked stream funcs for faster I/O

* Sat Jul 10 2004 Adrian Havill <havill@redhat.com> - 1.3.2-1
- enforce rfc restriction limiting port search to the connected
  local/foreign pair

* Fri Jul 08 2004 Adrian Havill <havill@redhat.com> - 1.3.1-1
- increase default connections-per-sec/max-instances for HP
- more doc cleanup
- remove unnecessary rootdir check for -N/--ident

* Fri Jul 02 2004 Adrian Havill <havill@redhat.com> - 1.3.0-1
- add unknown-error only -e option
- edit readme, add rfc to docdir
- code cleanup; remove static buffers, orthagonalize id names
- ipv6 hybrid addr zero run correction
- extra eight bits added to random key

* Wed Jun 30 2004 Adrian Havill <havill@redhat.com> - 1.2.8-1
- zero out invalid port(s)

* Tue Jun 29 2004 Adrian Havill <havill@redhat.com> - 1.2.7-1
- added Provides to satisfy HP pkg rpm dep (#121447, #111640)
- more code cleanup; minimize --resolve dns lookups

* Mon Jun 28 2004 Adrian Havill <havill@redhat.com> - 1.2.6-1
- incorporated suggestions from Thomas Zehetbauer (#124914)

* Sat Jun 26 2004 Adrian Havill <havill@redhat.com> - 1.2.5-1
- clean up src

* Thu Jun 24 2004 Adrian Havill <havill@redhat.com> - 1.2.4-1
- code vet and minor changes re alan@'s comments
- default operating mode to alias all usernames as 'nobody'
  to prevent noobies from getting their mail addr harvested
- clean up README documentation

* Wed Jun 23 2004 Adrian Havill <havill@redhat.com> - 1.2.3-1
- mark xinetd conf file as a noreplace config file
- more robust error checking for proper rfc1413 tokens

* Tue Jun 22 2004 Adrian Havill <havill@redhat.com> - 1.2.1-1
- add Requires and BuildRequires

* Mon Jun 21 2004 Adrian Havill <havill@redhat.com> - 1.2.0-1
- A few tweaks in the cmdline options for orthagonality
- minor bug fix regarding reading from stdin in some multiquery cmdline cases
- add --resolve

* Sun Jun 20 2004 Adrian Havill <havill@redhat.com> - 1.1.0-1
- add extra options for --help, --usage

* Sat Jun 19 2004 Adrian Havill <havill@redhat.com> - 1.0.0-2
- Obsolete pidentd -- authd and pidentd can't/shouldn't coexist on FC/RHEL
- license tweak to allow openssl under any condition
- no spec url needed; package is not worthy enough.

* Fri Jun 18 2004 Jens Petersen <petersen@redhat.com> - 1.0.0-1
- Initial packaging
