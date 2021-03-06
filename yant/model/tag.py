import os
import logging
import pickle

from yant.utils import yant_utils


class TagManager:
    # TODO: make this a singleton

    def __init__(self):
        self.is_tag_loaded = False
        data_path = yant_utils.get_data_path()
        self.filename = os.path.join(data_path, "tag.dat")
        self.logger = logging.getLogger("TagManager")
        try:
            self.load_tag()
        except:
            self.logger.warn("Cannot load tags, creating a new tag file...")
            all_books = yant_utils.list_all_books()
            self.data = {"all":all_books}
            self.save_tag()

    def __str__(self):
        return "TagManager"

    def load_tag(self):
        if self.is_tag_loaded:
            return
        with open(self.filename, "rb") as tag_fp: 
            self.data = pickle.load(tag_fp)
        self.is_tag_loaded = True

    def save_tag(self):
        with open(self.filename, "wb") as tag_fp:
            pickle.dump(self.data, tag_fp)

    def get_tags(self):
        return list(self.data.keys())

    def get_books(self, tag):
        if tag not in self.data:
            self.logger.warning("Tag {0} doesn't exist in TagManager.".format(tag))
            return []
        else:
            return self.data[tag]

    def get_mapping(self):
        return self.data

    def tag_book(self, tag, book):
        try:
            if tag not in self.data:
                self.data[tag] = [book]
                self.save_tag()
            elif book not in self.data[tag]:
                self.data[tag].append(book)
                self.save_tag()
            else:
                self.logger.warning(book + " already has tag " + tag + ". skip.")
        except:
             self.logger.error("Apply tag to book failed.")

    def untag_book(self, tag, book):
        try:
            if tag not in self.data:
                self.logger.error("Tag {0} doesn't exist in TagManager.".format(tag))
            elif book not in self.data[tag]:
                self.logger.error(book + " doesn't have the tag " + tag + ".")
            else:
                self.data[tag].remove(book)
                if self.data[tag] == []:
                    self.logger.warning("No book has the tag '" + tag + "' now. Remove the tag.")
                    del self.data[tag]
                self.save_tag()
        except:
            self.logger.error("Remove the tag from book failed.")

