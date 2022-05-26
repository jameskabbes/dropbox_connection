from parent_class import ParentClass
import dropbox

class Connection( ParentClass ):

    def __init__( self, *args, **kwargs ):

        ParentClass.__init__( self )

        self.db = self.get_db_conn( *args, **kwargs )

    def get_db_conn( self, *args, **kwargs ):

        """suggested to get connection with oauth2_access_token"""

        return dropbox.Dropbox( *args, **kwargs )

