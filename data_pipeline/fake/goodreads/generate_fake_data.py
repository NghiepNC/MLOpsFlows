#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   generate_fake_data.py
@Time    :   2023/03/15 19:44:08
@Author  :   Duy Nam
@Version :   0.1
@Contact :   nam.nd.00@gmail.com
@Desc    :   MLOps Flows
'''

import os
import argparse
from typing import Any, List
from uuid import uuid4
from datetime import datetime
from collections import OrderedDict
import sys
import csv
import pandas as pd
from faker import Faker
from data_pipeline.utils.logger import Logging
from data_pipeline.fake.goodreads import config


class GoodreadsFake:
    """The Goodreads instance"""

    def __init__(self, base_directory: str = "") -> None:
        """The goodreadsfake instance initialization

        Args:
            base_directory (str, optional): The path to base directory. Defaults to None.
        """
        self.logging = Logging().get_logger()
        self._faker = Faker(['it_IT', 'en_US', 'hi_IN', 'ja_JP'])
        self._fake_books = [
            "Vacation People","Enter the Aardvark",
            "Murder Makes Scents",
            "A Blink of the Screen: Collected Shorter Fiction",
            "Living Your Dreams: How to make a living doing what you love",
            "The Bedroom Experiment(Hot Jocks #5.5)",
            "Sweet Soul (Sweet Home, #4; Carillo Boys, #3)",
            "Would Like to Meet",
            "House of Earth and Blood",
            "Ugly Betty: The Book",
            "The Favorite Daughter",
            "The East End",
            "Jinn'sDominion (Desert Cursed, #3",
            "Pine & Boof: The Lucky Leaf",
            "Beyond Belief: My Secret Life Inside Scientology and My Harrowing Escape",
            "Spark Joy: An Illustrated Master Class on the Artof Organizing and Tidying Up",
            "You've Been Volunteered: A Class Mom Novel",
            "Clown in a Cornfield",
            "Maksim (Akimov Bratva #1)",
            "Write or Wrong: A Dark College Romance (Write to Love Book 1)",
            "Bruno Has One Hundred Friends",
            "Mr. Cat and the Little Girl",
            "His Gift: A Valentine's Romance Novella",
            "The Crisis of Bad Preaching: Redeeming the Heart and Way of the Catholic Preacher",
            "TheItalian Villa",
            "The Tycoonâ€™s Fake FiancÃ©e (European Tycoon Book 2)",
            "Zaftig Dating Agency: Series Collection 4-",
            "Ra","The Mind Illuminated: A Complete Meditation Guide IntegratingBuddhist Wisdom and \
                Brain Science",
            "New Friends for Zaza",
            "Postmortem (Kay Scarpetta, #1)",
            "The Roman Spring of Mrs. Stone",
            "A Wizard of Earthsea",
            "Dragons & Magic (Dragon's Den Casino #1)"
        ]
        self._user_data_list: List[Any] = []
        self._review_data_list: List[Any] = []
        self._author_data_list: List[Any] = []
        self._book_data_list: List[Any] = []
        self._base_directory = base_directory if base_directory != "" \
            else config.GOODREADS_BASE_DIRECTORY

        if not os.path.exists(self._base_directory):
            os.makedirs(self._base_directory)
            self.logging.info("Created %s." % (self._base_directory))

    def generate(self, num_records: int = 0):
        """Generate the fake data follow the given num_records

        Args:
            num_records (int, optional): The number of records which to generate. Defaults to 0.
        """
        if num_records <= 0:
            self.logging.error("The number of records must be greater than 0, not %s" \
                               % str(num_records))
            sys.exit(1)

        for _ in range(num_records):
            review_obj = self._generate_fake_review_data()
            self._review_data_list.append(self._parse_review_data(review_obj))
            self._user_data_list.append(self._parse_user_data(review_obj))
            self._author_data_list.append(self._parse_author_data(review_obj))
            self._book_data_list.append(self._parse_book_data(review_obj))

        for module_name, module_data in zip(["reviews", "user", "author", "book"],
                                            [self._review_data_list, self._user_data_list,\
                                             self._author_data_list, self._book_data_list]):
            self.logging.info("Start to write to disk")
            self._write_to_disk(module_name, module_data)
            self.logging.info("Clear cache modules")
            self._clear_modules()

    def _generate_fake_review_data(self):
        """Generate fake review data
        """
        return {
            #Fake review
            "review_id" : self._faker.random_int(0, 10000000),
            "user_id" : self._faker.random_int(0, 100000),
            "book_id" : self._faker.random_int(0, 100000),
            "author_id" : self._faker.random_int(0, 100000),
            "review_text" : self._clean_text(self._faker.text()),
            "review_rating" : self._faker.pyfloat(right_digits = 2, min_value =0, max_value = 5),
            "review_votes" : self._faker.random_int(0, 1000000),
            "spoiler_flag" : bool(self._faker.random_int(0, 1)),
            "spoiler_state" : 'No state',
            "review_added_date": 'Tue Feb 11 18:08:25 -0800 2020',
            "review_updated_date": 'Tue Feb 11 18:18:25 -0800 2020',
            "review_read_count": self._faker.random_int(0, 1000000),
            "comments_count": self._faker.random_int(0, 1000000),
            "review_url": self._faker.image_url(),

            # Fake user
            "user_name": self._faker.name(),
            "user_display_name": self._faker.name(),
            "location": self._faker.address(),
            "profile_link": self._faker.image_url(),
            "uri": self._faker.image_url(),
            "user_image_url": self._faker.image_url(),
            "small_image_url": self._faker.image_url(),
            "has_image": bool(self._faker.random_int(0,1)),

            # Fake book
            "title": self._fake_books[ self._faker.random_int(0, len(self._fake_books)-1) ],
            "title_without_series": self._fake_books[ \
                self._faker.random_int(0, len(self._fake_books)-1) ],
            "image_url": self._faker.image_url(),
            "book_url": self._faker.image_url(),
            "num_pages": self._faker.random_int(10, 1000),
            "format": 'Book',
            "edition_information": 'No information',
            "publisher": 'fake publisher',
            "publication_day": self._faker.random_int(1, 28),
            "publication_year": self._faker.random_int(1900, 2100),
            "publication_month": self._faker.random_int(1, 12),
            "ratings_count": self._faker.random_int(0, 1000000),
            "description": 'fake description',
            "published": self._faker.random_int(0,10),

            # Fake author
            "name": self._faker.name(),
            "role": list(['editor', 'illustrator'])[self._faker.random_int(0,1)],
            "profile_url": self._faker.image_url(),
            "average_rating": self._faker.pyfloat(right_digits = 2, min_value =0, max_value = 5),
            "rating_count": self._faker.random_int(0, 1000000),
            "text_review_count": self._faker.random_int(0, 1000000),
            "record_create_timestamp": datetime.now()
        }

    def _parse_review_data(self, review_obj: Any = None):
        """Parse review data from review objects.

        Args:
            review_obj (Any): the review object. Defaults to None.
        """
        if review_obj is None:
            self.logging.error("Review object %s is None." % review_obj)
            return OrderedDict()

        return OrderedDict(
            {
                "review_id": review_obj['review_id'],
                "user_id" : review_obj['user_id'],
                "book_id" : review_obj['book_id'],
                "author_id" : review_obj['author_id'],
                "review_text": review_obj['review_text'],
                "review_rating": review_obj['review_rating'],
                "review_votes": review_obj['review_votes'],
                "spoiler_flag": review_obj['spoiler_flag'],
                "spoiler_state": review_obj['spoiler_state'],
                "review_added_date": review_obj['review_added_date'],
                "review_updated_date": review_obj['review_updated_date'],
                "review_read_count": review_obj['review_read_count'],
                "comments_count": review_obj['comments_count'],
                "review_url": review_obj['review_url'],
                "record_create_timestamp" : review_obj['record_create_timestamp']
            }.items()
        )

    def _parse_user_data(self, review_obj: Any = None):
        """Parse user data from review object.

        Args:
            review_obj (Any, optional): the review objects. Defaults to None.
        """
        if review_obj is None:
            self.logging.error("Review object %s is None." % review_obj)
            return OrderedDict()

        return OrderedDict(
            {
                "user_id": review_obj['user_id'],
                "user_name": review_obj['user_name'],
                "user_display_name": review_obj['user_display_name'],
                "location": review_obj['location'],
                "profile_link": review_obj['profile_link'],
                "uri": review_obj['uri'],
                "user_image_url": review_obj['user_image_url'],
                "small_image_url": review_obj['small_image_url'],
                "has_image": review_obj['has_image'],
                "record_create_timestamp": review_obj['record_create_timestamp']
            }.items()
        )

    def _parse_author_data(self, review_obj: Any = None):
        """Parse author data from review object.

        Args:
            review_obj (Any, optional): the review object. Defaults to None.
        """
        if review_obj is None:
            self.logging.error("Review object %s is None." % review_obj)
            return OrderedDict()

        return OrderedDict(
            {
                "author_id": review_obj['author_id'],
                "name": review_obj['name'],
                "role": review_obj['role'],
                "profile_url": review_obj['profile_url'],
                "average_rating": review_obj['average_rating'],
                "rating_count": review_obj['rating_count'],
                "text_review_count": review_obj['text_review_count'],
                "record_create_timestamp": review_obj['record_create_timestamp']
            }.items()
        )

    def _parse_book_data(self, review_obj: Any = None):
        """Parse book data from review object.

        Args:
            review_obj (Any, optional): the review object. Defaults to None.
        """
        if review_obj is None:
            self.logging.error("Review object %s is None." % review_obj)
            return OrderedDict()

        return OrderedDict(
            {
                "book_id": review_obj['book_id'],
                "title": review_obj['title'],
                "title_without_series": review_obj['title_without_series'],
                "image_url": review_obj['image_url'],
                "book_url": review_obj['book_url'],
                "num_pages": review_obj['num_pages'],
                "format": review_obj['format'],
                "edition_information": review_obj['edition_information'],
                "publisher": review_obj['publisher'],
                "publication_day": review_obj['publication_day'],
                "publication_year": review_obj['publication_year'],
                "publication_month": review_obj['publication_month'],
                "average_rating": review_obj['average_rating'],
                "ratings_count": review_obj['ratings_count'],
                "description": review_obj['description'],
                "authors": review_obj['author_id'],
                "published": review_obj['published'],
                "record_create_timestamp": review_obj['record_create_timestamp']
            }.items()
        )

    def _write_to_disk(self, module_name: str = "", module_data: Any = None):
        """Write the module data to disk

        Args:
            module_name (str, optional): the module name. Defaults to "".
            module_data (Any, optional): the module data which to write them. Defaults to None.
        """
        if not module_name:
            self.logging.warning("The %s is empty. Create uuid module name." % module_name)
            module_name = uuid4().hex

        if module_data is None:
            self.logging.error("The module data is %s" % str(module_data))
            sys.exit(1)

        now = datetime.now().strftime("%Y-%M-%d_%H-%m-%d")

        output_file_path = os.path.join(self._base_directory, f"{module_name}-{str(now)}.csv")
        if os.path.exists(output_file_path):
            self.logging.warning("%s existed. Overwrite it." % output_file_path)

        write_mode, header = ('a', False) \
            if os.path.isfile(output_file_path) else ('w', True)
        self.logging.info("Using the write mode `%s` and `%s` to write module data to disk." \
                          % (write_mode, header))

        if len(module_data) > 0:
            pd \
                .DataFrame(module_data) \
                .to_csv(path_or_buf=output_file_path, sep=",", index=False, mode=write_mode, \
                        header=header, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

            self.logging.info("Write given module data to %s" % output_file_path)

    def _clean_text(self, text: str = ""):
        """Clean text.

        Args:
            text (str, optional): the input text to clean. Defaults to "".
        """
        if text == "":
            self.logging.error("The empty string.")
            sys.exit(1)

        return " ".join((text.replace("\n", "")).split())

    def _clear_modules(self):
        self._user_data_list = []
        self._review_data_list = []
        self._author_data_list = []
        self._book_data_list = []

    def __str__(self) -> str:
        return "GoodreadsFake Instance"


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="A fake data generator for Goodreads reivews."
    )
    required = parser.add_argument_group('required arguments')
    required.add_argument('-n', '--num_records', type=int, metavar='', required=True, \
                          help="Number of records to generate.")
    args = parser.parse_args()
    goodreadsfake = GoodreadsFake()
    goodreadsfake.generate(args.num_records)
