"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    if list1 == []:
        return []
    ans = [list1[0]]
    for idx in range(len(list1)):
        if list1[idx] != ans[-1]:
            ans.append(list1[idx])
    return ans

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    ans = []
    if list1 == [] or list2 == []:
        return ans
    idx, jdx = 0, 0
    while idx < len(list1) and jdx < len(list2):
        if list1[idx] == list2[jdx]:
            ans.append(list1[idx])
            idx += 1
            jdx += 1
        elif list1[idx] < list2[jdx]:
            idx += 1
        else:
            jdx += 1
    return ans

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """  
    ans = []
    if list1 == [] or list2 == []:
        ans += list1 + list2
        return ans
    idx, jdx = 0, 0
    while idx < len(list1) and jdx < len(list2):
        if list1[idx] < list2[jdx]:
            ans.append(list1[idx])
            idx += 1
        else: 
            ans.append(list2[jdx])
            jdx += 1
    if idx == len(list1) and jdx != len(list2):
        ans += [list2[num] for num in range(jdx, len(list2))]
    elif idx != len(list1) and jdx == len(list2):
        ans += [list1[num] for num in range(idx, len(list1))]
    return ans
    
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    mid = len(list1) / 2
    left = list1[0:mid]
    right = list1[mid:len(list1)]
    return merge(merge_sort(left), merge_sort(right))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    ans = []
    if len(word) < 1:
        ans.append(word)
        return ans
    first = word[0]
    rest = word[1:len(word)]
    rest_strings = gen_all_strings(rest)
    for string in rest_strings:
        for idx in range(len(string)):
            temp = string[0:idx] + first + string[idx:len(string)]
            ans.append(temp)
        ans.append(string + first)
    return ans + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    dictionary = []
    netfile = urllib2.urlopen(codeskulptor.file2url(filename)) 
    for line in netfile.readlines():
        dictionary.append(line[:-1])
    return dictionary

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()





    
    
