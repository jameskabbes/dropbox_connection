from parent_class import ParentClass
import dropbox
import kabbes_account_manager
import requests
import urllib
import py_starter as ps

class Connection( ParentClass ):

    def __init__( self, *args, **kwargs ):

        ParentClass.__init__( self )

        if len(self.cfg['use_stored_credentials'])>0:
            kwargs = self.load_credentials( kwargs )

        self.db = self.get_db_conn( *args, **kwargs )

    @staticmethod
    def get_db_conn( *args, **kwargs ):
        """suggested to get connection with oauth2_access_token"""
        return dropbox.Dropbox( *args, **kwargs )

    def load_credentials( self, user_given_creds ):

        if self.cfg['accounts_manager.client.inst'] == None:
            args, kwargs = self.cfg['accounts_manager.client'].get_args(), self.cfg['accounts_manager.client'].get_kwargs()
            self.cfg.get_node('accounts_manager.client.inst').set_value( kabbes_account_manager.Client( *args, **kwargs ) )

        DropboxAccount = self.cfg['accounts_manager.client.inst'].Accounts.Accounts[ self.cfg['accounts_manager.id'] ]

        if 'refresh_token' in self.cfg['use_stored_credentials']:
            stored_credentials = {}
            for key in self.cfg['use_stored_credentials']:
                account_key = self.cfg['accounts_manager.' + key]
                stored_credentials[key] = DropboxAccount.Entries.get_Entry( account_key ).Value.val

            data={ 
                'refresh_token': stored_credentials['refresh_token'], 
                'grant_type':'refresh_token',
                'client_id': stored_credentials['app_key'],
                'client_secret': stored_credentials['app_secret']
            }

            res = requests.post( 'https://api.dropbox.com/oauth2/token', data=urllib.parse.urlencode(data) )
            oauth2_access_token = ps.json_to_dict( res.content.decode() )['access_token']

        user_given_creds['oauth2_access_token'] = oauth2_access_token
        return user_given_creds



