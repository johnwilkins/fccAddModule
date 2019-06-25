#!/usr/bin/python

# This program creates module files in the flexible content format.
# It creates the file, file name, module ID, heading anchor and heading.
# The program must run in the same directory as the master.adoc and assembly files.

import os
import sys
import getopt
import ConfigParser

def main(argv):

    #Load the default values to save time on CLI usage.
    configParser = ConfigParser.RawConfigParser()
    configParser.read('./fccAddModule.conf')
    moduleType = configParser.get('fcc-add-module-conf', 'defaultModuleType')
    moduleDestinationPath = configParser.get('fcc-add-module-conf', 'moduleDestinationPath')
    moduleSourcePath = configParser.get('fcc-add-module-conf', 'moduleSourcePath')
    moduleSourceFileName = ""
    componentType = configParser.get('fcc-add-module-conf', 'defaultComponentType')
    locale = configParser.get('fcc-add-module-conf', 'defaultLocale')
    fileExtension = configParser.get('fcc-add-module-conf', 'fileExtension')
    ctx = "-{context}"
    assemblyFileName = ""

    try:
        moduleName = ""

        #define command line arguments.
        opts, args = getopt.getopt(argv,"n:t:c:a:s:",["name=","type=","component=","assembly=","source="])

        for opt, arg in opts:
            if opt in ("-n", "--name"):
                moduleName = arg
            elif opt in ("-t", "--type"):
                moduleType = arg
            elif opt in ("-c", "--component"):
                componentType = arg
            elif opt in ("-a", "--assembly"):
                assemblyFileName = arg
            elif opt in ("-s", "--source"):
                moduleSourceFileName = arg

        if moduleName == "":
            print ("\nERROR: Module name is required! Use the -n or --name option.\n")
            printUsage()
            sys.exit()

        lowercaseModuleName = moduleName.lower()
        baseModuleId = lowercaseModuleName.replace(' ', '-')


        outputFileName = moduleDestinationPath + moduleType + "_" + componentType + "_" + baseModuleId + "_" + locale + fileExtension
        moduleId = "[id='" + baseModuleId + ctx + "']"

        if moduleSourceFileName != "":
            sourceFile = open(moduleSourcePath + moduleSourceFileName, 'r')
            sourceFile.next()

        outFile = open(outputFileName, 'w') #output file to write to.
        outFile.write(moduleId + "\n\n")
        outFile.write("= " + moduleName + "\n")
        print ("\n- Added module ID\n- Added module heading.")

        if moduleSourceFileName != "":
            for line in sourceFile:
                outFile.write(line)
            print("- Added module source")

        includeText = "include::{includedir}/" + outputFileName + "[leveloffset=+1]"

        if assemblyFileName != "":
            assemblyFile = open(assemblyFileName, 'a')
            assemblyFile.write("\n" + includeText + "\n")
            print("- Added include to assembly file.")

        print ("Output File: " + outputFileName)
    except OSError as e:
        print(str(e))

    except getopt.GetoptError:
        #printUsage()
        sys.exit(2)




def printUsage():
        print "You may specify the options in any order.\nThe fccAddModule.py helper program will create a new module in the flexible customer content/modular format.\nThis helper program MUST run in the same directory as the master.adoc file.\nTo incorporate existing topic content, use the -s or --source option.\nNOTE: The -s or --source will omit the first line to erase the existing [[anchor-tag]].\nTo APPEND an include statement to an assembly, use the -a or --assembly option.\nThe assembly file SHOULD exist already; however, you may create a file without the required formatting on-the-fly.\nTo override the default component type in fccAddModule.conf, use the -c or --component option."
        print "\nUsage: \n$ python fccAddModule.py -n '<moduleName>' [options] \n\nOPTIONS:\n"
        print "-n '<moduleName>' OR --name '<moduleName>' (REQUIRED)"
        print "-t (proc|con|ref) OR --type (proc|con|ref) OPTIONAL. DEFAULT = proc"
        print "-a <assemblyFile> OR --assembly <assemblyFile> (OPTIONAL)"
        print "-c <componentName> OR --component <componentName> (e.g., 'osp', 'ceph') May set default in fccAddModule.conf"
        print "-s <sourceFileName> OR --source <sourceFileName> The source file to include. OPTIONAL\n"
        print "-d <moduleDestinationPath> OR --destination <moduleDestinationPath> The destination path for the module. (OPTIONAL)"

if __name__ == "__main__":
    main(sys.argv[1:])
