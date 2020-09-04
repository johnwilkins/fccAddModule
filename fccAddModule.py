#!/usr/bin/python

# This program creates module files in the flexible content format.
# It creates the file, file name, module ID, heading anchor and heading.
# The program must run in the same directory as the master.adoc and assembly
# files. If you specify the -o option, it will rename the module, include the
# assembly include directive if -a is specified.

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
    componentType = configParser.get('fcc-add-module-conf', 'defaultComponentType')
    locale = configParser.get('fcc-add-module-conf', 'defaultLocale')
    fileExtension = configParser.get('fcc-add-module-conf', 'fileExtension')

    #Initialize variables
    ctx = "_{context}"
    assemblyFileName = ""
    oldName = ""
    moduleName = ""

    try:

        #define command line arguments.
        opts, args = getopt.getopt(argv,"n:o:t:c:a:d:h",["name=","old=","type=","component=","assembly=", "destination=", "help"])

        for opt, arg in opts:
            if opt in ("-n", "--name"):
                moduleName = arg
            elif opt in ("-o", "--old"):
                oldName = arg
            elif opt in ("-t", "--type"):
                moduleType = arg
            elif opt in ("-c", "--component"):
                componentType = arg
            elif opt in ("-a", "--assembly"):
                assemblyFileName = arg
            elif opt in ("-d", "--destination"):
                moduleDestinationPath = arg
            elif opt in ("-h", "--help"):
                printUsage()
                sys.exit()

        #fccAddModule ALWAYS requires a module name.
        if moduleName == "":
            print ("\nERROR: Module name is required! Use the -n or --name option.\n")
            printUsage()
            sys.exit()

        #Create a heading comment for the file header.
        headingComment = getHeadingComment(assemblyFileName)

        #The outputModuleId is a component of the outputFileName and moduleID.
        outputModuleId = getModuleID(moduleName)

        moduleId = "[id='" + outputModuleId + ctx + "']"

        outputFileName = createFileName(moduleDestinationPath, moduleType, componentType, outputModuleId, locale, fileExtension)

        includeText = getIncludeDirective(outputFileName)

        #Test if oldName exists, and rename the module if it does.
        if oldName !="":
            # The inputModuleId is derived from the old name and to parse get inputFileName and old moduleID during rename operations.
            inputModuleId = getModuleID(oldName)

            inputFileName = createFileName(moduleDestinationPath, moduleType, componentType, inputModuleId, locale, fileExtension)

            inputFile = open (inputFileName, 'r')
            moduleData = inputFile.read()
            inputFile.close()

            moduleMod = moduleData.replace(inputModuleId, outputModuleId)
            moduleData = moduleMod.replace(oldName, moduleName)

            outFile = open(outputFileName, 'w') #output file to write to.
            outFile.write(moduleData)
            outFile.close()

            os.remove(inputFileName)
            print ("\n- Renamed module from" + oldName + "\nto:\n" + moduleName)

            if assemblyFileName != "":
                assemblyFile = open(assemblyFileName, 'r')
                assemblyData = assemblyFile.read()
                assemblyFile.close()

                inputIncludeText = getIncludeDirective(inputFileName)
                modifiedAssemblyData = assemblyData.replace(inputIncludeText, includeText)

                assemblyFile = open(assemblyFileName, 'w')
                assemblyFile.write(modifiedAssemblyData)
                assemblyFile.close()
            print ("\n- Renamed include text")

        else:
            outFile = open(outputFileName, 'w') #output file to write to.
            outFile.write(headingComment + "\n\n")
            outFile.write(moduleId + "\n\n")
            outFile.write("= " + moduleName + "\n")
            print ("\n- Added module heading.\n- Added module ID")

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


#Takes a title case string name of a module, and coverts it to a
#lowercase dash(-) delimited module ID for anchor tags and file names.
def getModuleID(name):
    lowercaseModuleName = name.lower()
    return lowercaseModuleName.replace(' ', '-')

#Takes destination path, module type, component type, module ID, locale and extension and creates a file name.
def createFileName(dpath, mtype, ctype, modId, locale, ext):
    return dpath + mtype + "_" + ctype + "_" + modId + "_" + locale + ext

#Takes an assembly file name and gets a heading comment.
def getHeadingComment(assemblyFileName):
    return "// This is included in the following assemblies:\n//\n// " + assemblyFileName

#Takes a file name and returns an include directive for the assembly file.
def getIncludeDirective(fileName):
        return "include::{includedir}/" + fileName + "[leveloffset=+1]"



def printUsage():
        print "\n\n====================\nfccAddModule.py Help\n====================\n\n\tThe fccAddModule.py helper program will create a new module in the flexible customer\n\tcontent/modular format. This helper program MUST run in the same directory as the\n\tmaster.adoc file. To incorporate existing topic content, use the -s or --source option.\n\tNOTE: The -s or --source will omit the first line to erase the existing [[anchor-tag]].\n\tTo APPEND an include statement to an assembly, use the -a or --assembly option.\n\tThe assembly file SHOULD exist already; however, you may create a file without\n\tthe required formatting on-the-fly. To override the default component type in\n\tfccAddModule.conf, use the -c or --component option."
        print "\nUSAGE: \n\t$ python fccAddModule.py -n '<moduleName>' [options] \n\nOPTIONS:\n"
        print "\t-n '<moduleName>' OR --name '<moduleName>' REQUIRED"
        print "\t-o '<oldModuleName>' OR --old '<oldModuleName>' OPTIONAL"
        print "\t-t (proc|con|ref|assembly) OR --type (proc|con|ref|assembly) OPTIONAL. DEFAULT = proc"
        print "\t-a <assemblyFile> OR --assembly <assemblyFile> OPTIONAL"
        print "\t-c <componentName> OR --component <componentName> OPTIONAL. For default see fccAddModule.conf."
        print "\t-d <moduleDestinationPath> OR --destination <moduleDestinationPath> The destination path for the module. OPTIONAL. DEFAULT = modules/.\n"

if __name__ == "__main__":
    main(sys.argv[1:])
