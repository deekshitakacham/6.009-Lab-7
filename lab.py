# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self, key_type):
        self.value = None
        #means that given key has no val associated with it
        self.children = {}
        #maps sequence to another trie node, next level
        self.key_type = key_type
        #set type based off input 


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        
        >>>  trie = lab.Trie(str)
        trie['cat'] = 'kitten'
        trie['car'] = 'tricycle'
        trie['carpet'] = 'rug'
        expect = read_expected('1.pickle')
        assert dictify(trie) == expect, "Your trie is incorrect."
        """
        if type(key) != self.key_type:
            raise TypeError
        
        if len(key) == 0:
          
            self.value = value
        #base case is when string is empty or tuple is empty, both len 0
        
        else: 
            #examine recursively
            after_vals = key[1:]
        
            #ark
            before_vals = key[:1]
            #b
           
            
            
            if before_vals not in self.children:
                #if tree doesn't exist
              
                self.children[before_vals] = Trie(self.key_type)
               
                #calls the trie layer after it 
                self.children[before_vals][after_vals] = value
                #get tree instance for 'b'
                
            
                #recursive step, makes 'ark' equal to value
                
            else: 
                #if tree already exists 
                trie_instance= self.children[before_vals] 
                #grabs the instance 
                trie_instance[after_vals] = value
                #sets 'ark' to value recursively 
                



    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        >>> t = Trie(str)
        >>> t['bark'] = ':)' 
        >>> t['bark']
        ':)'
        >>> t['apple']
        KeyError
        >>> t['ba']
        KeyError
        >>> t[1]
        TypeError
        
        """
        
        next_trie = self
        #self refers to the head node 
        
        if not isinstance(key, self.key_type):
            raise TypeError 
        #checks if key is of right type 
             
        for i in range(len(key)): 

            val = key[i:i+1]
            #loop through each val in string or tuple  
            
            if val not in next_trie.children:
                raise KeyError
                
            next_trie = next_trie.children[val]
            
        if next_trie.value is None:
            #in the case of 'ba'
            raise KeyError
            
        return next_trie.value
            
    

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
    
        >>> t = Trie(str)
        >>> t['bar'] = ':)' 
        >>> del t['ba']
        raise KeyError
        """
        next_trie = self
        #self refers to the head node 
        
        if not isinstance(key, self.key_type):
            raise TypeError 
        #checks if key is of right type 
             
        for i in range(len(key)): 

            val = key[i:i+1]
            #loop through each val in string or tuple 
             
            if val not in next_trie.children:
                raise KeyError
              
            next_trie = next_trie.children[val]
            
        if next_trie.value != None:
            next_trie.value = None
            
        elif next_trie.value == None:
            raise KeyError
        
            
        
    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        try: 
            if self.__getitem__(key) != None:
                return True
            else:
                return False 
            
        except:
            return False 



    def __iter__(self, key_seen = None):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator! Key_seen = list of key vals seen so far
        """
        #yield 
        #when you know what to output
        
        #yield from
        #returns (potentially unknown) values from a function
        if key_seen == None: 
            if self.key_type == str:
                key_seen = ''
            if self.key_type == tuple:
                key_seen = tuple()
        
        if self.value != None:
              
            yield (key_seen, self.value) 
         
            #making the list
        
         
        for i in self.children:
    
            path = key_seen+i
                
            yield from self.children[i].__iter__(path)
            
            #iterating through list


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    
    >>> text = 'my, name is apple apple apple named myriad.'
    >>> trie = Trie(str)
    >>> a = make_word_trie(text)
    >>> a['my']
    1

    """
    
    clean_text = tokenize_sentences(text)
    
    trie_instance = Trie(str)
    
    for sentence in clean_text:
       
        sentence_spaced = sentence.split()
    #separates the sentences with spaces
        for word in sentence_spaced:
       
    #trie_instance.__contains__(word)
    #dunder method
            if word in trie_instance: 
     
    #dunder method for set item 
                trie_instance[word] += 1
      
            else: 
                trie_instance[word] = 1
    
    return trie_instance  
        

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """

    clean_text = tokenize_sentences(text)
    trie_instance = Trie(tuple)

    for sentence in clean_text:
        sentences_spaced = sentence.split()
        tup_sentence = tuple(sentences_spaced) 
        #separates the sentences with spaces, makes final tuple
        if tup_sentence in trie_instance: 
            #dunder method for set item 
            trie_instance[tup_sentence] += 1
          
        else: 
            trie_instance[tup_sentence] = 1
      
    return trie_instance


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    if type(prefix) != trie.key_type:
        raise TypeError
        
    freq = []
    #list of words that have prefix, value is their frequency 
    
    for i in range(len(prefix)): 

        letter = prefix[i:i+1]
   
        #checks if prefix is in trie and goes down to next level, updating trie

        if letter in trie.children:
            
            trie = trie.children[letter]
            
        else: 
            #if prefix not in trie, return empty list 
            return []
        
    #invoking the iter method 
    for key, val in trie: 
        #make sure to concatenate key to prefix 
        new_key = prefix+key
        freq.append((new_key, val))
        
    #sort freq list 
    freq.sort(reverse = True, key=lambda x: x[1])
    
    #get list of max_count size 
    
    result = []
    
    if max_count == None: 
        count = len(freq)
    else:
        count = min(max_count, len(freq))
    
        
    for i in range(count):
        result.append(freq[i])
        
    #get a list of just the words (no value)
    final_result = []
    for tup in result: 
        final_result.append(tup[0])
        
    return final_result 
        
            
def character_insert(prefix):
    """
    Helper function to insert a letter into the prefix.
    """

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    result = set()
    
    for i in range(len(prefix)+1):
        for letter in letters: 
            result.add(prefix[:i]+letter+prefix[i:])
            
    return result


def character_single_delete(prefix):
    """
    Helper function to delete a letter from the prefix
    """
    
    result = set()
    
    for i in range(len(prefix)):
        result.add(prefix[:i]+prefix[i+1:])
            
    return result 

    
def character_single_replace(prefix):
    """
    Helper function to replace a letter in the prefix
    """
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    result = set()

    for i in range(len(prefix)):
        for letter in letters:
            result.add(prefix[:i]+letter+prefix[i+1:])
            
    return result
        
        
    
def character_two_transpose(prefix):
    """
    Helper function to transpose two letters in the prefix
    """
    result = set()
    
    for i in range(len(prefix)-1):
        #always have n-1 transpositions 
        val = (prefix[:i]+ prefix[i+1:i+2] + prefix[i:i+1] + prefix[i+2:])
        result.add(val)
            
    return result
            
        
    

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    words = autocomplete(trie, prefix, max_count)
    result = words.copy()
    
    if max_count == len(words):
        return words
    
    #if max_count is equal to length of words, just return autocomplete output
    
    #get all words that start with prefix
    
    
    else: 
        #max_count == None or max_count != len(words):
     
        #make copy of words list 
        all_words = character_insert(prefix) | character_single_delete(prefix) | character_single_replace(prefix) | character_two_transpose(prefix)
        #get words with all the edits, use sets to save time and make sure no repeats 
        actual_words = {}
        #dictionary to store words with their frequencies 
        
        set_words = set(words)
        
        for word in all_words:
            #dunder for contains
            if word not in set_words: 
                if word in trie:
                    #creates word in dictionary with frequency as the value
                    actual_words[word] = trie[word]
                
            
        sorted_actual = {k: v for k, v in sorted(actual_words.items(), key=lambda item: item[1])}
        #sort dictionary 
        keys = list(sorted_actual.keys())
        keys.reverse()
        #reverse keys 
                        
        if max_count is None:
            return result+keys
        
        #if none, return everything
        
            
        else: 
            count = max_count-len(words)
            return result+keys[:count]
        
        #else, return the remaining 
         
def word_recurse(trie, pattern, og_trie, prefix, freq):
    if len(pattern) == 1: 
        if pattern == '*':
            #build up prefix as we recurse, no max_count 
            
            words = autocomplete(og_trie, prefix)
    
            for word in words:
                if word not in freq:
                    freq[word] = og_trie[word]
                    
                
                
        elif pattern == '?':
            for i in trie.children: 
                #only look through key values
                if i in trie: 
                    if prefix+i not in freq: 
                        freq[prefix+i] = trie[i]
                
          
        else:
            if pattern in trie: 
                if prefix+pattern not in freq: 
                    freq[prefix+pattern] = trie[pattern]
                    
                    
        return freq
    
    if pattern[0] == '*':
       #two cases = ignoring or adding another word
       
       #skipping asterick
       word_recurse(trie, pattern[1:], og_trie, prefix, freq)
       
       for i in trie.children:
           
           word_recurse(trie.children[i], pattern, og_trie, prefix+i, freq)
           #do not decrease pattern to look at all the letters
           #prefix changing due to adding other letter
      
   
    elif pattern[0] == '?':
        for i in trie.children: 
           word_recurse(trie.children[i], pattern[1:], og_trie, prefix+i, freq) 
    
    else:
        if pattern[0] in trie.children: 
            print(pattern[0])
            print(prefix)
            word_recurse(trie.children[pattern[0]], pattern[1:],og_trie, prefix+pattern[0], freq) 
    
    return freq
        
                 
            


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    prefix = ''
    freq = {}
    og_trie = trie 
    return list(word_recurse(trie, pattern, og_trie, prefix, freq).items())


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    #doctest.testmod()
        
#    text = 'my, name is apple apple apple named myriad.'
#    text2 = 'a man at the market murmered that he had met a mermaid. ''mark didnt believe the man had met a mermaid.'
#    trie = Trie(str)
#    a = make_word_trie(text2)
#    print(list(iter(a)))
#    
#    
#    ['owrd', 'wrod', 'wodr']
#    
#    lis = ['word']
#    pre = 'word'

    #print(character_single_delete(lis, pre))
    #print(character_insert(lis, pre))
    #print(character_single_replace(lis, pre))
    #print(character_two_transpose(lis, pre))
    
    with open("metamorphosis.txt", encoding="utf-8") as f:
        text1 = f.read()
        
    with open("a tale of two cities.txt", encoding="utf-8") as f:
        text2 = f.read()
        
    with open("dracula.txt", encoding="utf-8") as f:
        text3 = f.read()
        
    with open("alice in wonderland.txt", encoding="utf-8") as f:
        text4 = f.read()
        
    with open("pride and prejudice.txt", encoding="utf-8") as f:
        text5 = f.read()
    
    
    #Question 1 
    alice_phrase = make_phrase_trie(text4)
    print(autocomplete(alice_phrase, (), 6))
    
    #Question 2
    moph_word = make_word_trie(text1) 
    print(autocorrect(moph_word, 'gre', 6))
    
    #Question 3
    print(word_filter(moph_word, 'c*h'))
    
    #Question 4
    tale_word = make_word_trie(text2)
    print(word_filter(tale_word, 'r?c*t'))
    
    #Question 5
    alice_word = make_word_trie(text4)
    print(autocorrect(alice_word, 'hear', 12))
    
    #Question 6
    pride_word = make_word_trie(text5)
    print(autocorrect(pride_word, 'hear'))
    
    