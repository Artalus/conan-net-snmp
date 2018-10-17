from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class NetsnmpConan(ConanFile):
    name = "net-snmp"
    version = "5.7.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Netsnmp here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
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

    # def package(self):
        # self.copy("*.h", dst="include", src="include")
        # self.copy("*.so", dst="lib", src="lib", keep_path=False)
        # self.copy("*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["netsnmpagent", "netsnmphelpers", "netsnmpmibs", "netsnmp"]
