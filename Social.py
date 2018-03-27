#Trie Based off of Steve Hanov's implementation of Levenshtein Distance
#His website is here: http://stevehanov.ca/blog/index.php?id=114
#More efficient implementation than first one
#Less space and less operations
#Important: Used PyPy as Interpreter, See README for more details
class Trie:
    def __init__(self):
        self.word = None
        #Dictionary of Letters mapped to a new Trie
        self.children = {}
        #Boolean to check if tree has been searched before
        self.searched = False
    def insert(self, word):
        '''
        :param word: Word (string) to be inserted into tree
        :return: None
        '''
        parent = self
        #Traverses through the tree to find appropriate letters
        for i in word:
            if i not in parent.children:
                parent.children[i] = Trie()
            parent = parent.children[i]
        parent.word = word


def search_neighbors_helper(tree, letter, word, prev_row_cost, word_list):
    '''
    Recursive helper to search for words with editDistance of <= 1
    :param tree: Current Trie object to be traversed through
    :param letter: Current letter (string) of the trie object
    :param word: word (string) to search for
    :param prev_row_cost: rowCost of the previous letter (int)
    :param word_list: List of words that are friends
    :return: None
    '''
    word_col = len(word) + 1
    current_row_cost = [prev_row_cost[0] + 1]
    for i in range(1, word_col):
        #Definition of Levenshtein Distance
        #Calculates the supposed insert_cost and delete_cost to be used as defined by Levenshtein distance
        insert_cost = current_row_cost[i - 1] + 1
        delete_cost = prev_row_cost[i] + 1
        if word[i-1] != letter:
            sub_cost = prev_row_cost[i - 1] + 1
        else:
            #If no letter is substituted
            sub_cost = prev_row_cost[i - 1]
        #Levenshtein Distance is the minimum of the three costs
        current_row_cost.append(min(insert_cost, delete_cost, sub_cost))
    #Checks to see if Levenshtein distance exceeds 1, if not, and current Trie is a word, append it to the list to return
    #Checks to see if we traversed through the tree before to not double count
    if current_row_cost[-1] <= 1 and tree.word is not None and tree.searched is False:
        word_list.append(tree.word)
        tree.searched = True
    #Continues down the trie to find friends if edit distance does not exceed 1
    if min(current_row_cost) <= 1:
        for i in tree.children:
            search_neighbors_helper(tree.children[i], i, word, current_row_cost, word_list)


def search(tree, need_to_find):
    '''
    Main search method to find all friend
    :param tree: Current Trie object to be traversed through
    :param need_to_find: List of words that has friends yet to be found
    :return: Number of words in the social link of need_to_find
    '''
    #Counter starts at -1 because we need to traverse through
    #the original word twice, but do not want to double count it
    counter = -1
    while len(need_to_find)> 0:
        #increment counter every time we pop a neighbor
        counter += 1
        current_friend = need_to_find.pop()
        #Default cost to supply to recursive helper
        current_row_cost = (range(len(current_friend) + 1))
        for i in tree.children:
            search_neighbors_helper(tree.children[i], i, current_friend, current_row_cost, need_to_find)
    return counter

def set_up_dictionary_from_text(file_name):
    '''
    :param file_name: Dictionary in .txt format
    :return: list of all words from dictionary
    '''
    with open(file_name, 'r') as word_list:
        words = word_list.read().split()
    return words
def set_up_tree(social_links):
    '''
    :param file_name: Dictionary in .txt format
    :return: list of all words from dictionary
    '''
    tree = Trie()
    for i in social_links:
        tree.insert(i)
    return tree

def find_all_links(tree, keyword):
    '''
    :param tree: Trie object containing dictionary
    :param keyword: word (string) to find friends for
    :return: the number of friends in the word's social link
    '''
    neighbors = [keyword]
    return search(tree, neighbors)


