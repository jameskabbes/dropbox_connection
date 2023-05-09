import kabbes_dropbox_connection
import kabbes_client

class Client( kabbes_dropbox_connection.Connection ):

    _BASE_DICT = {}

    def __init__( self, *args, dict={}, root_dict={}, **kwargs ):

        d = {}
        d.update( Client._BASE_DICT )
        d.update( dict )

        root_inst = kabbes_client.Root( root_dict=root_dict )
        self.Package = kabbes_client.Package( kabbes_dropbox_connection._Dir, dict=d, root=root_inst )
        self.cfg = self.Package.cfg

        kabbes_dropbox_connection.Connection.__init__( self, *args, **kwargs )
