# addModule

The `addModule.py` program is a helper utility for adding a module in Red Hat's Flexible Customer Content format (FCC). The primary purpose for the program is to enable writers to specify a module name in plain text title case and an assembly file name. The program will:

* Generate the module file
* Add a header comment indicating which assembly includes the module
* Add an anchor tag to the module
* Add a heading with the specified module name
* Generate the module file name in the specified format
* Save the module file; and,
* Add/append an include statement to the assembly file, if specified.

If you specify `-r` or `--rename` with an old module name, the program will rename the module, including the assembly file's include statement if you specify `-a` or `--assembly`.

To use the program, copy `addModule.conf` and `addModule.py` to your project in the same directory as `main.adoc`. Modify the default values in the `addModule.conf` file as needed. The program __must__ be run in the same directory as `main.adoc` and the assembly files.

For ease of use, modify the `defaultComponentType` setting of the `addModule.conf` file to the name of the product or component. For example, "ceph" as a product or "rbd", "rgw", "rados", or "cephfs" as components of Ceph Storage; "osp" as a product, or "heat", "nova", "glance", etc. as components of OpenStack Platform. You can override the default value on the command line with the `-c` or `--component` argument.

Modify the `moduleDestinationPath` setting of the `addModule.conf` file to specify the destination path where `addModule.py` will save module file. Make sure to add an ending slash (_e.g._, `directory/` not `directory`).

## Usage

    $ python addModule.py --name "My Module Name" --assembly assembly_assembly-file-name_en-us.adoc

The foregoing usage with the `fcc` format generates a file called `proc_comp_my-module-name_en-us.adoc` where `proc` is the default module type of procedure, `comp` is the component name, `my-module-name` is the name of the module and `en_us` specifies the locale.

The foregoing usage with the `ocp` format generates a file called `comp_my-module-name.adoc` where `comp` is the component name, and `my-module-name` is the name of the module. Use the `-f` or `--format` option, or change the default in the `addModule.conf` configuration file.


The generated file contents include:

    // This is included in the following assemblies:
    //
    //
    // assembly_assembly-file-name_en-us.adoc
    [id='my-module-name_{context}']

    = My Module Name

If the module is an assembly, typically the assembly will be incorporated into the `main.adoc` file or another assembly file, which is in the project directory rather than the default `modules` destination directory. Specify the `-d` option and the project folder as the destination for the module when adding an assembly. For example:

    $ python addModule.py -n "Assembly" -a main.adoc -d ./ -t assembly

The program appends an include statement to the assembly file, if specified:

    include::{includedir}/<moduleDestinationPath>/proc_comp_my-module-name_en-us.adoc[leveloffset=+1]

The program assumes the use of an `{includedir}` variable in the assembly files. The `moduleDestinationPath` is the location where the program stores modules.

## Options:

* -n `<moduleName>` OR --name `<moduleName>` REQUIRED
* -r `<oldModuleName>` OR --rename `<oldModuleName>` OPTIONAL
* -f <fcc|ocp> OR --format <fcc|ocp> OPTIONAL. DEFAULT = fcc
* -t (proc|con|ref|assembly) OR --type (proc|con|ref|assembly) OPTIONAL
* -a <assemblyFile> OR --assembly <assemblyFile> OPTIONAL
* -c <componentName> OR --component <componentName> OPTIONAL
* -d <moduleDestinationPath> OR --destination <moduleDestinationPath> OPTIONAL

The `-t` or `--type` option specifies the type of module. The options are `proc` for procedure, `con` for concept, `ref` for reference and `assembly` for an assembly. By default, the program uses `proc`. You may override the default with the `-t` or `--type` option on the command line, or set a new default in the `addModule.conf` configuration file. _Procedure_ is the most common module type so `proc` is the current default value.

The component name should be the product name or a sub-component of the product.

The `-d` or `--destination` option is the destination path for the module. In Red Hat's Flexible Customer Content (FCC) format, module files often live in a different directory from the `main.adoc` file and assembly files. You may override the default with the `-d` or `--destination` option on the command line, or set a new default in the `addModule.conf` configuration file. Make sure to add an ending slash (_e.g._, `directory/` not `directory`).

The `-f` or `--format` option is the file name format. The default format is the `fcc` format, which includes a component type and a locale. The alternate format is `ocp`, which omits a component type and the locale.

# Script development

* Use Python 3.
* Run `pip install configparser`.
* Fork the fccAddModule repo and git clone to your home directory, for example `~/fccAddmodule`

To run the script from `~/fccAddmodule` for `~/openshift-docs` repo, do the following:

1. Copy `addModule.conf` to the root of your `~/openshift-docs` repo folder
2. cd to `openshift-docs`, and run:
    
    $ python ../fccAddModule/addModule.py --name "My Module Name" --assembly assembly_assembly-file-name_en-us.adoc

# RPM packaging

Install the bare minimum of required packages (tested on Fedora 33)
    
    $ sudo dnf install rpm-build rpm-devel rpmdevtools
    
    $ pip install pyinstaller --user

First-time setup of build dirs
    
    $ rpmdev-setuptree

Copy the source files
    
    $ sudo cp -r ~/fccAddModule/ $HOME/rpmbuild/SOURCES/

Invoke the build
    
    $ rpmbuild -ba ~/fccAddModule/fccAddModule.spec
    
    





