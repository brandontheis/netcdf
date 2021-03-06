# AltCCRPMS
%global _prefix /opt/%{name}/%{version}
%global _sysconfdir %{_prefix}/etc
%global _defaultdocdir %{_prefix}/share/doc
%global _infodir %{_prefix}/share/info
%global _mandir %{_prefix}/share/man

%global _cc_name intel
%global _cc_name_suffix -%{_cc_name}

#We don't want to be beholden to the proprietary libraries
%global    _use_internal_dependency_generator 0
%global    __find_requires %{nil}

# Non gcc compilers don't generate build ids
%undefine _missing_build_ids_terminate_build

%global shortname netcdf

Name:           netcdf42%{?_cc_name_suffix}
Version:        4.2.1.1
Release:        1%{?dist}
Summary:        Libraries for the Unidata network Common Data Form

Group:          Applications/Engineering
License:        NetCDF
URL:            http://www.unidata.ucar.edu/software/netcdf/
Source0:        http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-%{version}.tar.gz
#Source0:        http://www.unidata.ucar.edu/downloads/netcdf/ftp/snapshot/netcdf-4-daily.tar.gz
Source1:        netcdf.module.in
Source2:        netcdf-mpi.module.in
#Use pkgconfig in nc-config to avoid multi-lib issues
Patch0:         netcdf-pkgconfig.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  chrpath
BuildRequires:  doxygen
BuildRequires:  hdf5%{?_cc_name_suffix}-devel%{?_isa} >= 1.8.4
BuildRequires:  gawk
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel
%ifnarch s390 s390x %{arm}
BuildRequires:  valgrind
%endif
#mpiexec segfaults if ssh is not present
#https://trac.mcs.anl.gov/projects/mpich2/ticket/1576
BuildRequires:  openssh-clients

# AltCCRPMs
Requires:       hdf5%{?_cc_name_suffix}%{?_isa} = 1.8.9
Provides:       %{shortname}%{?_cc_name_suffix} = %{version}-%{release}
Provides:       %{shortname}%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}

%global with_mpich2 0
%global with_openmpi 1
%if 0%{?rhel}
%ifarch ppc64
# No mpich2 on ppc64 in EL
%global with_mpich2 0
%endif
%endif
%ifarch s390 s390x
# No openmpi on s390(x)
%global with_openmpi 0
%endif

%if %{with_mpich2}
%global mpi_list mpich2
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif

%description
NetCDF (network Common Data Form) is an interface for array-oriented 
data access and a freely-distributed collection of software libraries 
for C, Fortran, C++, and perl that provides an implementation of the 
interface.  The NetCDF library also defines a machine-independent 
format for representing scientific data.  Together, the interface, 
library, and format support the creation, access, and sharing of 
scientific data. The NetCDF software was developed at the Unidata 
Program Center in Boulder, Colorado.

NetCDF data is: 

   o Self-Describing: A NetCDF file includes information about the
     data it contains.

   o Network-transparent:  A NetCDF file is represented in a form that
     can be accessed by computers with different ways of storing
     integers, characters, and floating-point numbers.

   o Direct-access:  A small subset of a large dataset may be accessed
     efficiently, without first reading through all the preceding
     data.

   o Appendable:  Data can be appended to a NetCDF dataset along one
     dimension without copying the dataset or redefining its
     structure. The structure of a NetCDF dataset can be changed,
     though this sometimes causes the dataset to be copied.

   o Sharable:  One writer and multiple readers may simultaneously
     access the same NetCDF file.


%package devel
Summary:        Development files for netcdf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       hdf5%{?_cc_name_suffix}-devel%{?_isa}
Requires:       libcurl-devel
Provides:       %{shortname}%{?_cc_name_suffix}-devel = %{version}-%{release}
Provides:       %{shortname}%{?_cc_name_suffix}-devel%{?_isa} = %{version}-%{release}

%description devel
This package contains the netCDF C header files, shared devel libs, and 
man pages.


%package static
Summary:        Static libs for netcdf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{shortname}%{?_cc_name_suffix}-static = %{version}-%{release}
Provides:       %{shortname}%{?_cc_name_suffix}-static%{?_isa} = %{version}-%{release}

%description static
This package contains the netCDF C static libs.


%if %{with_mpich2}
%package mpich2
Summary: NetCDF mpich2 libraries
Group: Development/Libraries
Requires: mpich2%{?_cc_name_suffix}%{?_isa}
BuildRequires: mpich2%{?_cc_name_suffix}-devel%{?_isa}
BuildRequires: hdf5-mpich2%{?_cc_name_suffix}-devel%{?_isa} >= 1.8.4
Requires:       hdf5-mpich2%{?_cc_name_suffix}%{?_isa} = 1.8.9
Provides:       %{shortname}-mpich2%{?_cc_name_suffix} = %{version}-%{release}
Provides:       %{shortname}-mpich2%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}

%description mpich2
NetCDF parallel mpich2 libraries


%package mpich2-devel
Summary: NetCDF mpich2 development files
Group: Development/Libraries
Requires: %{name}-mpich2%{?_isa} = %{version}-%{release}
Requires: mpich2%{?_cc_name_suffix}%{?_isa}
Requires: pkgconfig
Requires: hdf5-mpich2%{?_cc_name_suffix}-devel%{?_isa}
Requires: libcurl-devel
Provides: %{shortname}-mpich2%{?_cc_name_suffix}-devel = %{version}-%{release}
Provides: %{shortname}-mpich2%{?_cc_name_suffix}-devel%{?_isa} = %{version}-%{release}

%description mpich2-devel
NetCDF parallel mpich2 development files


%package mpich2-static
Summary: NetCDF mpich2 static libraries
Group: Development/Libraries
Requires: %{name}-mpich2-devel%{?_isa} = %{version}-%{release}
Provides: %{shortname}-mpich2%{?_cc_name_suffix}-static = %{version}-%{release}
Provides: %{shortname}-mpich2%{?_cc_name_suffix}-static%{?_isa} = %{version}-%{release}

%description mpich2-static
NetCDF parallel mpich2 static libraries
%endif


%if %{with_openmpi}
%package openmpi
Summary: NetCDF openmpi libraries
Group: Development/Libraries
Requires: openmpi%{?_cc_name_suffix}%{?_isa}
BuildRequires: openmpi%{?_cc_name_suffix}-devel%{?_isa}
BuildRequires: hdf5-openmpi%{?_cc_name_suffix}-devel%{?_isa} >= 1.8.4
Requires:       hdf5-openmpi%{?_cc_name_suffix}%{?_isa} = 1.8.9
Provides:       %{shortname}-openmpi%{?_cc_name_suffix} = %{version}-%{release}
Provides:       %{shortname}-openmpi%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}

%description openmpi
NetCDF parallel openmpi libraries


%package openmpi-devel
Summary: NetCDF openmpi development files
Group: Development/Libraries
Requires: %{name}-openmpi%{_isa} = %{version}-%{release}
Requires: openmpi%{?_cc_name_suffix}-devel%{?_isa}
Requires: pkgconfig
Requires: hdf5-openmpi%{?_cc_name_suffix}-devel%{?_isa}
Requires: libcurl-devel
Provides: %{shortname}-openmpi%{?_cc_name_suffix}-devel = %{version}-%{release}
Provides: %{shortname}-openmpi%{?_cc_name_suffix}-devel%{?_isa} = %{version}-%{release}

%description openmpi-devel
NetCDF parallel openmpi development files


%package openmpi-static
Summary: NetCDF openmpi static libraries
Group: Development/Libraries
Requires: %{name}-openmpi-devel%{?_isa} = %{version}-%{release}
Provides: %{shortname}-openmpi%{?_cc_name_suffix}-static = %{version}-%{release}
Provides: %{shortname}-openmpi%{?_cc_name_suffix}-static%{?_isa} = %{version}-%{release}

%description openmpi-static
NetCDF parallel openmpi static libraries
%endif


%prep
%setup -q -n netcdf-%{version}
%patch0 -p1 -b .pkgconfig


%build
#Do out of tree builds
%global _configure ../configure
#Common configure options
%global configure_opts \\\
           --enable-shared \\\
           --enable-netcdf-4 \\\
           --enable-dap \\\
           --enable-extra-example-tests \\\
           --disable-dap-remote-tests \\\
%{nil}

# Serial build
mkdir build
pushd build
export CC=icc
export CFLAGS="-g -O3 -axSSE2,SSE4.1,SSE4.2"
module load hdf5/%{_cc_name}
ln -s ../configure .
%configure %{configure_opts}
make %{?_smp_mflags}
module purge
popd

# MPI builds
export CC=mpicc
for mpi in %{mpi_list}
do
  mkdir $mpi
  pushd $mpi
  module load hdf5/$mpi-%{_cc_name}
  ln -s ../configure .
  %configure %{configure_opts} \
    --libdir=%{_libdir}/$mpi/lib \
    --bindir=%{_libdir}/$mpi/bin \
    --sbindir=%{_libdir}/$mpi/sbin \
    --includedir=%{_includedir}/$mpi-%{_arch} \
    --datarootdir=%{_libdir}/$mpi/share \
    --mandir=%{_libdir}/$mpi/share/man \
    --enable-parallel-tests
  make %{?_smp_mflags}
  module purge
  popd
done


%install
module load hdf5/%{_cc_name}
make -C build install DESTDIR=${RPM_BUILD_ROOT}
/bin/rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
chrpath --delete ${RPM_BUILD_ROOT}/%{_bindir}/nc{copy,dump,gen,gen3}
/bin/rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
module purge
for mpi in %{mpi_list}
do
  module load hdf5/$mpi-%{_cc_name}
  make -C $mpi install DESTDIR=${RPM_BUILD_ROOT}
  rm $RPM_BUILD_ROOT/%{_libdir}/$mpi/lib/*.la
  chrpath --delete ${RPM_BUILD_ROOT}/%{_libdir}/$mpi/bin/nc{copy,dump,gen,gen3}
  module purge
done

# AltCCRPMS
# Make the environment-modules file
mkdir -p %{buildroot}/etc/modulefiles/%{shortname}/%{_cc_name}/%{version}
# Since we're doing our own substitution here, use our own definitions.
sed -e 's#@PREFIX@#'%{_prefix}'#' -e 's#@LIB@#%{_lib}#' -e 's#@ARCH@#%{_arch}#' -e 's#@CC@#%{_cc_name}#' %SOURCE1 > %{buildroot}/etc/modulefiles/%{shortname}/%{_cc_name}/%{version}/%{_arch}
for mpi in %{mpi_list}
do
mkdir -p %{buildroot}/etc/modulefiles/%{shortname}/${mpi}-%{_cc_name}/%{version}
sed -e 's#@PREFIX@#'%{_prefix}'#' -e 's#@LIB@#%{_lib}#' -e 's#@ARCH@#%{_arch}#' -e 's#@CC@#%{_cc_name}#' -e 's#@MPI@#'$mpi'#' %SOURCE2 > %{buildroot}/etc/modulefiles/%{shortname}/${mpi}-%{_cc_name}/%{version}/%{_arch}
done


%check
%ifnarch s390
module load hdf5/%{_cc_name}
make -C build check
module purge
for mpi in %{mpi_list}
do
  module load hdf5/$mpi-%{_cc_name}
  make -C $mpi check
  module purge
done
%endif


%clean
rm -rf ${RPM_BUILD_ROOT}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYRIGHT README
/etc/modulefiles/%{shortname}/%{_cc_name}/
%{_bindir}/nccopy
%{_bindir}/ncdump
%{_bindir}/ncgen
%{_bindir}/ncgen3
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%doc examples
%{_bindir}/nc-config
%{_includedir}/netcdf.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/netcdf.pc
%{_mandir}/man3/*

%files static
%{_libdir}/*.a

%if %{with_mpich2}
%files mpich2
%doc COPYRIGHT README
/etc/modulefiles/%{shortname}/mpich2-%{_cc_name}/
%{_libdir}/mpich2/bin/nccopy
%{_libdir}/mpich2/bin/ncdump
%{_libdir}/mpich2/bin/ncgen
%{_libdir}/mpich2/bin/ncgen3
%{_libdir}/mpich2/lib/*.so.*
%doc %{_libdir}/mpich2/share/man/man1/*.1*

%files mpich2-devel
%{_libdir}/mpich2/bin/nc-config
%{_includedir}/mpich2-%{_arch}
%{_libdir}/mpich2/lib/*.so
%{_libdir}/mpich2/lib/pkgconfig/netcdf.pc
%doc %{_libdir}/mpich2/share/man/man3/*.3*

%files mpich2-static
%{_libdir}/mpich2/lib/*.a
%endif

%if %{with_openmpi}
%files openmpi
%doc COPYRIGHT README
/etc/modulefiles/%{shortname}/openmpi-%{_cc_name}/
%{_libdir}/openmpi/bin/nccopy
%{_libdir}/openmpi/bin/ncdump
%{_libdir}/openmpi/bin/ncgen
%{_libdir}/openmpi/bin/ncgen3
%{_libdir}/openmpi/lib/*.so.*
%doc %{_libdir}/openmpi/share/man/man1/*.1*

%files openmpi-devel
%{_libdir}/openmpi/bin/nc-config
%{_includedir}/openmpi-%{_arch}
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/lib/pkgconfig/netcdf.pc
%doc %{_libdir}/openmpi/share/man/man3/*.3*

%files openmpi-static
%{_libdir}/openmpi/lib/*.a
%endif


%changelog
* Fri Aug 3 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1.1-1
- Update to 4.2.1.1

* Sun Jul 22 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-1
- Update to 4.2.1 final

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-0.1.rc1
- Update to 4.2.1 rc1
- Rebase pkgconfig patch
- Drop fflags patch, upstream now calls nf-config

* Wed Jun 13 2012 Dan Horák <dan[at]danny.cz> - 4.2-5
- temporarily disable checks on s390 (memory corruption and stuck build)

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-4
- Rebuild with hdf5 1.8.9

* Wed Mar 21 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-3
- Update to real 4.2 final

* Tue Mar 20 2012 Dan Horák <dan[at]danny.cz> - 4.2-2
- use %%{mpi_list} also in %%check

* Fri Mar 16 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-1
- Update to 4.2 final

* Wed Mar 7 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.4.rc2
- Ship examples with -devel

* Wed Mar 7 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.3.rc2
- Enable MPI builds

* Tue Mar 6 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.2.rc2
- Update to 4.2-rc2
- Fortran and C++ APIs are now in separate packages

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.3-3
- Rebuild for hdf5 1.8.8, add explicit requires

* Thu Aug 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 4.1.3-2
- Add ARM to valgrind excludes

* Tue Jun 21 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.3-1
- Update to 4.1.3
- Update pkgconfig and fflags patches
- Drop libm patch fixed upstream

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.2-2
- Rebuild for hdf5 1.8.7

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.2-1
- Update to 4.1.2 (soname bump)
- Add patch to add -lm to libnetcdf4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 19 2010 Dan Horák <dan[at]danny.cz> - 4.1.1-4
- no valgrind on s390(x)

* Mon Apr 19 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-3
- Explicitly link libnetcdf.so against -lhdf5_hl -lhdf5

* Fri Apr 9 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-2
- Add patch to cleanup nc-config --fflags

* Thu Apr 8 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-1
- Update to 4.1.1

* Fri Feb 5 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-1
- Update to 4.1.0 final

* Mon Feb 1 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.8.2010020100
- Update snapshot, pkgconfig patch
- Re-enable make check

* Sat Dec 5 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.7.2009120100
- Leave include files in /usr/include

* Tue Dec 1 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.6.2009120100
- Update snapshot, removes SZIP defines from header

* Fri Nov 13 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.5.2009111309
- Update snapshot
- Docs are installed now

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.5.2009111008
- Explicitly link libnetcdf to the hdf libraries, don't link with -lcurl

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.4.2009111008
- Add Requires: libcurl-devel to devel package

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.3.2009111008
- Drop hdf4 support - too problematic with linking all required libraries

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.2.2009111008
- Add patch to use proper hdf4 libraries
- Add Requires: hdf-devel, hdf5-devel to devel package
- Move nc-config to devel package

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.1.2009111008
- Update to 4.1.0 beta 2 snapshot
- Enable: netcdf-4, dap, hdf4, ncgen4, a lot more tests

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Orion Poplawski <orion@cora.nwra.com> - 4.0.1-1
- Update to 4.0.1
- Add pkgconfig file

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Orion Poplawski <orion@cora.nwra.com> - 4.0.0-1
- Update to 4.0 final
- Drop netcdf-3 symlink (bug #447158)
- Update cstring patch, partially upstreamed

* Thu May 29 2008 Balint Cristian <rezso@rdsor.ro> - 4.0.0-0.6.beta2
- fix symlink to netcdf-3

* Sun May 18 2008 Patrice Dumas <pertusus@free.fr> - 4.0.0-0.5.beta2
- use %%{_fmoddir}
- don't use %%makeinstall

* Thu May 15 2008 Balint Cristian <rezso@rdsor.ro> - 4.0.0-0.4.beta2
- re-enable ppc64 since hdf5 is now present for ppc64

* Thu May  8 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.3.beta2
- make package compliant with bz # 373861

* Thu May  8 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.2.beta2
- ExcludeArch: ppc64 since it doesn't (for now) have hdf5

* Wed May  7 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.1.beta2
- try out upstream 4.0.0-beta2

* Wed Apr  2 2008 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-7
- Change patch to include <cstring>
- Remove %%{?_smp_mflags} - not parallel build safe (fortran modules)

* Wed Feb 20 2008 Ed Hill <ed@eh3.com> - 3.6.2-6
- add patch that (hopefully?) allows the GCC 4.3 build to proceed

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6.2-5
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 3.6.2-4
- add BR: gawk

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 3.6.2-3
- rebuild for BuildID

* Mon May 21 2007 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-2
- Run checks

* Sat Mar 17 2007 Ed Hill <ed@eh3.com> - 3.6.2-1
- 3.6.2 has a new build system supporting shared libs

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.6.1-4
- switch to compat-gcc-34-g77 instead of compat-gcc-32-g77

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.6.1-3
- rebuild for imminent FC-6 release

* Thu May 11 2006 Ed Hill <ed@eh3.com> - 3.6.1-2
- add missing BuildRequires for the g77 interface

* Fri Apr 21 2006 Ed Hill <ed@eh3.com> - 3.6.1-1
- update to upstream 3.6.1

* Thu Feb 16 2006 Ed Hill <ed@eh3.com> - 3.6.0-10.p1
- rebuild for new GCC

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> - 3.6.0-9.p1
- rebuild for gcc4.1

* Sun Oct 16 2005 Ed Hill <ed@eh3.com> - 3.6.0-8.p1
- building the library twice (once each for g77 and gfortran) 
  fixes an annoying problem for people who need both compilers

* Fri Sep 29 2005 Ed Hill <ed@eh3.com> - 3.6.0-7.p1
- add FFLAGS="-fPIC"

* Fri Jun 13 2005 Ed Hill <ed@eh3.com> - 3.6.0-6.p1
- rebuild

* Fri Jun  3 2005 Ed Hill <ed@eh3.com> - 3.6.0-5.p1
- bump for the build system

* Mon May  9 2005 Ed Hill <ed@eh3.com> - 3.6.0-4.p1
- remove hard-coded dist/fedora macros

* Wed May  5 2005 Ed Hill <ed@eh3.com> - 3.6.0-3.p1
- make netcdf-devel require netcdf (bug #156748)
- cleanup environment and paths

* Tue Apr  5 2005 Ed Hill <ed@eh3.com> - 0:3.6.0-2.p1
- update for gcc-gfortran
- fix file permissions

* Sat Mar  5 2005 Ed Hill <ed@eh3.com> - 0:3.6.0-1.p1
- update for 3.6.0-p1 large-files-bug fix and remove the Epoch

* Sun Dec 12 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0-0.2.beta6
- fix naming scheme for pre-releases (per Michael Schwendt)

* Sat Dec 11 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.2
- For Fortran, use only g77 (ignore gfortran, even if its installed)

* Tue Dec  7 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.1
- remove "BuildRequires: gcc4-gfortran"

* Sat Dec  4 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.0
- upgrade to 3.6.0beta6
- create separate devel package that does *not* depend upon 
  the non-devel package and put the headers/libs in "netcdf-3" 
  subdirs for easy co-existance with upcoming netcdf-4

* Thu Dec  2 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.12
- remove unneeded %%configure flags

* Wed Dec  1 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.11
- headers in /usr/include/netcdf, libs in /usr/lib/netcdf

* Mon Oct  4 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.10
- Put headers in their own directory but leave the libraries in the 
  %%{_libdir} -- there are only two libs and the majority of other
  "*-devel" packages follow this pattern

* Sun Oct  3 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:3.5.1-0.fdr.9
- add patch to install lib and headers into own tree

* Sun Aug  1 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.8
- added -fPIC so x86_64 build works with nco package

* Fri Jul 30 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.7
- fix typo in the x86_64 build and now works on x86_64

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.6
- fix license

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.5
- fix (hopefully?) x86_64 /usr/lib64 handling

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.4
- replace paths with macros

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.3
- fix spelling

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.2
- removed "--prefix=/usr" from %%configure

* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.1
- Remove unnecessary parts and cleanup for submission

* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.0
- Initial RPM release.
