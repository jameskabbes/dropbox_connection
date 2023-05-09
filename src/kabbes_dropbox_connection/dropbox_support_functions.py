import dropbox
import py_starter as ps
import dir_ops as do
from dir_ops import Dir
from dir_ops import Path
import os


def create_sharing_folder( db_dir ):

    '''create a sharing folder at the given dropbox dir'''
    return dropbox.sharing_share_folder( db_dir )

def get_access_level( access_level_key = None ):

    if access_level_key == None:
        access_level_key = user_choose_access_level()

    return dropbox.sharing.AccessLevel( access_level_key )

def user_choose_access_level():

    options = ['editor','viewer','owner','other']

    ps.print_for_loop( options )
    ind = ps.get_int_input( 1, len(options), prompt = 'Choose the access level' )

    return options[ind-1]

def get_shared_folder_id( sharing_folder ):

    '''get the shared folder id'''
    return sharing_folder.get_complete().shared_folder_id

def get_member_selector( email_address ):

    return dropbox.sharing.MemberSelector.email( email_address )

def get_add_member( member_selector, AccessLevel ):

    add_member = dropbox.sharing.AddMember( member_selector, access_level = AccessLevel )
    return add_member

def sharing_add_folder_member( shared_folder_id, add_member, custom_message ):

    dropbox.sharing_add_folder_member( shared_folder_id, [add_member], quiet = False, custom_message = custom_message )

def get_url_from_link_object( Link ):

    return Link.url

def sharing_create_shared_link( db_path, short_url = False, return_url = True ):

    ''' create a shared link of a dropbox path. returns a path link
    path is a path to a dropbox folder. ex: Pictures/test_folder
    '''

    Link = dropbox.sharing_create_shared_link( db_path, short_url = short_url )

    if return_url:
        return get_url_from_link_object( Link )
    else:
        return Link
