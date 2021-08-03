%define		crates_ver 0.9.0

Summary:	A fast, cross-platform, OpenGL terminal emulator
Name:		alacritty
Version:	0.9.0
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/alacritty/alacritty/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	393d34a29db21390964181b73cf9cba1
# cd alacritty-%{version}
# cargo vendor
# cd ..
# tar cJf alacritty-crates-%{version}.tar.xz alacritty-%{version}/{vendor,Cargo.lock}
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	7f43543fb0a78f495bb2f6b71ae3a6d7
URL:		https://github.com/alacritty/alacritty
BuildRequires:	cargo
BuildRequires:	fontconfig-devel >= 2.11.1
BuildRequires:	freetype-devel >= 2.8.0
BuildRequires:	libxcb-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires:	fontconfig-libs >= 2.11.1
Requires:	freetype >= 2.8.0
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alacritty is a modern terminal emulator that comes with sensible
defaults, but allows for extensive configuration. By integrating with
other applications, rather than reimplementing their functionality, it
manages to provide a flexible set of features with high performance.

%package -n bash-completion-alacritty
Summary:	Bash completion for alacritty command line
Summary(pl.UTF-8):	Bashowe dopełnianie linii poleceń programu alacritty
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-alacritty
Bash completion for alacritty command line.

%description -n bash-completion-alacritty -l pl.UTF-8
Bashowe dopełnianie linii poleceń programu alacritty.

%package -n fish-completion-alacritty
Summary:	fish-completion for alacritty
Summary(pl.UTF-8):	Uzupełnianie nazw w fish dla alacritty
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-alacritty
fish-completion for alacritty.

%description -n fish-completion-alacritty -l pl.UTF-8
Pakiet ten dostarcza uzupełnianie nazw w fish dla alacritty.

%package -n zsh-completion-alacritty
Summary:	ZSH completion for alacritty command line
Summary(pl.UTF-8):	Dopełnianie linii poleceń programu alacritty dla powłoki ZSH
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-alacritty
ZSH completion for alacritty command line.

%description -n zsh-completion-alacritty -l pl.UTF-8
Dopełnianie linii poleceń programu alacritty dla powłoki ZSH.

%prep
%setup -q -a1

%{__mv} %{name}-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_desktopdir},%{_datadir}/metainfo,%{_pixmapsdir},%{bash_compdir},%{fish_compdir},%{zsh_compdir}}

cp -p target/release/alacritty $RPM_BUILD_ROOT%{_bindir}
cp -p extra/alacritty.man $RPM_BUILD_ROOT%{_mandir}/man1/alacritty.1
cp -p extra/completions/_alacritty $RPM_BUILD_ROOT%{zsh_compdir}/_alacritty
cp -p extra/completions/alacritty.bash $RPM_BUILD_ROOT%{bash_compdir}/alacritty
cp -p extra/completions/alacritty.fish $RPM_BUILD_ROOT%{fish_compdir}/alacritty.fish
cp -p extra/linux/Alacritty.desktop $RPM_BUILD_ROOT%{_desktopdir}/Alacritty.desktop
cp -p extra/linux/io.alacritty.Alacritty.appdata.xml $RPM_BUILD_ROOT%{_datadir}/metainfo
cp -p extra/logo/alacritty-term.svg $RPM_BUILD_ROOT%{_pixmapsdir}/Alacritty.svg

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/alacritty
%{_mandir}/man1/alacritty.1*
%{_desktopdir}/Alacritty.desktop
%{_datadir}/metainfo/io.alacritty.Alacritty.appdata.xml
%{_pixmapsdir}/Alacritty.svg

%files -n bash-completion-alacritty
%defattr(644,root,root,755)
%{bash_compdir}/alacritty

%files -n fish-completion-alacritty
%defattr(644,root,root,755)
%{fish_compdir}/alacritty.fish

%files -n zsh-completion-alacritty
%defattr(644,root,root,755)
%{zsh_compdir}/_alacritty
