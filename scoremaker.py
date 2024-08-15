from soynlp.hangle import jamo_levenshtein

def scoreing(s1,s2):
    d=jamo_levenshtein(s1, s2)
    l=max(len(s1),len(s2))
    return (l-d)/l*100


s1 = '가족'
s2 = '가죽'
print(jamo_levenshtein(s1, s2))
print(scoreing(s1,s2))