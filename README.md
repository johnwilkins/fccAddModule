# fccAddModule

The `fccAddModule.py` program is a helper utility for adding a module in Red Hat's Flexible Customer Content format (FCC). The primary purpose for the program is to enable writers to specify a module name in plain text titlecase and an assembly file name. The program will:

* Generate the module file
* Add a header comment indicating which assembly includes the module
* Add an anchor tag to the module
* Add a heading with the specified module name
* Generate the module file name
* Save the module file; and,
* Add/append an include statement to the assembly file, if specified.

To use the program, copy `fccAddModule.conf` and `fccAddModule.py` to your project in the same directory as `master.adoc`. Modify the default values in the `fccAddModule.conf` file as needed. The program __must__ be run in the same directory as `master.adoc` and the assembly files.

For ease of use, modify the `defaultComponentType` setting of the `fccAddModule.conf` file to the name of the product or component. For example, "ceph" as a product or "rbd", "rgw", "rados", or "cephfs" as components of Ceph Storage; "osp" as a product, or "heat", "nova", "glance", etc. as components of OpenStack Platform. You can override the default value on the command line with the `-c` or `--component` argument.

Modify the `moduleDestinationPath` setting of the `fccAddModule.conf` file to specify the destination path where `fccAddModule.py` will save module file. Make sure to add an ending slash (_e.g._, `directory/` not `directory`).

## Usage:

    $ python fccAddModule.py --name "My Module Name" --assembly assembly_assembly-file-name_en-us.adoc

The foregoing usage generates a file called `proc_comp_my-module-name_en-us.adoc` where `proc` is the default module type of procedure, `comp` is the component name, `my-module-name` is the name of the module and `en_us` specifies the locale.

The generated file contents include:

    // This is included in the following assemblies:
    //
    //
    // assembly_assembly-file-name_en-us.adoc
    [id='my-module-name_{context}']

    = My Module Name

If the module is an assembly, typically the assembly will be incorporated into the `master.adoc` file or another assembly file, which is in the project directory rather than the default `modules` destination directory. Specify the `-d` option and the project folder as the destination for the module when adding an assembly. For example:

    $ python fccAddModule.py -n "Assembly" -a master.adoc -d ./ -t assembly

The program appends an include statement to the assembly file, if specified:

    include::{includedir}/<moduleDestinationPath>/proc_comp_my-module-name_en-us.adoc[leveloffset=+1]

The program assumes the use of an `{includedir}` variable in the assembly files. The `moduleDestinationPath` is the location where the program stores modules.

## Options:

* -n `<moduleName>` OR --name `<moduleName>` REQUIRED
* -t `(proc|con|ref|assembly)` OR --type `(proc|con|ref|assembly)` OPTIONAL
* -a `<assemblyFile>` OR --assembly `<assemblyFile>` OPTIONAL
* -c `<componentName>` OR --component `<componentName>` OPTIONAL
* -s `<sourceFileName>` OR --source `<sourceFileName>` OPTIONAL
* -d `<moduleDestinationPath>` OR --destination `<moduleDestinationPath>` OPTIONAL

The `-t` or `--type` option specifies the type of module. The options are `proc` for procedure, `con` for concept, `ref` for reference and `assembly` for an assembly. By default, the program uses `proc`. You may override the default with the `-t` or `--type` option on the command line, or set a new default in the `fccAddModule.conf` configuration file. _Procedure_ is the most common module type so `proc` is the default value.

The component name should be the product name or a sub-component of the product.

The `-s` or `--source` option refers to an existing text file. Specifying an existing text file will import the text of the file after the heading. __The program truncates the first line to trim anchor tags. If your file does not have an anchor tag, you should add a carriage return at the first line of the source file.

The `-d` or `--destination` option is the destination path for the module. In Red Hat's Flexible Customer Content (FCC) format, module files often live in a different directory from the `master.adoc` file and assembly files. You may override the default with the `-d` or `--destination` option on the command line, or set a new default in the `fccAddModule.conf` configuration file. Make sure to add an ending slash (_e.g._, `directory/` not `directory`).
