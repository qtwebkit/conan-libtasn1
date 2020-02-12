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

    def build_requirements(self):
        print(tools.os_info.detect_windows_subsystem())
        if tools.os_info.is_windows and "CONAN_BASH_PATH" not in os.environ:
            self.build_requires("msys2/20190524")

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
        with tools.vcvars(self.settings) if self.settings.compiler == "Visual Studio" else tools.no_op():
            with tools.chdir(self._source_subfolder):
                env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
                args = ["--disable-dependency-tracking", "--disable-doc"]
                if self.settings.os != "Windows" and self.options.fPIC:
                    args.append("--with-pic")
                if self.options.shared:
                    args.extend(["--disable-static", "--enable-shared"])
                else:
                    args.extend(["--disable-shared", "--enable-static"])
                if self.settings.compiler == "Visual Studio":
                    runtime = str(self.settings.compiler.runtime)
                    prefix = tools.unix_path(self.package_folder)
                    args.extend(['CC=$PWD/build-aux/compile cl -nologo',
                                 'CFLAGS=-%s' % runtime,
                                 'CXX=$PWD/build-aux/compile cl -nologo',
                                 'CXXFLAGS=-%s' % runtime,
                                 'CPPFLAGS=-D_WIN32_WINNT=0x0600 -I%s/include' % prefix,
                                 'LDFLAGS=-L%s/lib' % prefix,
                                 'LD=link',
                                 'NM=dumpbin -symbols',
                                 'STRIP=:',
                                 'AR=$PWD/build-aux/ar-lib lib',
                                 'RANLIB=:'])
                env_build.configure(args=args)
                env_build.make()
                env_build.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["tasn1"]
