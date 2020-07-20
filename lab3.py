from collections import Counter
from re import sub

def getFile(fileName):
    file = open(fileName, encoding='utf-8')
    return file

def getText(file):
    text = file.read()
    file.close()
    text = sub('\ufeff', '', text)
    text = sub('\n', '', text)
    return text

def findMostCommonBigrams(alph, text):
    bigram = Counter()
    for letter1 in alph:
        for letter2 in alph:
            bigram[letter1+letter2]=0;
    for letter in range(0,len(text)-1, 2):              
        bigram[text[letter]+text[letter+1]]+=1          
    return list(dict(bigram.most_common(5)).keys())    
    

def main():
    alph = "абвгдежзийклмнопрстуфхцчшщьыэюя"
    fileName = 'variants/15.txt'
    text = getText(getFile(fileName))
    theMostCommonBigramsInLanguage = ['ст', 'но', 'то', 'на', 'ен']
    theMostCommonBigramsInText = findMostCommonBigrams(alph, text)
    decryptAffineCipher(theMostCommonBigramsInLanguage, theMostCommonBigramsInText, alph, text, fileName)
      

def advancedEuclideanAlgorithm(num1, num2):   # u*num1 + v*num2 = gcd(num1, num2)
    if(num2==0):
        return (num1, 1, 0)
    else:
        (greatestCommonDivisior, u, v) = advancedEuclideanAlgorithm(num2, num1 % num2)
        return (greatestCommonDivisior, v, u - num1//num2*v)   # gcd, u - reverced, v


def solutionOfLinearComparisons(num1, num2, b):                # num1*x = b*mod(num2)
    greatestCommonDivisior = advancedEuclideanAlgorithm(num1, num2)[0]
    solutions = []
    if greatestCommonDivisior == 1:
        solutions.append((advancedEuclideanAlgorithm(num1, num2)[1] * b) % num2)
        return solutions
    elif greatestCommonDivisior > 1:
        if b % greatestCommonDivisior != 0:
            solutions.append('No solutions')
            return solutions 
        else:
            num2 /= greatestCommonDivisior
            x0 = (advancedEuclideanAlgorithm(num1/greatestCommonDivisior, num2)[1] * (b/greatestCommonDivisior)) % num2
            for solution in range(0, greatestCommonDivisior):
                solutions.append(x0 + solution*num2)
            return solutions   
        

def decryptAffineCipher(languageBigrams, textBigrams, alph, text, fileName):
    bigramCombinations = [[lBigr, tBigr] for lBigr in languageBigrams for tBigr in textBigrams]
    for bigr in bigramCombinations:
        bigr[0] = alph.index(bigr[0][0])*31 + alph.index(bigr[0][1])
        bigr[1] = alph.index(bigr[1][0])*31 + alph.index(bigr[1][1])
    paramsA, paramsB = [], []
    for i in bigramCombinations:
        for j in bigramCombinations:
            if i[0]==j[0] or i[1] == j[1]:
                continue
            A = solutionOfLinearComparisons((i[0]-j[0]) % pow(31, 2), pow(31,2), (i[1]-j[1]) % pow(31,2))
            for x in A:
                if x != 'No solutions':
                    paramsA.append(x)
                    paramsB.append((i[1]- x*i[0])% pow(31,2))
    for par in range(len(paramsA)):
        encryptedText = ''
        a1 = advancedEuclideanAlgorithm(paramsA[par], pow(31,2))[1] % pow(31,2)
        for let in range(0, len(text)-1, 2):                                                                   
            bigramIndex =  alph.index(text[let]) * 31 + alph.index(text[let+1])
            encryptedText += (alph[int(((a1 * (bigramIndex - paramsB[par]) % pow(31, 2))//31) % len(alph))] + alph[int(((34 * (bigramIndex - 500) % pow(31, 2))%31) % len(alph))])
        if (0.0553-affinityIndex(encryptedText)) < 0.0015:
            print("Key: a= " + str(paramsA[par]) + " ,b= " + str(paramsB[par]) + " ,opposite a= " + str(a1))
            print('Encripted text for ' + fileName + ':\n' + encryptedText)
            break

def affinityIndex(text):
    affinityIndex = 0
    Dict = dict(Counter(text))
    for i in Dict:
        affinityIndex += (Dict[i]*(Dict[i]-1))
    affinityIndex /= (len(text)*(len(text)-1))
    return affinityIndex                    
                    
    
main()
