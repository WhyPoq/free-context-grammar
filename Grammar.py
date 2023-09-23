
from random import *


class Grammar:

    def __init__(self):
        self.rules = {}

    def addRule(self, name, result):
        self.rules[name] = result

    def removeRule(self, name):
        self.rules.pop(name)

    def trimLeft(self, s):
        if(len(s) > 0 and s[0] == ' '):
            s = s[1:]
        return s

    def trimRight(self, s):
        if(len(s) > 0 and s[len(s) - 1] == ' '):
            s = s[:-1]
        return s

    def splitMultiple(self, s):
        elements = s.split(';')
        for i in range(len(elements)):
            elements[i] = self.trimLeft(elements[i])
        return elements

    def chooseMultiple(self, elements):
        return elements[randrange(0, len(elements))]

    def chooseMultipleProb(self, elements):
        return elements[randrange(0, len(elements))]

    def readVariables(self, input):
        isVarsPart = True
        varsPart = ""
        inputPart = ""
        for c in input:
            if(isVarsPart and c == '|'):
                isVarsPart = False
            elif(isVarsPart and c != '(' and c != ')'):
                varsPart += c
            elif(not isVarsPart):
                inputPart += c

        wereArgs = True
        if(isVarsPart):
            wereArgs = False

        if(not wereArgs):
            varsPart = ""
            inputPart = input
            
        varsPart = self.trimRight(varsPart)
        if(wereArgs):
             inputPart = self.trimLeft(inputPart)

        return (varsPart, inputPart)

    def setVariables(self, varsPart, arguments):
        variables = {}
        varsStr = self.splitMultiple(varsPart)
        for i in range(len(varsStr)):
            el = varsStr[i]
            namePart = True
            varName = ""
            varVal = ""
            for c in el:
                if(namePart and c == '='):
                    namePart = False
                elif(namePart):
                    varName += c
                else:
                    varVal += c

            if(i < len(arguments)):
                variables[varName] = self.getResult(arguments[i])
            elif(not namePart):
                varName = self.trimRight(varName)
                varVal = self.trimLeft(varVal)
                variables[varName] = self.getResult(varVal)

        return variables

    def getArguments(self, input):
        argsPart = True
        arguments = ""
        element = ""
        for c in input:
            if(argsPart and c != '(' and c != ')'):
                arguments += c
            elif(argsPart and c == ')'):
                argsPart = False
            elif(not argsPart):
                element += c

        if(argsPart):
            element = arguments
            arguments = ""
        else:
            arguments = self.trimRight(arguments)
            element = self.trimLeft(element)
        return arguments, element

    def getChoiceArgs(self, input):
        argsPart = True
        arguments = ""
        element = ""
        for c in input:
            if(argsPart and c != '{' and c != '}'):
                arguments += c
            elif(argsPart and c == '}'):
                argsPart = False
            elif(not argsPart):
                element += c

        needLeft = ""
        needRight = ""
        needInfo = 0
        probCoeff = 1
        if(argsPart):
            element = arguments
            arguments = []
        else:
            element = self.trimLeft(element)
            arguments = self.trimRight(arguments)
            arguments = self.splitMultiple(arguments)

        if(len(arguments) >= 1):
            isLeftPart = True
            lastC = ' '
            for c in arguments[0]:
                if(isLeftPart and lastC == '!' and c == '='):
                    isLeftPart = False
                    needInfo = -1
                elif(isLeftPart and lastC == '=' and c == '='):
                    isLeftPart = False   
                    needInfo = 1
                elif(isLeftPart and c != '!' and c != '='):
                    needLeft += c
                elif(not isLeftPart):
                    needRight += c
                lastC = c
        if(len(arguments) >= 2):
            probCoeff = int(arguments[1][:-1]) / 100
        needLeft = self.trimRight(needLeft)
        needRight = self.trimLeft(needRight)
        return needLeft, needRight, needInfo, probCoeff, element
                

    def getResult(self, input, arguments=[]):
        varsPart, input = self.readVariables(input)
        variables = self.setVariables(varsPart, arguments)

        stack = [""]
        i = 0
        while(i < len(input)):
            if(input[i] == '#'):
                element = ""
                i += 1
                while(i < len(input) and input[i] != '#'):
                    element += input[i]
                    i += 1
                if(element in variables):
                    stack[len(stack) - 1] += variables[element]      
            elif(input[i] == '@'):
                element = ""
                i += 1
                while(i < len(input) and input[i] != '@'):
                    element += input[i]
                    i += 1
                stack[len(stack) - 1] += '@' + element + '@'            
            elif(input[i] == '<' or input[i] == '['):
                stack.append("")
            elif(input[i] == '>'):
                element = stack.pop()
                arguments, element = self.getArguments(element)
                if(arguments != ""):
                    arguments = self.splitMultiple(arguments)
                if(element in self.rules):
                    element = self.rules[element]
                stack[len(stack) - 1] += self.getResult(element, arguments)
            elif(input[i] == ']'):
                elements = self.splitMultiple(stack.pop())
                pickedElements = []
                for element in elements:
                    needLeft, needRight, needInfo, probCoeff, el = self.getChoiceArgs(element)
                    if(needInfo == 1 and self.getResult(needLeft) == self.getResult(needRight)):
                        pickedElements.append(el)
                    elif(needInfo == -1 and self.getResult(needLeft) != self.getResult(needRight)):
                        pickedElements.append(el)
                    elif(needInfo == 0):
                        pickedElements.append(el)

                if(len(pickedElements) == 0):
                    element = "error"
                else:
                    element = self.chooseMultiple(pickedElements)

                stack[len(stack) - 1] += self.getResult(element)
            else:
                stack[len(stack) - 1] += input[i]

            i += 1
        
        output = stack.pop()
        return output

    def applyModifiers(self, input):
        output = "";
        i = 0
        noNextSpace = False
        nextCap = False
        while(i < len(input)):
            if(input[i] == '$'):
                element = ""
                i += 1
                while(i < len(input) and input[i] != '$'):
                    element += input[i]
                    i += 1
                if(element == "eS"):
                    noNextSpace = True
                if(element == "eSL"):
                    if(len(output) > 0 and output[len(output) - 1] == ' '):
                        output = output[:-1]
                elif(element == "cap"):
                    nextCap = True
                elif(element == "capS"):
                    nextCap = True
                    if(i + 1 < len(input) and input[i + 1] == ' '):
                        i += 1

            else:
                adding = input[i]
                if(adding == ' ' and noNextSpace): adding = ""
                if(nextCap): 
                    adding = adding.capitalize()

                output += adding

                noNextSpace = False
                nextCap = False

            i += 1 

        return output

    def run(self, input, arguments=[]):
        result = self.getResult(input, arguments)
        result = self.applyModifiers(result)

        return result
        
                
    