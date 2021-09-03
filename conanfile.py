from conans import ConanFile, CMake, tools, Meson
import os


class GstpluginsgoodConan(ConanFile):
    name = "gst_plugins_good"
    version = "1.19.1"
    description = ""
    url = "https://github.com/GStreamer/gst-plugins-good"
    homepage = "https://github.com/GStreamer/gst-plugins-good"
    license = "GPLv2+"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {
        "shared": True
    }
    generators = "cmake", "pkg_config"
    requires = (
        "gst_plugins_base/1.19.1",
    )
    source_subfolder = "gst-plugins-good"
    build_subfolder = "build"
    remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-good.git'}

    def source(self):
        tools.mkdir(self.source_subfolder)
        with tools.chdir(self.source_subfolder):
            self.run('git init')
            for key, val in self.remotes.items():
                self.run("git remote add %s %s" % (key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s' % (self.version))
            self.run('git submodule update --init --recursive')

    def build(self):
        # tools.mkdir("install")
        # install_path = os.getcwd() + "/install"
        # with tools.chdir("../" + self.source_subfolder):
        #     self.run("meson setup ../build --prefix " + install_path)
        # self.run("ninja")
        pkg_config_paths = [
            os.path.join(
                self.deps_cpp_info['gst_plugins_base'].rootpath, 'lib', 'pkgconfig')
        ]
        pkg_config_args = "--define-variable package_root_path_gst_plugins_base=" + \
            self.deps_cpp_info['gst_plugins_base'].rootpath
        vars = {
            'PKG_CONFIG': "pkg-config " + pkg_config_args}
        with tools.environment_append(vars):
            meson = Meson(self)
            meson.configure(build_folder=self.build_subfolder,
                            source_folder=self.source_subfolder,
                            pkg_config_paths=pkg_config_paths)
            meson.build()
        # self.run("ninja install --verbose")

    def package(self):
        self.copy("lib/*", "", "install")
        self.copy("include/*", "", "install")
        self.copy("bin/*", "", "install")
        self.copy("share/*", "", "install")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(
            self)
        self.cpp_info.includedirs = ['include/gstreamer-1.0']
