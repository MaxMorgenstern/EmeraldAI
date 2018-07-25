#!/usr/bin/python
# -*- coding: utf-8 -*-

def MinimumEditDistance(string1,string2):
    if len(string1) > len(string2):
        string1,string2 = string2,string1
    distances = range(len(string1) + 1)
    for index2,char2 in enumerate(string2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(string1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]


def LevenshteinDistance(string1, string2):
    m = len(string1)
    n = len(string2)
    lensum = float(m + n)
    d = []
    for i in range(m+1):
        d.append([i])
    del d[0][0]
    for j in range(n+1):
        d[0].append(j)
    for j in range(1,n+1):
        for i in range(1,m+1):
            if string1[i-1] == string2[j-1]:
                d[i].insert(j,d[i-1][j-1])
            else:
                minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)
                d[i].insert(j, minimum)
    ldist = d[-1][-1]
    ratio = (lensum - ldist)/lensum
    return {'distance':ldist, 'ratio':ratio}
