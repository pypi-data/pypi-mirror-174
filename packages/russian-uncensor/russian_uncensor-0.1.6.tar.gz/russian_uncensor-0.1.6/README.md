# russian_uncensor
Welcome to ***Russian Uncenscor***! This library helps you find original forms of the obscene words in your text
based on statistical information from collected dictionary of the obscene words: frequent single letters, bi-grams and 
tri-grams. This is a simple instrument for your NLP tasks which you can use for cleaning text, restore gaps and even use
in moderation task etc.

## Installation
You can find [this project on PyPi](https://pypi.org/project/russian-uncensor/)

To install using pip:
`pip install russian_uncensor`

Or just clone project repository:
```
git clone https://github.com/AlexKly/russian_uncensor 
python setup.py develop
```

## Usage
Supported main functions:
- extract from dict of the obscene words and get n-grams
- perform uncensoring of the masked obscene words in sentence
- perform uncensoring of the splitted obscene words in sentence

Example how to use it is [here](https://github.com/AlexKly/russian_uncensor/blob/master/example.py)

Also, you can check tests to understand how to use library.
[Check this](https://github.com/AlexKly/russian_uncensor/blob/master/tests/test_russian_uncensor.py)

### Quickstart
If you want to run uncensor quickly and use it with default settings, you need to import `Uncensor()` and 
use following functions:
```
# Import uncensor:
from russian_uncensor import uncensored

text = 'obscene_word'
# Call uncensor and find suitable variants of obscene word:
uncensor = uncensored.Uncensor()
uncensored_masked = uncensor.uncensor_masked(text)
uncensored_splitted = uncensor.uncensor_splitted(text)

print('Uncensored in masked word: ', uncensored_masked)
print('Uncensored in splitted word: ', uncensored_masked)
```

## N-grams and WordStats
`WordStats()` use information from dictionary of obscene words `russian_uncensor/data/obscene_words.txt` to build
dictionaries all possible n-grams and frequent single letters, which you can meet in your Russian text. If you want to
use default settings, you don't need to use this class, but if you have custom dictionary of swear words you use it.
Specify the path to your file as a parameter, and also you can change the location of the stats dictionaries which 
you will get in output.
```
custom_ws = WordStats(
    dict_path=custom_path,
    neg_words_fn=my_dict_neg_words_filename_i,
    freq_letters_fn=custom_freq_letters_filename_o,
    bigrams_fn=custom_bi_grams_filename_o,
    trigrams_fn=custom_tri_grams_filename_0,
    debug=True
)
```
To calculate statistical elements and get it use `custom_wc.get_n_grams()` or `custom_wc.save_n_grams()`

## Uncensor
The `Uncensor()` also can work with default dictionary and with your custom. Just you need to specify paths to your
dictionaries with *frequent words*, *bi_grams* and *tri_grams* which you got running `WordStats().save_n_grams` using
custom dictionary.

**Uncensor** can find variants of the uncensored single words, so you need to take this into account when you will use it in
your project. **Uncensor** after applying substitutions will return all possible variants based on statistics based on
power of your origin dictionary, and the less clear the word, the more variants it will return. If it is not possible 
to recover, then **Uncensor** will return *None*. Nowadays, **Uncensor** can not to perform substitutions and return
variants if in uncensored words masked more than 3 consecutive letters. Notice that.

When you perform `Uncensor().uncensor_splitted()` method return set ***(particles positions in text, united particle)***.
You can use particles positions to unite these particles into one word correctly.

***Good Luck and Have Fun!***