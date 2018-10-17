from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class NetsnmpConan(ConanFile):
    name = "net-snmp"
    version = "5.7.3"
    license = "BSD-like. http://www.net-snmp.org/about/license.html"
    url = "https://github.com/Artalus/conan-net-snmp"
    description = "SNMP is a widely used protocol for monitoring the health and welfare of network equipment"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = ("shared=False", "fPIC=False")

    requires = "OpenSSL/[>1.0.0,<1.1.0]@conan/stable"

    snmp = '%s-%s'%(name, version)

    def source(self):
        tools.get('http://downloads.sourceforge.net/project/net-snmp/net-snmp/%s/%s.zip' % (self.version, self.snmp), keep_permissions=True)

    def build(self):
        tools.mkdir('build')
        with tools.chdir('build'):
            autotools = AutoToolsBuildEnvironment(self)
            conf = '../'+self.snmp
            os.chmod('%s/configure'%conf, 0o777)
            autotools.configure(configure_dir=conf, args=[
                '--bindir=/tmp/whatevereresrserasd', # TODO: properly get rid of bin/ after installation
                '--with-defaults',
                '--disable-agent',
                '--disable-applications',
                '--disable-scripts',
                '--disable-mibs',
                '--disable-manuals',
                ])
            autotools.make()
            autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["netsnmpagent", "netsnmphelpers", "netsnmpmibs", "netsnmp"]
