Name:		navit
Summary:	Car navigation system with routing engine
Version:	0.2.0
Release:	2
Group:		Sciences/Other
License:	GPLv2+
URL:		http://www.navit-project.org/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	http://www.navit-project.org/maps/osm_bbox_11.3,47.9,11.7,48.2.osm.bz2
BuildRequires:	gd-devel
BuildRequires:	gettext-devel
BuildRequires:	nas-devel
BuildRequires:	postgresql-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	pkgconfig(libgpsd)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(quesoglc)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(xmu)
Requires:	fonts-ttf-dejavu
Suggests:	gpsd

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

%package gtk-gui
Summary:	GTK GUI for Navit navigation system
Group:		Sciences/Other
Requires:	%{name} = %{version}-%{release}

%description gtk-gui
Navit is a car navigation system with routing engine. This package
contains the GTK GUI for Navit. You need to enable this GUI in
/etc/navit/navit.xml or ~/.navit/navit.xml to use it.

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
install -m 0644 %{SOURCE1} navit/maps

%build
%configure2_5x --enable-graphics-gd --disable-graphics-qt-qpainter
%make 

%install
%makeinstall_std

# Don't need the README here
rm -f %{buildroot}%{_datadir}/%{name}/README

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

%files -f %{name}.lang
%doc AUTHORS README README.urpmi
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/dbus-1/services/org.navit_project.navit.service
%exclude %{_libdir}/%{name}/graphics/libgraphics_sdl*
%exclude %{_libdir}/%{name}/gui/libgui_gtk*
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.xml

%files gtk-gui
%{_libdir}/%{name}/gui/libgui_gtk*

%files graphics-sdl
%{_libdir}/%{name}/graphics/libgraphics_sdl*

