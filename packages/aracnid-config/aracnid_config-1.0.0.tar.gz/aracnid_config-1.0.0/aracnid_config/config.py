"""Class module for configuration functions.
"""
import os

from aracnid_logger import Logger

from i_mongodb import MongoDBInterface

# initialize logging
logger = Logger(__name__).get_logger()


class Config:
    """The Config class is the configuration data store.

    Environment Variables:
        CONFIG_COLLECTION: Name of the configuration collection in MongoDB.

    Properties:
        auto_update: Process flag to automatically update properties to MongoDB.
        name: The name of the configuration set.
        props: The entire configuration set.
    """

    reserved = [
        'auto_update',
        'mdb',
        'db_name',
        'mongo_client',
    ]

    def __init__(self, name=None, mdb=None):
        # read environment variables
        self._collection_name = os.environ.get('CONFIG_COLLECTION')

        # initialize variables
        self._props = {}
        self.auto_update = True
        mongodb = MongoDBInterface()

        # initialize mongodb
        self.mdb = mdb
        if not mdb:
            self.mdb = mongodb.get_mdb()
        self._collection = mongodb.read_collection(self._collection_name)

        # load the configuration set
        self.load_properties(name)

    @property
    def name(self):
        """Get 'name'
        """
        return self._name

    @name.setter
    def name(self, val):
        """Set 'name'
        """
        self._name = val

    @property
    def props(self):
        """Get 'props'
        """
        return self._props

    def __getattr__(self, prop_name):
        """Reads the specified configuration property.

        Args:
            prop_name: The property name.

        Returns:
            The value of the specified property.
        """
        if self._props:
            if prop_name in self._props:
                return self._props[prop_name]

        return None

    def __getitem__(self, prop_name):
        """Reads a specific configuration property, via subscripting.

        Args:
            prop_name: The property name.

        Returns:
            The value of the specified property.
        """
        return self.__getattr__(prop_name)

    def __setattr__(self, prop_name, val):
        """Sets a configuration property.

        Args:
            prop_name: The property name.
            val: The value of the specified property.
        """
        # skip object attributes
        if prop_name in Config.reserved or prop_name.startswith('_'):
            super().__setattr__(prop_name, val)

        else:
            self._props[prop_name] = val
            if self.auto_update:
                self.update()

    def __setitem__(self, prop_name, val):
        """Sets a configuration property, via subscripting.

        Args:
            prop_name: The property name.
            val: The value of the specified property.
        """
        self.__setattr__(prop_name, val)

    def __delattr__(self, prop_name):
        """Deletes a configuration property

        Args:
            prop_name: The property name.
        """
        self.props.pop(prop_name, None)

    def load_properties(self, name):
        """Read the specified set of properties.

        Args:
            name: The name of the configuration set.
        """
        # reset props
        self._props = {}

        # set the configuration set name
        self._name = name

        # read the named configuration set
        doc = self._collection.find_one({'_id': name})
        if doc:
            self._props = doc['props']

    def update(self):
        """Updates the configuration properties.
        """
        self._collection.find_one_and_replace(
            {'_id': self._name},
            {'_id': self._name, 'props': self._props},
            upsert=True)

    def delete(self):
        """Deletes the entire configuration set.

        Does not delete the name of the configuration set. This object can
        still be used to rebuild the configuration set after a deletion.
        """
        if self._name:
            self._collection.delete_one({'_id': self._name})
            # self._name = None
            self._props = {}


if __name__ == '__main__':
    pass
