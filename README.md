Yanote: A CLI notebook tool

* Goal

  The primary goal of Yanote is storing information or knowledge as key-value
  pairs for later queries or review. 

* Feature

  - support multiple notebooks;
  - support add, delete, update, and search notes;
  - support RANDOM review of notes in the same book;
  - support building English vocabulary.

* Installation 

  After downloading yanote.tar.gz
  ```
  $ tar -xzf yanote.tar.gz
  $ cd yanote
  $ sudo sh install.sh
  ```
  *Require Python 3 to run*.

* Usage examples

  - create a notebook named "magic": 
```
       $ yanote -c magic
```
  - add my bestbuy reward number ("1234"): 
```
       $ yanote magic -a "bestbuy reward" 
       Add a note for bestbuy reward: 1234
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

  - Use "-w" to call "sdcv" and "forvo" to show the meaning and pronounce the
    *key*, which is very useful for building vocabulary. "forvo" is a CLI client
    for forvo.com. You can download it from github.com/pl53/forvo-linux-client

  - By default, database files are stored in ~/.yanote. If you need to save them
    in another directory (e.g. Dropbox folder), you can set the YANOTE_PATH env.

For bugs and suggestions, please send emails to lipeng.net at gmail dot com.
