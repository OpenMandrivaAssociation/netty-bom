Name:		netty-bom
Version:	4.1.139.Final
Release:	1
Summary:	Bill of Materials for Netty components
Group:		Development/Java
License:	Apache-2.0
URL:		https://netty.io/
# Tag netty-4.1.139.Final. The bill of materials is bom/pom.xml.
# The lookaside archive is that module plus the tag's license files.
Source0:	netty-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	python
# The file attribute generator only emits the pom-typed coordinate.
# Gradle's catalog asks for the untyped name.
Provides:	mvn(io.netty:netty-bom) = %{version}

%description
Bill of Materials for Netty %{version}. Gradle 9.9.1 imports this
coordinate. Each managed io.netty artifact uses the BOM version.
The native 2.0.84.Final transport version is recorded in the POM.

%prep
%autosetup -n netty-%{version}
find . -depth \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -exec /bin/rm -rf {} +

%install
sysjar install --buildroot %{buildroot} --artifact bom/pom.xml --file-name netty-bom --filelist .mfiles

%check
python - <<'PY'
import xml.etree.ElementTree as ET
NS = {"m": "http://maven.apache.org/POM/4.0.0"}
root = ET.parse("%{buildroot}/usr/share/maven-poms/netty-bom.pom").getroot()
ver = root.find("m:version", NS).text
art = root.find("m:artifactId", NS).text
common = None
for dep in root.findall(".//m:dependency", NS):
    name = dep.find("m:artifactId", NS)
    if name is not None and name.text == "netty-common":
        common = dep.find("m:version", NS).text
if ver != "%{version}" or art != "netty-bom" or common != "${project.version}":
    raise SystemExit("bad bom %s %s %s" % (ver, art, common))
print("netty_bom_ok", ver, "netty-common", common)
PY

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt
