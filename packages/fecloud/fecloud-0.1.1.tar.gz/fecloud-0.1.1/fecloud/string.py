import random
import datetime

def spacingEndline(num):
    space=""
    endline="\n"
    for _ in range(num):
        space+=endline
    return space

def spacingSpace(num):
    space=""
    endline=" "
    for _ in range(num):
        space+=endline
    return space

def fullCapitalize(content):
    return content.upper()

def joinStringFromList(listString):
    temp=""
    for ils,ls in enumerate(listString):
        temp+=ls
        if(ils!=len(listString)):
            temp+="\n"
    
    return temp

def ampEncoder(input_string):
    input_string=input_string.replace("&Delta;","AMP_DELTA")
    input_string=input_string.replace("&diamondsuit;","AMP_DIAMONDSUIT")
    input_string=input_string.replace("&clubs;","AMP_CLUBS")
    input_string=input_string.replace("&nbsp;","AMP_NBSP")
    return input_string

def ampDecoder(input_string):
    input_string=input_string.replace("AMP_DELTA","&Delta;")
    input_string=input_string.replace("AMP_DIAMONDSUIT","&diamondsuit;")
    input_string=input_string.replace("AMP_CLUBS","&clubs;")
    input_string=input_string.replace("AMP_NBSP","&nbsp;")
    return input_string

def stringMatchFromList(input_string, input_list):
    for il in input_list:
        if(il in input_string):
            return True
        else:
            continue

    return False


def removeSpecialCharacters(input_string):
    special_character_string='''~`!@#$%^&*()_-+={[}]|\:;"'<,>.?/'''
    special_character_array=[c for c in special_character_string]

    output_string=input_string
    for sca in special_character_array:
        output_string=output_string.replace(sca,"")

    return output_string




def stringToUpperCase(input_string):
    return input_string.upper()



def stringToLowerCase(input_string):
    return input_string.lower()



def extraStringSpaceStrip(input_string):
    output_string=" ".join(input_string.split())
    return output_string





def stringToSet(input_string):
    output_string=input_string.split()
    return set(output_string)



def stringToList(input_string):
    input_string=input_string.split()
    return input_string



def listToString(input_list):
    return " ".join(input_list)










def extraSpaceStrip(input_string):
    output_string=input_string
    for _ in range(len(input_string)):
        output_string=output_string.replace("  "," ")
    return output_string





def stringPreprocess1(input_string):
    output_string=input_string
    output_string=extraSpaceStrip(output_string)
    output_string=stringToLowerCase(output_string)
    output_string=removeSpecialCharacters(output_string)
    return output_string


def setMatchScore1(input_set1, input_set2):
    output_set=input_set1.intersection(input_set2)
    return len(output_set),output_set


def randomCharStream(moreLen=4, withTimeStamp = True):
    charArray = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    stream = ""
    for _ in range(moreLen):stream+=str(charArray[random.randint(0,len(charArray)-1)] )
    
    if(withTimeStamp == True):
        ddnsc = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":","_").replace(".","_")
        return stream + "_" + ddnsc
    else:
        return stream


def randomNumberStream(tokenLen=4):
    stream = ""
    for _ in range(tokenLen):stream+=str(random.randint(0,9))
    return stream