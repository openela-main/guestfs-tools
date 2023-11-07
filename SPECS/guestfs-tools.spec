# Architectures that we run the test suite on.
#
# As the test suite takes a very long time to run and is somewhat
# unreliable on !x86 architectures, only run it on x86-64.
%global test_arches x86_64

# Verify tarball signature with GPGv2.
%global verify_tarball_signature 1

# If there are patches which touch autotools files, set this to 1.
%global patches_touch_autotools 1

# The source directory.
%global source_directory 1.50-stable

# Filter perl provides.
%{?perl_default_filter}

Summary:       Tools to access and modify virtual machine disk images
Name:          guestfs-tools
Version:       1.50.1
Release:       3%{?dist}
License:       GPLv2+

# Build only for architectures that have a kernel
ExclusiveArch: %{kernel_arches}
%if 0%{?rhel}
# No qemu-kvm on POWER (RHBZ#1946532).
ExcludeArch: %{power64}
%endif

# Source and patches.
URL:           http://libguestfs.org/
Source0:       http://download.libguestfs.org/guestfs-tools/%{source_directory}/%{name}-%{version}.tar.gz
%if 0%{verify_tarball_signature}
Source1:       http://download.libguestfs.org/guestfs-tools/%{source_directory}/%{name}-%{version}.tar.gz.sig
%endif

# Keyring used to verify tarball signature.
%if 0%{verify_tarball_signature}
Source2:       libguestfs.keyring
%endif

# Maintainer script which helps with handling patches.
Source3:       copy-patches.sh

# Patches are maintained in the following repository:
# https://github.com/rwmjones/guestfs-tools/commits/rhel-9.3

# Patches.
Patch0001:     0001-RHEL-Reject-use-of-libguestfs-winsupport-features-ex.patch
Patch0002:     0002-RHEL-builder-Disable-opensuse-repository.patch
Patch0003:     0003-Remove-virt-dib.patch
Patch0004:     0004-drivers-Look-up-vendor-and-device-names-in-PCI-and-U.patch
Patch0005:     0005-update-common-submodule.patch
Patch0006:     0006-inspector-rename-VGs-and-LVs-in-LUKS-on-LVM-test.patch
Patch0007:     0007-inspector-test-dev-mapper-VG-LV-translation-in-LUKS-.patch

%if 0%{patches_touch_autotools}
BuildRequires: autoconf, automake, libtool, gettext-devel
%endif

# Basic build requirements.
BuildRequires: gcc, gcc-c++
BuildRequires: make
BuildRequires: libguestfs-devel >= 1:1.49.8-1
BuildRequires: libguestfs-xfs
BuildRequires: perl(Pod::Simple)
BuildRequires: perl(Pod::Man)
BuildRequires: perl(Module::Build)
BuildRequires: perl(Test::More)
BuildRequires: /usr/bin/pod2text
BuildRequires: po4a
BuildRequires: pcre2-devel
BuildRequires: libxml2-devel
BuildRequires: jansson-devel
BuildRequires: libvirt-devel
BuildRequires: libosinfo-devel
BuildRequires: libxcrypt-devel
BuildRequires: ncurses-devel
%ifarch x86_64
BuildRequires: glibc-static
%endif
BuildRequires: ocaml-libguestfs-devel
BuildRequires: ocaml-findlib-devel
BuildRequires: ocaml-gettext-devel
%if !0%{?rhel}
BuildRequires: ocaml-ounit-devel
%endif
BuildRequires: flex
BuildRequires: bison
BuildRequires: xz-devel
%if !0%{?rhel}
BuildRequires: zip
BuildRequires: unzip
%endif
%if !0%{?rhel}
BuildRequires: perl(Expect)
%endif
BuildRequires: bash-completion
BuildRequires: /usr/bin/qemu-img
BuildRequires: xorriso
BuildRequires: hwdata-devel
BuildRequires: perl(Locale::TextDomain)
BuildRequires: perl(Sys::Guestfs)
BuildRequires: perl(Win::Hivex)
BuildRequires: perl(Win::Hivex::Regedit)
BuildRequires: perl-generators

%if 0%{verify_tarball_signature}
BuildRequires: gnupg2
%endif

# Ensure a minimum version of libguestfs is installed.  This contains
# a workaround for openssl bug RHBZ#2133884 and the hang where we
# called setenv between fork and exec.
Requires:      libguestfs >= 1.49.6-1

# For virt-builder:
Requires:      curl
Requires:      gnupg2
Requires:      /usr/bin/qemu-img
Requires:      xz

# For virt-builder-repository:
Suggests:      osinfo-db

# For virt-drivers:
Recommends:    hwdata

# For virt-inspector, since Fedora and RHEL >= 7 use XFS:
Recommends:    libguestfs-xfs

# For virt-edit and virt-customize:
Suggests:      perl

# This replaces the libguestfs-tools-c package.
Provides:      libguestfs-tools-c = 1:%{version}-%{release}
Obsoletes:     libguestfs-tools-c <= 1:1.45.2-1


%description
guestfs-tools is a set of tools that can be used to make batch
configuration changes to guests, get disk used/free statistics
(virt-df), perform backups and guest clones, change
registry/UUID/hostname info, build guests from scratch (virt-builder)
and much more.

Virt-alignment-scan scans virtual machines looking for partition
alignment problems.

Virt-builder is a command line tool for rapidly making disk images
of popular free operating systems.

Virt-cat is a command line tool to display the contents of a file in a
virtual machine.

Virt-customize is a command line tool for customizing virtual machine
disk images.

Virt-df is a command line tool to display free space on virtual
machine filesystems.  Unlike other tools, it doesn’t just display the
amount of space allocated to a virtual machine, but can look inside
the virtual machine to see how much space is really being used.  It is
like the df(1) command, but for virtual machines, except that it also
works for Windows virtual machines.

Virt-diff shows the differences between virtual machines.

Virt-drivers detects the bootloader, kernel and drivers inside a guest.

Virt-edit is a command line tool to edit the contents of a file in a
virtual machine.

Virt-filesystems is a command line tool to display the filesystems,
partitions, block devices, LVs, VGs and PVs found in a disk image
or virtual machine.  It replaces the deprecated programs
virt-list-filesystems and virt-list-partitions with a much more
capable tool.

Virt-format is a command line tool to erase and make blank disks.

Virt-get-kernel extracts a kernel/initrd from a disk image.

Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.

Virt-log is a command line tool to display the log files from a
virtual machine.

Virt-ls is a command line tool to list out files in a virtual machine.

Virt-make-fs is a command line tool to build a filesystem out of
a collection of files or a tarball.

Virt-resize can resize existing virtual machine disk images.

Virt-sparsify makes virtual machine disk images sparse (thin-provisioned).

Virt-sysprep lets you reset or unconfigure virtual machines in
preparation for cloning them.

Virt-tail follows (tails) a log file within a guest, like 'tail -f'.


%package -n virt-win-reg
Summary:       Access and modify the Windows Registry of a Windows VM
License:       GPLv2+
BuildArch:     noarch

# This replaces the libguestfs-tools package.
Provides:      libguestfs-tools = 1:%{version}-%{release}
Obsoletes:     libguestfs-tools <= 1:1.45.2-1


%description -n virt-win-reg
Virt-win-reg lets you look at and modify the Windows Registry of
Windows virtual machines.


%package bash-completion
Summary:       Bash tab-completion scripts for %{name}
BuildArch:     noarch
Requires:      bash-completion >= 2.0
Requires:      %{name} = %{version}-%{release}


%description bash-completion
Install this package if you want intelligent bash tab-completion
for the virt-* tools.


%package man-pages-ja
Summary:       Japanese (ja) man pages for %{name}
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}

%description man-pages-ja
%{name}-man-pages-ja contains Japanese (ja) man pages
for %{name}.


%package man-pages-uk
Summary:       Ukrainian (uk) man pages for %{name}
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}

%description man-pages-uk
%{name}-man-pages-uk contains Ukrainian (uk) man pages
for %{name}.


%prep
%if 0%{verify_tarball_signature}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%setup -q
%autopatch -p1

%if 0%{patches_touch_autotools}
autoreconf -i
%endif


%build
%{configure}

# Building index-parse.c by hand works around a race condition in the
# autotools cruft, where two or more copies of yacc race with each
# other, resulting in a corrupted file.
make -j1 -C builder index-parse.c

make V=1 %{?_smp_mflags}


%check
%ifarch %{test_arches}
# Only run the tests with non-debug (ie. non-Rawhide) kernels.
# XXX This tests for any debug kernel installed.
if grep CONFIG_DEBUG_MUTEXES=y /lib/modules/*/config ; then
    echo "Skipping tests because debug kernel is installed"
    exit 0
fi

# Enable debugging.
export LIBGUESTFS_DEBUG=1
export LIBGUESTFS_TRACE=1

# This test is currently broken and needs further investigation.
export SKIP_TEST_MACHINE_READABLE_SH=1

# This test fails for me in local mock and Koji, but not when running
# in an unrestricted environment.
export SKIP_TEST_VIRT_FORMAT_SH=1

# This test takes too long to run under Koji and times out.  It runs
# fine with KVM enabled.
export SKIP_TEST_VIRT_RESIZE_PL=1

if ! make check -k ; then
    # Dump out the log files of any failing tests to make
    # debugging test failures easier.
    for f in `find -name test-suite.log | xargs grep -l ^FAIL:`; do
        echo '*****' $f '*****'
        cat $f
        echo
    done
    exit 1
fi
%endif


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Delete libtool files.
find $RPM_BUILD_ROOT -name '*.la' -delete

# Move installed documentation back to the source directory so
# we can install it using a %%doc rule.
mv $RPM_BUILD_ROOT%{_docdir}/%{name} installed-docs
gzip --best installed-docs/*.xml

# Find locale files.
%find_lang %{name}


# Fix upgrades from old libguestfs-tools-c package
# which had /etc/virt-builder -> xdg/virt-builder.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement/
# This can be removed in Fedora > 36.
%pretrans -p <lua>
path = "/etc/virt-builder"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end


%files -f %{name}.lang
%license COPYING
%doc README
%doc installed-docs/*
%dir %{_sysconfdir}/virt-builder
%dir %{_sysconfdir}/virt-builder/repos.d
%config(noreplace) %{_sysconfdir}/virt-builder/repos.d/*
%{_bindir}/virt-alignment-scan
%{_bindir}/virt-builder
%{_bindir}/virt-builder-repository
%{_bindir}/virt-cat
%{_bindir}/virt-customize
%{_bindir}/virt-df
%{_bindir}/virt-diff
%{_bindir}/virt-drivers
%{_bindir}/virt-edit
%{_bindir}/virt-filesystems
%{_bindir}/virt-format
%{_bindir}/virt-get-kernel
%{_bindir}/virt-index-validate
%{_bindir}/virt-inspector
%{_bindir}/virt-log
%{_bindir}/virt-ls
%{_bindir}/virt-make-fs
%{_bindir}/virt-resize
%{_bindir}/virt-sparsify
%{_bindir}/virt-sysprep
%{_bindir}/virt-tail
%{_mandir}/man1/guestfs-tools-release-notes-1*.1*
%{_mandir}/man1/virt-alignment-scan.1*
%{_mandir}/man1/virt-builder-repository.1*
%{_mandir}/man1/virt-builder.1*
%{_mandir}/man1/virt-cat.1*
%{_mandir}/man1/virt-customize.1*
%{_mandir}/man1/virt-df.1*
%{_mandir}/man1/virt-diff.1*
%{_mandir}/man1/virt-drivers.1*
%{_mandir}/man1/virt-edit.1*
%{_mandir}/man1/virt-filesystems.1*
%{_mandir}/man1/virt-format.1*
%{_mandir}/man1/virt-get-kernel.1*
%{_mandir}/man1/virt-index-validate.1*
%{_mandir}/man1/virt-inspector.1*
%{_mandir}/man1/virt-log.1*
%{_mandir}/man1/virt-ls.1*
%{_mandir}/man1/virt-make-fs.1*
%{_mandir}/man1/virt-resize.1*
%{_mandir}/man1/virt-sparsify.1*
%{_mandir}/man1/virt-sysprep.1*
%{_mandir}/man1/virt-tail.1*


%files -n virt-win-reg
%license COPYING
%doc README
%{_bindir}/virt-win-reg
%{_mandir}/man1/virt-win-reg.1*


%files bash-completion
%license COPYING
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/virt-*


%files man-pages-ja
%lang(ja) %{_mandir}/ja/man1/*.1*


%files man-pages-uk
%lang(uk) %{_mandir}/uk/man1/*.1*


%changelog
* Thu Jun 08 2023 Laszlo Ersek <lersek@redhat.com> - 1.50.1-3
- let virt-inspector recognize "--key /dev/mapper/VG-LV:key:password"
- reenable "make check"; we now use "-cpu max" (libguestfs 30f74f38bd6e)
  resolves: rhbz#2209280

* Thu Apr 06 2023 Richard W.M. Jones <rjones@redhat.com> - 1.50.1-1
- Rebase to guestfs-tools 1.50.1
  resolves: rhbz#2168626
- Fix virt-drivers inspection of RHEL 9.2 guests
  resolves: rhbz#2184963

* Thu Nov 24 2022 Richard W.M. Jones <rjones@redhat.com> - 1.48.2-8
- Support Rocky Linux in virt-customize
  resolves: rhbz#2133443
- Disable OpenSUSE repo in virt-builder
  resolves: rhbz#2145160

* Fri Jul 15 2022 Richard W.M. Jones <rjones@redhat.com> - 1.48.2-5
- Rebase to guestfs-tools 1.48.2
  resolves: rhbz#2059286
- Default to --selinux-relabel in various tools
  resolves: rhbz#2075718, rhbz#2089748
- Add lvm system.devices cleanup operation to virt-sysprep
  resolves: rhbz#2072493
- Refactor virt-customize --install, --update options in common submodule
- Add support for Clevis & Tang
  resolves: rhbz#1809453
- Fix CVE-2022-2211 Denial of Service in --key parameter
  resolves: rhbz#2102721
- Fix virt-sysprep and LUKS-on-LVM guests
  resolves: rhbz#2106286

* Sat Dec 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-6
- Clean up NetworkManager connection files
- Add the copy-patches.sh script from virt-v2v
  resolves: rhbz#1980922

* Tue Nov 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-5
- Fix detection of Kylin Desktop
  resolves: rhbz#2025950

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.46.1-4.1
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-3.el9.1
- Add gating tests (for RHEL 9)

* Mon May 17 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-3
- Fix virt-win-reg --version
  resolves: rhbz#1961160

* Thu May 13 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-2
- BR perl-generators so deps of virt-win-reg subpackage are correct.
  resolves: rhbz#1960191

* Sat May 08 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.1-1
- New stable branch version 1.46.1.

* Tue Apr 27 2021 Richard W.M. Jones <rjones@redhat.com> - 1.46.0-1
- New stable branch version 1.46.0.

* Wed Apr 07 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.3-4
- Use Epoch 1 for virt-dib subpackage (only).

* Wed Mar 31 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.3-3
- Add BR xorriso, needed to run the tests.

* Mon Mar 29 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.3-1
- New upstream version 1.45.3.
- Fix symlink replacement of virt-builder directory (RHBZ#1943838).

* Fri Mar 26 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-5
- Skip test-virt-resize.pl that takes too long to run.

* Thu Mar 25 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-4
- Add perl(Test::More) dependency for the Perl test suite.
- Add perl(Module::Build) dependency for the Perl bindings.
- Fix ounit2 dependency again.

* Wed Mar 24 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-2
- Add perl(Locale::TextDomain) dependency for virt-win-reg.
- Fix ounit2 dependency upstream.

* Tue Mar 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.45.2-1
- New guestfs-tools package, split off from libguestfs.
