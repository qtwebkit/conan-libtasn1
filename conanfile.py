from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class Libtasn1Conan(ConanFile):
    name = "libtasn1"
    version = "4.16.0"
    license = "LGPL-2.1-or-later"
    author = "Bincrafters <bincrafters@gmail.com>"
    url = "https://github.com/qtwebkit/conan-libtasn1"
    homepage = "https://www.gnu.org/software/libtasn1/"
    description = "Libtasn1 is the ASN.1 library used by GnuTLS, p11-kit and some other packages"
    topics = ("conan", "asn.1")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "sources"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(url="http://ftp.gnu.org/gnu/libtasn1/libtasn1-{}.tar.gz".format(self.version),
                  sha256="0e0fb0903839117cb6e3b56e68222771bebf22ad7fc2295a0ed7d576e8d4329d")
        os.rename("libtasn1-{}".format(self.version), self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            args = ["--disable-dependency-tracking", "--disable-doc"]
            if self.settings.os != "Windows" and self.options.fPIC:
                args.append("--with-pic")
            if self.options.shared:
                args.extend(["--disable-static", "--enable-shared"])
            else:
                args.extend(["--disable-shared", "--enable-static"])
            env_build.configure(args=args)
            env_build.make()
            env_build.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["tasn1"]
