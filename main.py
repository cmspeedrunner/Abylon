import sys
import os
import time
os.system("")

###---> Setting up all the constants and lists to be appended to <---###
TokenPrefix = ["FUNCTION:", "OUTPUT:", "VARIABLE:", "RETURN:", "PUT:"] # This is the token prefix
Identifiers = ["fun", "write", "var", "return", "put"] # This is what the transpiler is searching for, it matches it up to the list above

class colors:
 

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
 
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
 
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
 





TokList = [] # This is the list that the tokenprefix values are put into, if the matching identifier in the "Identifiers" list is found
ValList = [] # This is where the value of whatever token is found is put, for example, it will look for functions by searching with the "Identifiers" list for "fun"
# If it finds "fun", it will append to the TokList "FUNCTION:" and then it will find the value of the function (eg. main(){) and append it here



CAbylon = ["#include <stdio.h>", "#include <stdbool.h>", "#include <string.h>", "#include <stdlib.h>"] # This is for the C code, appending to this as the program transpiles to create the matching c code.

###---###

###---> Open the file <---###
try:
    fileName = sys.argv[1]
except IndexError as err:
    print(colors.fg.red+"═════════"+colors.fg.orange+"ERROR: No file given"+colors.fg.red+"═════════"+colors.reset)
    print(colors.fg.orange+"You passed the command: "+colors.fg.red+str(sys.argv[0])+colors.reset)
    print(colors.fg.orange+"Expected: "+colors.fg.green+str(sys.argv[0])+" filename.abyl"+colors.reset)


try:
    with open(fileName) as File:
        Content = File.read()
        File.close()
except NameError as err:
    exit()
###---###

###---> This function just searches through each line, splits it up, and searches for the identifier, if it finds one, it appends it and its value to both TokList and ValList <---###
def Tokenize(line):
    tokenList = line.split() # Split up the line given into single words
    
    for i, tokens in enumerate(tokenList): # For each word in the new split line
        for i2, identifier in enumerate(Identifiers): # and for each identifier in the list
            if tokens == identifier: # if we find a word in the line that matches up
                GetValue = line.split(identifier) # split the line from that point and get everything to the right of it
                GetValue = "".join(GetValue) # remove all the blank space from the left of it
                TokList.append(TokenPrefix[i2]) # append the token type to the token list, eg "FUNCTION:" if it finds a function
                ValList.append(GetValue.strip()) # append the formatted value to the value list, eg "main(){"
###---###


###---> Split the user file code into lines and call the tokenise function into it<---###
ContentLines = Content.splitlines()
for i, item in enumerate(ContentLines):
    if item.strip() != "": # If the line is blank, just skip it
        Tokenize(item)
###---###
        

VarNames = []
VarTypes = []
VarValues = []
def Assemble(TokenList, ValueList):
    
    
    def caseFunc():
        defaultFunType = "void"
        FuncName = ValueList[i]
        for i2, item in enumerate(TokenList):
            if item == "RETURN:":
                returnValue = ValueList[i2]
                if str(returnValue).isdigit():
                    defaultFunType = "int"
        CAbylon.append(defaultFunType+" "+FuncName)
        

    
    def caseWrite(nl):
        outputValue = ValueList[i]
        
        
        if str(outputValue).startswith("\"") and str(outputValue).endswith("\""):
            CPrintCall = "printf("
            if "+" in str(outputValue):
                args = str(outputValue).split("+")
                removeConcat = str(outputValue).replace("+", ",")
                toadd = "%s"*len(args)
                CPrintCall = CPrintCall + "\""+toadd+nl+"\", "+removeConcat+");"
                CAbylon.append(CPrintCall)
            else:
                CPrintCall = CPrintCall +outputValue+");"
                CPrintCall= str(CPrintCall).replace("\");",nl+"\");")
                CAbylon.append(CPrintCall)

        elif "+" in str(outputValue):
                args = str(outputValue).split("+")
                
                for argNum, arg in enumerate(args):

                    if arg.strip().isdigit():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"

                    elif "." in arg.strip():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"  
                    
                    elif arg.strip() == "true" or arg.strip() == "false":
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"  
                        

                    elif arg.strip().isalnum():
                        CPrintCall = "printf(\""
                        

                        for varNums, var in enumerate(VarNames):
                            if arg.strip() == var:
                                VarTypeRef = str(VarTypes[varNums])
                                
                                if VarTypeRef == "INT: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "STRING: ":
                                    removeConcat = str(outputValue).replace("+", ",")
                                    argLength = len(args)-1
                                    toadd = "%s"*argLength
                                    CPrintCall = CPrintCall+toadd+"%s"+nl+"\", "+removeConcat+");"
                                elif VarTypeRef == "FLOAT: ":
                                    CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "BOOL: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "STRING INPUT: ":
                                    removeConcat = str(outputValue).replace("+", ",")
                                    argLength = len(args)-1
                                    toadd = "%s"*argLength
                                    CPrintCall = CPrintCall+toadd+"%s\", "+removeConcat+");"
                                elif VarTypeRef == "INT INPUT: ":
                                    CPrintCall = CPrintCall+"%d\", "+outputValue+");"
                                elif VarTypeRef == "FLOAT INPUT: ":
                                    CPrintCall = CPrintCall+"%f\", "+outputValue+");"
                                    
                CAbylon.append(CPrintCall)  
        elif "-" in str(outputValue):
                args = str(outputValue).split("-")
                
                for argNum, arg in enumerate(args):

                    if arg.strip().isdigit():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"

                    elif "." in arg.strip():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"  
                    
                    elif arg.strip() == "true" or arg.strip() == "false":
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"  
                        

                    elif arg.strip().isalnum():
                        CPrintCall = "printf(\""
                        

                        for varNums, var in enumerate(VarNames):
                            if arg.strip() == var:
                                VarTypeRef = str(VarTypes[varNums])
                                
                                if VarTypeRef == "INT: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "STRING: ":
                                    
                                    print(colors.fg.red+"═════════"+colors.fg.orange+"TRANSPILER ERROR: Invalid operation"+colors.fg.red+"═════════"+colors.reset)
                                    print(colors.fg.orange+"Your code includes the operation: '"+colors.fg.red+str(ValueList[i])+colors.fg.orange+"'")
                                    print(colors.fg.blue+"\n═════════"+colors.fg.orange+"VARIABLE TABLE"+colors.fg.blue+"═════════")
                                    for iv, item in enumerate(VarNames):
                                        print(colors.fg.cyan+"VARIABLE NAME: "+colors.fg.blue+item + colors.fg.cyan+" VARIABLE TYPE: "+colors.fg.blue+str(VarTypes[iv])+colors.fg.cyan+" VARIABLE VALUE: "+colors.fg.blue+str(VarValues[iv])+colors.fg.blue)
                                    print("════════════════════════════════")
                                    print(colors.fg.orange+"The variables: "+colors.fg.blue,VarNames,colors.fg.orange+" are both strings and you cannot subtract strings"+colors.reset)

                                    
                                    exit()
                                elif VarTypeRef == "FLOAT: ":
                                    CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "BOOL: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"   
                CAbylon.append(CPrintCall)  
        elif "*" in str(outputValue):
                args = str(outputValue).split("*")
                
                for argNum, arg in enumerate(args):

                    if arg.strip().isdigit():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"

                    elif "." in arg.strip():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"  
                    
                    elif arg.strip() == "true" or arg.strip() == "false":
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"  
                        

                    elif arg.strip().isalnum():
                        CPrintCall = "printf(\""
                        

                        for varNums, var in enumerate(VarNames):
                            if arg.strip() == var:
                                VarTypeRef = str(VarTypes[varNums])
                                
                                if VarTypeRef == "INT: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "STRING: ":
                                    print(colors.fg.red+"═════════"+colors.fg.orange+"TRANSPILER ERROR: Invalid operation"+colors.fg.red+"═════════"+colors.reset)
                                    print(colors.fg.orange+"Your code includes the operation: '"+colors.fg.red+str(ValueList[i])+colors.fg.orange+"'")
                                    print(colors.fg.blue+"\n═════════"+colors.fg.orange+"VARIABLE TABLE"+colors.fg.blue+"═════════")
                                    for iv, item in enumerate(VarNames):
                                        print(colors.fg.cyan+"VARIABLE NAME: "+colors.fg.blue+item + colors.fg.cyan+" VARIABLE TYPE: "+colors.fg.blue+str(VarTypes[iv])+colors.fg.cyan+" VARIABLE VALUE: "+colors.fg.blue+str(VarValues[iv])+colors.fg.blue)
                                    print("════════════════════════════════")
                                    print(colors.fg.orange+"The variables: "+colors.fg.blue,VarNames,colors.fg.orange+" are both strings and you cannot multiply strings in Abylon yet"+colors.reset)

                                    
                                    exit()
                                elif VarTypeRef == "FLOAT: ":
                                    CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "BOOL: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"   
                                
                                    

                CAbylon.append(CPrintCall)  
        
        elif "/" in str(outputValue):
                args = str(outputValue).split("/")
                
                for argNum, arg in enumerate(args):

                    if arg.strip().isdigit():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"

                    elif "." in arg.strip():
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"  
                    
                    elif arg.strip() == "true" or arg.strip() == "false":
                        CPrintCall = "printf(\""
                        CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"  
                        

                    elif arg.strip().isalnum():
                        CPrintCall = "printf(\""
                        

                        for varNums, var in enumerate(VarNames):
                            if arg.strip() == var:
                                VarTypeRef = str(VarTypes[varNums])
                                
                                if VarTypeRef == "INT: ":
                                    CPrintCall = CPrintCall+"%.1f"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "STRING: ":
                                    print(colors.fg.red+"═════════"+colors.fg.orange+"TRANSPILER ERROR: Invalid operation"+colors.fg.red+"═════════"+colors.reset)
                                    print(colors.fg.orange+"Your code includes the operation: '"+colors.fg.red+str(ValueList[i])+colors.fg.orange+"'")
                                    print(colors.fg.blue+"\n═════════"+colors.fg.orange+"VARIABLE TABLE"+colors.fg.blue+"═════════")
                                    for iv, item in enumerate(VarNames):
                                        print(colors.fg.cyan+"VARIABLE NAME: "+colors.fg.blue+item + colors.fg.cyan+" VARIABLE TYPE: "+colors.fg.blue+str(VarTypes[iv])+colors.fg.cyan+" VARIABLE VALUE: "+colors.fg.blue+str(VarValues[iv])+colors.fg.blue)
                                    print("════════════════════════════════")
                                    print(colors.fg.orange+"The variables: "+colors.fg.blue,VarNames,colors.fg.orange+" are both strings and you cannot divide strings"+colors.reset)

                                    
                                    exit()
                                elif VarTypeRef == "FLOAT: ":
                                    CPrintCall = CPrintCall+"%f"+nl+"\", "+outputValue+");"
                                elif VarTypeRef == "BOOL: ":
                                    CPrintCall = CPrintCall+"%d"+nl+"\", "+outputValue+");"   
                                
                                    

                CAbylon.append(CPrintCall)  
                         
                                

        elif str(outputValue).isdigit():
            
            CPrintCall = "printf(\"%d\", "+str(outputValue)+");"
            
            CAbylon.append(CPrintCall)


        elif "." in str(outputValue):
            CPrintCall = "printf(\"%f\", "+str(outputValue)+");"
            
            CAbylon.append(CPrintCall)


        elif str(outputValue).isalnum():
            CPrintCall = "printf(\""
            
            
            for y, item in enumerate(VarNames):
                if item == outputValue:
                    VariableTypeRef = str(VarTypes[y])
                    if VariableTypeRef == "STRING: ":
                        CPrintCall = CPrintCall +"%s"+nl+"\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
                    if VariableTypeRef == "INT: ":
                        CPrintCall = CPrintCall +"%d"+nl+"\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
                    if VariableTypeRef == "BOOL: ":
                        CPrintCall = CPrintCall +"%d"+nl+"\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
                    if VariableTypeRef == "FLOAT: ":
                        CPrintCall = CPrintCall +"%f"+nl+"\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
                    if VariableTypeRef == "STRING INPUT: ":
                        CPrintCall = CPrintCall +"%s\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
                    if VariableTypeRef == "INT INPUT: ":
                        CPrintCall = CPrintCall +"%d\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
                    if VariableTypeRef == "FLOAT INPUT: ":
                        CPrintCall = CPrintCall +"%f\", "+outputValue+");"
                        CAbylon.append(CPrintCall)
        
    
        
    
    def caseVariable():
        
        lineFull = str(ValueList[i])
        
        variables = (lineFull.split())
        
        varname = variables[0]
        operand = variables[1]
        value = lineFull.split(operand)[1].strip()
        arglistNum = []
        arglistStr = ["\""]
        if variables[2] == "readStr":
            inputString = value.replace("readStr", "").strip()
            VarNames.append(varname)
            VarValues.append("User input")
            VarTypes.append("STRING INPUT: ")
            CVariableCall = "printf("+inputString+");"
            CAbylon.append(CVariableCall)
            CVariableCall = "char "+varname+"[50];"
            CAbylon.append(CVariableCall)
            CVariableCall = "fgets("+varname+", 50, stdin);"
            CAbylon.append(CVariableCall)
            CVariableCall = varname+"[strcspn("+varname+", \"\\n\")] = 0;"
            CAbylon.append(CVariableCall)
            
            
        elif variables[2] == "readInt":
            inputString = value.replace("readInt", "").strip()
            VarNames.append(varname)
            VarValues.append("User input")
            VarTypes.append("INT INPUT: ")
            CVariableCall = "int "+varname+";"
            CAbylon.append(CVariableCall)
            CVariableCall = "printf("+inputString+");"
            CAbylon.append(CVariableCall)
            CVariableCall = "scanf(\"%d\", &"+varname+");\ngetchar();"
            CAbylon.append(CVariableCall)
        elif variables[2] == "readFlt":
            inputString = value.replace("readFlt", "").strip()
            VarNames.append(varname)
            VarValues.append("User input")
            VarTypes.append("FLOAT INPUT: ")
            CVariableCall = "float "+varname+";"
            CAbylon.append(CVariableCall)
            CVariableCall = "printf("+inputString+");"
            CAbylon.append(CVariableCall)
            CVariableCall = "scanf(\"\\n%f\", &"+varname+");\ngetchar();"
            CAbylon.append(CVariableCall)

        elif varname not in VarNames:
            VarNames.append(varname)
            VarValues.append(value)
            
            if "+" in value:
                
                if value.startswith("\"") and value.endswith("\""):
                
                    args = list(value) 
            
                    for a, item in enumerate(args):
                        if item == "\"":
                            arglistNum.append(a)             
                    StringNumber = int(len(arglistNum))     
                    for b in range(0, StringNumber-1):
                        string = "".join(args[arglistNum[b]:arglistNum[b+1]])
                        string = string.replace("\"", "")
                        if string.strip() != "+":
                            arglistStr.append(string)
                    arglistStr.append("\\n\"")         
                    value = "".join(arglistStr)

                    VarTypes.append("STRING: ")
                    CVariableCall = "char *"+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)
                
                else:
                    args = value.split("+")
                    Type = ""
                    catArgs = []
                    firstarg = args[0].strip()
                    for c, item in enumerate(args):
                        varArg = (item.strip())
                        
                        for c2, item2 in enumerate(VarNames):
                            if varArg == item2:
                                varTypeof = VarTypes[c2]
                                Type = varTypeof
                                if varTypeof == "STRING: ":
                                    if "\"" in "".join(args):
                                        getValue = str(VarValues[c2]).replace("\"", "")
                                        args[args.index(item)] = getValue.strip()
                                        args = "".join(args).replace("\"", "")
                                        replaced = "\""
                                        valueOf = replaced+args+"\""
                                        CVariableCall = "char *"+str(varname) + " "+str(operand)+ " "+valueOf+";"
                                    else:
                                        arglistStr.append(str(VarValues[c2]).replace("\"", ""))
                                    
                                        valueOf = "".join(arglistStr)
                                        valueOf = valueOf+"\""
                                        CVariableCall = "char *"+str(varname) + " "+str(operand)+ " "+valueOf+";"
                                    
                                elif varTypeof == "STRING INPUT: ":
                                    Type = "STRING: "
                                    
                                    valueOf = value.replace("+", ",")
                                    
                                    CVariableCall = "char "+str(varname)+"[50];"
                                    
                                    CVariableCall = CVariableCall + ("\nstrcpy("+str(varname)+", "+firstarg+");\n")
                                    catArgs.append("strcat("+str(varname)+", "+str(varArg)+");")
                                    
                                    
                                elif varTypeof == "INT: ":
                                    valueOf = value
                                    CVariableCall = "int "+str(varname) + " "+str(operand)+ " "+valueOf+";"
                                elif varTypeof == "INT INPUT: ":
                                    valueOf = value
                                    CVariableCall = "int "+str(varname) + " "+str(operand)+ " "+valueOf+";"
                                elif varTypeof == "FLOAT: ":
                                    valueOf = value
                                    CVariableCall = "float "+str(varname) + " "+str(operand)+ " "+valueOf+";"

                                elif varTypeof == "FLOAT INPUT: ":
                                    valueOf = value
                                    CVariableCall = "float "+str(varname) + " "+str(operand)+ " "+valueOf+";"
                                elif varTypeof == "BOOL: ":
                                    valueOf = value
                                    CVariableCall = "bool "+str(varname) + " "+str(operand)+ " "+valueOf+";"
                            else:
                                
                                if args[0].strip().isdigit():
                                    valueOf = value
                                    Type = "INT: "
                                    CVariableCall = "int "+str(varname) + " "+str(operand)+ " "+valueOf+";"

                                elif "." in args[0].strip():
                                    valueOf = value
                                    Type = "FLOAT: "
                                    CVariableCall = "float "+str(varname) + " "+str(operand)+ " "+valueOf+";"
                                elif args[0].strip() == "true" or args[0].strip() == "false":
                                    valueOf = value
                                    Type = "BOOL: "
                                    CVariableCall = "bool "+str(varname) + " "+str(operand)+ " "+valueOf+";"

                                
                    
                    VarTypes.append(Type)
                    VarValues[VarValues.index(value)] = valueOf
                    CAbylon.append(CVariableCall)
                    if len(catArgs) > 0:
                        catArgs.pop(0)
                        CAbylon.append("\n".join(catArgs))

                    
                
            
                
            elif "." in value:
                VarTypes.append("FLOAT: ")
                CVariableCall = "float "+str(varname) + " "+str(operand)+ " "+value+";"
                CAbylon.append(CVariableCall)

            elif value.strip() == "true" or value.strip() == "false":
                VarTypes.append("BOOL: ")
                CVariableCall = "bool "+str(varname) + " "+str(operand)+ " "+value+";"
                CAbylon.append(CVariableCall)

            
                    

            elif value.isalpha() and value.isdigit() == False:
                Location = VarNames.index(value)
                TypeOfVar = VarTypes[Location]
                VarTypes.append(TypeOfVar)
                
                
                if str(TypeOfVar) == "STRING: ":
                    CVariableCall = "char *"+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)
                elif str(TypeOfVar) == "FLOAT: ":
                    CVariableCall = "float "+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)
                elif str(TypeOfVar) == "INT: ":
                    CVariableCall = "int "+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)
                elif str(TypeOfVar) == "BOOL: ":
                    CVariableCall = "bool "+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)
            else:
                if value.startswith("\"") and value.endswith("\""):
                    VarTypes.append("STRING: ")
                    CVariableCall = "char *"+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)
                else:
                    VarTypes.append("INT: ")
                    CVariableCall = "int "+str(varname) + " "+str(operand)+ " "+value+";"
                    CAbylon.append(CVariableCall)

                
            

            

        elif varname in VarNames:
            Location = (VarNames.index(varname))
            VarValues[Location] = value
            vartype = (VarTypes[Location])
            

            if value.startswith("\"") and value.endswith("\""):
                if "+" in value:
                    
                    args = list(value)
                    for a, item in enumerate(args):
                        if item == "\"":
                            arglistNum.append(a)             
                    StringNumber = int(len(arglistNum))     
                    for b in range(0, StringNumber-1):
                        string = "".join(args[arglistNum[b]:arglistNum[b+1]])
                        string = string.replace("\"", "")
                        if string.strip() != "+":
                            arglistStr.append(string)
                    arglistStr.append("\"")         
                    value = "".join(arglistStr)
                CVariableCall = str(varname) + " "+str(operand)+ " "+value+";"
                CAbylon.append(CVariableCall)

            elif "\"" in value:
                args = value.split("+")
               
                for num, givenVar in enumerate(args):
                    args[num] = args[num].strip()
                    for num2, names, in enumerate(VarNames):
                        if givenVar.strip() == names.strip():
                            givenVar=(givenVar.strip())
                            VarLoc = VarNames.index(names.strip())
                            getValue = str(VarValues[VarLoc])

                
                args ="".join(args).replace("\"", "").strip()
                
                args = args.replace(givenVar.strip(), getValue.replace("\"", ""))
                VarValues[Location] = "\""+args+"\""
                CVariableCall = str(varname) + " "+str(operand)+ " \""+args+"\";"
                CAbylon.append(CVariableCall)
            elif "." in value:
                VarTypes.append("FLOAT: ")
                CVariableCall = str(varname) + " "+str(operand)+ " "+value+";"
                CAbylon.append(CVariableCall)
            elif value.strip() == "true" or value.strip() == "false":
                VarTypes.append("BOOL: ")
                CVariableCall = str(varname) + " "+str(operand)+ " "+value+";"
                CAbylon.append(CVariableCall)

            elif value.isdigit:
                VarTypes.append("INT: ")
                CVariableCall = str(varname) + " "+str(operand)+ " "+value+";"
                CAbylon.append(CVariableCall)
            
            

    for i, item in enumerate(TokenList):
        
        if item == "FUNCTION:":
            caseFunc()
        if item == "OUTPUT:":
            
            caseWrite("\\n")
        if item == "VARIABLE:":
            caseVariable()
        if item == "RETURN:":
            CReturnCall = "return "+ValueList[i]+";"
            CAbylon.append(CReturnCall)
        if item == "PUT:":
            caseWrite("")


        
    
    

Assemble(TokList, ValList)
CAbylon.append("}")


def debug():

    print(colors.fg.purple+"\n═════════"+colors.fg.green+"C CODE"+colors.fg.purple+"═════════"+colors.fg.cyan)
    for i, item in enumerate(CAbylon):
        print(colors.fg.green+str(i)+":   "+colors.fg.cyan+item)
    print(colors.fg.purple+"\n═══════════════════════════"+colors.reset)



    


try:    
    with open(fileName.split(".")[0]+".c", "x") as f:

        for i, item in enumerate(CAbylon):
            f.write(item +"\n")
        f.close()

except FileExistsError:
    with open(fileName.split(".")[0]+".c", "w") as f:
        for i, item in enumerate(CAbylon):
            f.write(item +"\n")
        f.close()


commandslist = " ".join(sys.argv)

start = time.time()
os.system("gcc "+fileName.split(".")[0]+".c -o "+fileName.split(".")[0]+".exe")
stop = time.time()-start

if "-t" in commandslist:
    print(colors.fg.cyan+"Compiled in "+colors.fg.green+colors.underline+str(stop)[0:5]+"s"+colors.reset)
    

if "-c" in commandslist:
    debug()
    

if "-f" not in commandslist:
    os.remove(fileName.split(".")[0]+".c")

if "-v" in commandslist:
    print(colors.fg.blue+"\n═════════"+colors.fg.orange+"VARIABLE TABLE"+colors.fg.blue+"═════════")
    for iv, item in enumerate(VarNames):
        
        print(colors.fg.cyan+"VARIABLE NAME: "+colors.fg.blue+item + colors.fg.cyan+" VARIABLE TYPE: "+colors.fg.blue+str(VarTypes[iv])+colors.fg.cyan+" VARIABLE VALUE: "+colors.fg.blue+str(VarValues[iv])+colors.fg.blue)
    print("════════════════════════════════"+colors.reset)
if "-r" in commandslist:
    os.system(fileName.split(".")[0])