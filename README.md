# fccAddModule

The __fccAddModule.py__ program is a helper utility for adding a module in Red Hat's Flexible Customer Content format (FCC). The primary purpose for the program is to enable writers to specify a module name in plain text titlecase and an assembly file name. The program will:

* Generate the module file
* Add an anchor tag to the module
* Add a heading with the specified module name
* Generate the module file name
* Save the module file; and,
* Add/append an include statement to the assembly file, if specified.

To use the program, copy _fccAddModule.conf_ and _fccAddModule.py_ to your project in the same directory as _master.adoc_. Modify the default values in the _fccAddModule.conf_ file as needed. The program __must__ be run in the same directory as _master.adoc_ and the assembly files.

For ease of use, modify the _defaultComponentType_ setting of the _fccAddModule.conf_ file to the name of the product or component. For example, "ceph" as a product or "rbd", "rgw", "rados", or `cephfs` as components of Ceph Storage; "osp" as a product, or "heat", "nova", "glance", etc. as components of OpenStack Platform. You can override the default value on the command line with the _-c_ or _--component_ argument.

Modify the _moduleDestinationPath_ setting of the _fccAddModule.conf_ file to specify the destination path where _fccAddModule.py_ will save module file. Make sure to add an ending slash (_e.g._, _directory/_ not _directory_).

## Usage:

  $ python fccAddModule.py --name "My Module Name" --assembly assembly_assembly-file-name_en-us.adoc

The foregoing usage generates a file called _proc_comp_my-module-name_en-us.adoc_ where _proc_ is the default module type of procedure, _comp_ is the component name, _my-module-name_ is the name of the module and _en_us_ specifies the locale.

The generated file contents include:

  [id='my-module-name-{context}']

  = My Module Name


The program appends an include statement to the assembly file, if specified:

  include::{includedir}/<moduleDestinationPath>/proc_comp_my-module-name_en-us.adoc[leveloffset=+1]

The program assumes the use of an _{includedir}_ variable. The _moduleDestinationPath_ is the location where the program stores modules.


## Options:

-n _<moduleName>_ OR --name _<moduleName>_ REQUIRED
-t _(proc|con|ref)_ OR --type _(proc|con|ref)_ OPTIONAL
-a _<assemblyFile>_ OR --assembly _<assemblyFile>_ OPTIONAL
-c _<componentName>_ OR --component _<componentName>_ OPTIONAL
-s <sourceFileName> OR --source <sourceFileName> OPTIONAL
-d <moduleDestinationPath> OR --destination <moduleDestinationPath> OPTIONAL

The _-t_ or _--type_ option specifies the type of module. The options are _proc_ for procedure, _con_ for concept, and _ref_ for reference. By default, the program uses _proc_. You may override the default with the _-t_ or _--type_ option on the command line, or set a new default in the _fccAddModule.conf_ configuration file. _Procedure_ is the most common module type so it is the default value.

The component name should be the product name or a sub-component of the product.

The _-s_ or _--source__ option refers to an existing text file. Specifying an existing text file will import the text of the file after the heading. __The program truncates the first line to trim anchor tags. If your file does not have an anchor tag, and a carriage return at the first line to use this features.

The _-d_ or _--destination_ option is the destination path for the module. In Red Hat's Flexible Customer Content (FCC) format, module files often live in a different folder from the _master.adoc_ file and assembly files. You may override the default with the _-d_ or _--destination_ option on the command line, or set a new default in the _fccAddModule.conf_ configuration file. Make sure to add an ending slash (_e.g._, _directory/_ not _directory_). 
