%define		_disable_ld_no_undefined	1

Name:		navit
Summary:	Car navigation system with routing engine
Version:	0.1.0
Release:	%{mkrel 3}
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	http://www.navit-project.org/maps/osm_bbox_11.3,47.9,11.7,48.2.osm.bz2
# Fix the building of translations - AdamW 2009/01
Patch0:		navit-0.1.0-po.patch
# Fix a string literal error - AdamW 2009/01
Patch1:		navit-0.1.0-literal.patch
# Fix the detection of Python on x86-64 - AdamW 2009/01
Patch2:		navit-0.1.0-pythonlib.patch
# From upstream SVN: Fix sample map generation with parallel make
# - AdamW 2009/01
Patch3:		navit-0.1.0-parallel.patch
# From upstream SVN: fix run on x86-64 - AdamW 2009/01
Patch4:		navit-0.1.0-libdir.patch
# Don't try to download the sample map on the fly - AdamW 2009/01
Patch5:		navit-0.1.0-static_sample.patch
Group:		Sciences/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
License:	GPLv2
BuildRequires:	zlib-devel
BuildRequires:	gtk+2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	SDL_image-devel
BuildRequires:	postgresql-devel
BuildRequires:	imlib2-devel
BuildRequires:	CEGUI-devel
BuildRequires:	libxmu-devel
BuildRequires:	mesaglut-devel
BuildRequires:	quesoglc-devel
# Clutter GUI doesn't build due to a header missing from the tarball
# and upstream SVN lists it as 'nothing functional for now' - check in
# future releases - AdamW 2009/01
#BuildRequires:	clutter-devel >= 0.8
BuildRequires:	python-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gd-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	gpsd-devel
BuildRequires:	qt4-devel
Requires:	fonts-ttf-dejavu
Suggests:	gpsd
URL:		http://www.navit-project.org/

%description
Navit is a car navigation system with routing engine. Its modular
design is capable of using vector maps of various formats for routing
and rendering of the displayed map. It's even possible to use multiple
maps at a time.

The GTK+ or SDL user interfaces are designed to work well with touch
screen displays. Points of Interest of various formats are displayed
on the map.

The current vehicle position is either read from gpsd or directly from
NMEA GPS sensors.

The routing engine not only calculates an optimal route to your
destination, but also generates directions and even speaks to you.

%package gui-cegui
Summary:	CEGUI GUI for Navit navigation system
Group:		Sciences/Other
Requires:	%{name} = %{version}-%{release}

%description gui-cegui
Navit is a car navigation system with routing engine. This package
contains the CEGUI GUI for Navit. You need to enable this GUI in
/etc/navit/navit.xml or ~/.navit/navit.xml to use it.

%package graphics-qt
Summary:	Qt graphics renderer for Navit navigation system
Group:		Sciences/Other
Requires:	%{name} = %{version}-%{release}

%description graphics-qt
Navit is a car navigation system with routing engine. This package
contains the Qt-QPainter graphics renderer for Navit. You need to
enable this renderer in /etc/navit/navit.xml or ~/.navit/navit.xml
to use it.

%package graphics-sdl
Summary:	SDL graphics renderer for Navit navigation system
Group:		Sciences/Other
Requires:	%{name} = %{version}-%{release}

%description graphics-sdl
Navit is a car navigation system with routing engine. This package
contains the SDL graphics renderer for Navit. You need to enable
this renderer in /etc/navit/navit.xml or ~/.navit/navit.xml to use it.

%prep
%setup -q
%patch0 -p1 -b .fixpo
%patch1 -p1 -b .literal
%patch2 -p1 -b .pythonlib
%patch3 -p2 -b .parallel
%patch4 -p2 -b .libdir
%patch5 -p1 -b .static_sample
install -m 0644 %{SOURCE1} navit/maps

%build
autoreconf -i
# See note on clutter above. - AdamW 2009/01
%configure2_5x --disable-gui-clutter
make 

%install
rm -rf %{buildroot}
%makeinstall_std

# Don't need the README here
rm -f %{buildroot}%{_datadir}/%{name}/README
# Use system Deja Vu
rm -f %{buildroot}%{_datadir}/%{name}/datafiles/fonts/DejaVuSans.ttf
ln -s %{_datadir}/fonts/TTF/dejavu/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}/datafiles/fonts/DejaVuSans.ttf

# Put the config file in /etc: upstream likes it in /usr to be
# relocatable, but that doesn't concern us. The code does check
# in /etc, so we don't need a patch - AdamW 2009/01
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/%{name}.xml %{buildroot}%{_sysconfdir}/%{name}/%{name}.xml

# Create a README.urpmi - AdamW 2009/01
cat > README.urpmi << EOF 
Navit comes with a sample map of Munich, but if you live (or drive!)
anywhere else, you'll need to add another map set. These are not
available as packages because they're rather large and the data changes
on a daily basis, so the packages would have to be refreshed very
often. For instructions on downloading or generating, and installing,
different types of map sets, see these Navit Wiki pages:

http://wiki.navit-project.org/index.php/OpenStreetMaps

http://wiki.navit-project.org/index.php/European_maps

http://wiki.navit-project.org/index.php/Garmin_maps

You should either add the appropriate configuration elements to
/etc/navit/navit.xml, or copy /etc/navit/navit.xml to
~/.navit/navit.xml and edit it there. You may have to remove or comment
out the section for the sample map set, also. Also note that the
default configuration assumes you have a GPS device active, and gpsd
running.
EOF

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr (-,root,root)
%doc AUTHORS README README.urpmi
%{_bindir}/%{name}
%{_bindir}/osm2navit
%{_libdir}/%{name}
%exclude %{_libdir}/%{name}/graphics/libgraphics_qt*
%exclude %{_libdir}/%{name}/graphics/libgraphics_sdl*
%exclude %{_libdir}/%{name}/gui/libgui_cegui*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.xml

%files gui-cegui
%defattr (-,root,root)
%{_libdir}/%{name}/gui/libgui_cegui*

%files graphics-qt
%defattr (-,root,root)
%{_libdir}/%{name}/graphics/libgraphics_qt*

%files graphics-sdl
%defattr (-,root,root)
%{_libdir}/%{name}/graphics/libgraphics_sdl*

