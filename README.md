#Yant: Yet Another Note Tool

Yant is a pure commandline note tool. It supports note operations such as *add*
(of course!), *remove*, *update*, *search*, *review* (I love this
feature), *import*, *export*, *fortune*, etc. With Yant, you can quickly find
your memory with one command. Moreover, you can do a two-step random review of
your notes! Think that you have taken tons of notes while learning something
new, and you want to fortify your new knowledge by reviewing notes from time to
time. Yant can do this perfectly for you. For each flashcard, it first pops a note
title (e.g. a new word), then after your press [Enter], more information shows
up (e.g. meaning of the word). The reviewing process is *random*, which means
you can avoid just reviewing the first few notes again and again.

Check it out and have fun with it!

##Installation

```
git clone git@github.com:pl53/yant.git
cd yant
bash install.sh
```

You can also download the zip file. After upzipping` it, you should see a folder
*yant-master*.

```
cd yant-master
bash install.sh
```


Note: require Python version >= 3.

##Usage example
```
$ yant create -b "where_my_stuff"
Book where_my_stuff created.
```
```
$ yant add -b where_my_stuff passport
Add a note for passport (press Enter to finish): bottom drawer, steel box
Add a note for passport (press Enter to finish): 
Flashcard added/updated to book 'where_my_stuff'.
```
```
$ yant find passport
==Match #1==
BOOK: where_my_stuff, TITLE: passport
#1: bottom drawer, steel box
```

##Basic usages
The command pattern is *yant [subcommand] [parameters and options]*, similar
to commandline tools such as git.

### Create notebook
To create a notebook, simply use the *create* subcommand.
```
yant create -b BOOK
```

You can also specify tags for the book with "-t" option and/or description with
"--desc" option. See ```yant create -h``` for details.

Note: You can use yant without explicitly creating any book. Yant creates a
default book *scratchpad* for you. If you don't specify a notebook in command,
*yant* uses *scratchpad*.

### Delete notebook
The subcommand is *destroy*. You should be absolutely sober when typing this
command.

### Add flashcard
Each notebook is a collection of **flashcards**, each of which consists of a
**title** and unlimited **notes**. To add a new flashcard,

```
usage: yant add [-h] [--notes NOTES] [-b BOOK] title

positional arguments:
  title                 title of the new flashcard

optional arguments:
  -h, --help            show this help message and exit
  --notes NOTES         notes separated by semicolons
  -b BOOK, --book BOOK  book name, use default 'scratchpad' if not specified
```

Then yant will prompt you to input notes for this flashcard if ```--note```
option not provided. After successfully adding a flashcard, yant computes a hash
code for this flashcard (like ```git```'s commit reference), you can late use
this hashcode to update the flashcard with the ```-k``` option.

Note: If the note title contains special characters such as space and dash, you
should quote it.

### Update flashcard

You can update **notes** of a flashcard using subcommand *update* or *up*.
Updating **title** is not supported currently, but it is in my upgrading plan.

```
usage: yant update [-h] (-k KEY | -t TITLE) [-b BOOK]

optional arguments:
  -h, --help            show this help message and exit
  -k KEY                hashkey of the flashcard
  -t TITLE              title of the flashcard
  -b BOOK, --book BOOK  book name, use default 'scratchpad' if not specified
```
Then yant will ask you for further commands, such as delete a note, replace a
note, or append note notes.

### Delete flashcard
```
yant remove [-h] (-k KEY | -t TITLE) [-b BOOK]
```
You can also use *delete*, *del*, or *rm* instead of *remove*.

### Search notes
```
yant find [-h] [-w] [-b BOOK | -t TAG] [--exec EXEC] keyword

positional arguments:
  keyword               keyword for search, support wild character

optional arguments:
  -h, --help            show this help message and exit
  -w                    Select only those flashcards containing matches the
                        whole word
  -b BOOK, --book BOOK  book name
  -t TAG, --tag TAG     tag name
  --exec EXEC           command executed on each node, use {0} for flashcard
                        title, {i} for note #i, {+} for all notes.
```

Each notebook has attached with one or more tags, and you can apply a subcommand
on books with the same tag, e.g. you can search all notes with a tag "tech".

An advanced feature of find is the *--exec* option. You can specify command to
execute on the flashcard title. For example, if the book title is a word, you
can execute *sdcv* for its meaning.

### Tag a book
As mentioned earlier, each books is associate with tags. "all" is the default
tag attached to all books automatically by *yant*.

```
yant tag [-h] [-d] -b BOOK tags

positional arguments:
  tags                  a list of tags separated by ';'

optional arguments:
  -h, --help            show this help message and exit
  -d                    delete the tags if option is speficified
  -b BOOK, --book BOOK  book name
```

### List books
You can see all existing notebooks you have created, or all books associated
with the same tag, or etails of a book. If neither "-b" nor "-t" is specified,
all books are displayed.
```
yant list [-h] [-b BOOK | -t TAG]

optional arguments:
  -h, --help            show this help message and exit
  -b BOOK, --book BOOK  book name
  -t TAG, --tag TAG     tag name
```

### Review flashcards
This is my favorate feature and the reason that I wrote *yant*.

```
yant review [-h] (-b BOOK | -t TAG) [--exec EXEC]

optional arguments:
  -h, --help            show this help message and exit
  -b BOOK, --book BOOK  book name
  -t TAG, --tag TAG     tag name
  --exec EXEC           command executed on each node, use {0} for flashcard
                        title, {i} for note #i, {+} for all notes.
```
Try it out. I believe you will like it.

### Fortune cookie

This subcommand randomly pick a flashcard and display it, similar to the
*fortune* command of unix.

```
yant fortune [-h] [-b BOOK | -t TAG]

optional arguments:
  -h, --help            show this help message and exit
  -b BOOK, --book BOOK  book name
  -t TAG, --tag TAG     tag name
```

### Export a notebook

This subcommand dumps all flashcards in readable texts to a specified file or
console if you don't provide a file.
```
yant export [-h] -b BOOK [--file FILE]

optional arguments:
  -h, --help            show this help message and exit
  -b BOOK, --book BOOK  book name
  --file FILE           exporting file, stdout by default
```

### Import a notebook

You can import flashcards from an exported file.

```
yant import [-h] -b BOOK --file FILE

optional arguments:
  -h, --help            show this help message and exit
  -b BOOK, --book BOOK  book name
  --file FILE           file to import from
```

##Tips

1. By default, data are stored in $HOME/.yanote. You can change the default data
   location by setting environment variable ```YANT_PATH```.

2. You can specifiy multiple ```--exec``` commands by using ```;``` as a separator.
