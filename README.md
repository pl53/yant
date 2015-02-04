Yanote: A CLI notebook tool

* Goal
  - The primary goal of Yanote is storing information or knowledge as key-value
  pairs for later queries or review. Note that entries in a notebook are
  un-ordered.

* Feature
  - support create, import, and export notebooks;
  - support add, delete, update, and search note entries;
  - support *random* review of entries in the same notebook;
  - support building English vocabulary.

* Requirement
  - Python 3

* Installation 
  - After downloading yanote.tar.gz
  ```
  $ tar -xzf yanote.tar.gz
  $ cd yanote
  $ sudo sh install.sh
  ```

* Usage examples
  - create a notebook named "magic": 
```
       $ yanote -c magic
```
  - add my bestbuy reward number ("1234"): 
```
       $ yanote magic -a "bestbuy reward" 
       Add an entry for bestbuy reward: 1234
       One record added/updated.
```
  - search my bestbuy reward number:
```
       $ yanote magic -s bestbuy
       ==Match #1==
       Key: bestbuy reward
       #1: 1234
```
  For complete usage, see "yanote -h"
 
* Advanced features
  - When adding an English word entry, use "-w" indicate it is a word, such as "yanote
	wordbook -w -a some_new_word." so Yanote will call "sdcv" and "forvo" to
    show the meaning and pronounce the word when showing it. "forvo" is a CLI client
    for forvo.com written by myself.  You can download it from
    https://github.com/pl53/forvo-linux-client

  - By default, database files are stored in ~/.yanote. You change the database
    directory (e.g. Dropbox folder) by setting the YANOTE_PATH env.

For bugs and suggestions, please send emails to lipeng.net at gmail dot com.

* TODO
  - support wildcard search
  - add encryption option
