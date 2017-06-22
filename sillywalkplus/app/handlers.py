import webapp2
from google.appengine.api.datastore_errors import BadRequestError

import models
import commands

class GetHandler(webapp2.RequestHandler):

    def dispatch(self):
        """
        Returns the item at the given name
        :return:
        """
        name = self.request.get('name')
        if name:
            try:
                status = 200
                data = models.Item.get_by_id(name).value
            except AttributeError: # id doesn't exist
                status = 404
                data = "None"
        else:
            status = 404
            data = "None"
        self.response.status = status
        self.response.write(data)


class SetHandler(webapp2.RequestHandler):

    def dispatch(self):
        """
        Sets the item at the given name
        This behaves kind of like PUT, so it is supposed to be idempotent. Except for validation errors, this thing should always return 201.
        No spaces allowed
        :return:
        """
        name = self.request.get('name')
        value = self.request.get('value')
        request_is_valid = name and value and ' ' not in name and ' ' not in value
        if request_is_valid:
            commands.SetItemCommand.create(item_name=name, item_value=value).execute()
            self.response.status = 201
        else:
            self.response.status = 400
            self.response.write('Bad request - entity name and value are required and must not contain spaces')


class UnsetHandler(webapp2.RequestHandler):

    def dispatch(self):
        """
        Deletes the entity with the given name, doesn't care whether it actually exists or not.
        Since DELETE is idempotent, we don't want to actually validate whether the entity exists.
        (except for maybe internal usage, but it won't be reflected by the API)
        :return:
        """
        name = self.request.get('name')
        if name:
            commands.UnsetCommand.create(item_name=name).execute()
        else:
            self.response.status = 400
            self.response.write('Bad request - invalid entity name')


class NumEqualToHandler(webapp2.RequestHandler):

    def dispatch(self):
        """
        Returns the number of appearances of a certain value
        :return:
        """
        value = self.request.get('value')
        try:
            count = models.ValueCount.get_by_id(value).count
        except (AttributeError, BadRequestError):  # This value has never been set before, or we just received junk
            count = 0
        self.response.write(count)


class UndoHandler(webapp2.RequestHandler):

    def dispatch(self):
        """
        Undoes the last set/unset
        :return:
        """
        try:
            commands.undo_last_command()
        except commands.NoCommandsError:
            self.response.write("NO COMMANDS")


class EndHandler(webapp2.RequestHandler):
    def dispatch(self):
        """
        Flushes the DB
        :return:
        """
        commands.EndCommand().execute()