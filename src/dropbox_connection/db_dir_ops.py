from __future__ import annotations
import dir_ops as do
import py_starter as ps
from typing import Tuple, List

import dropbox_connection
import dropbox

class DBDir( do.RemoteDir ):

    STATIC_METHOD_SUFFIX = '_dir'
    INSTANCE_METHOD_ATTS = ['path','conn']
    DEFAULT_KWARGS = {}

    def __init__( self, *args, **kwargs ):

        joined_atts = ps.merge_dicts( DBDir.DEFAULT_KWARGS, kwargs )
        self.set_atts( joined_atts )

        do.RemoteDir.__init__( self, self.path )

        self.inherited_kwargs = { 'conn': self.conn }
        self.DIR_CLASS = DBDir
        self.PATH_CLASS = DBPath
        self.DIRS_CLASS = DBDirs
        self.PATHS_CLASS = DBPaths

    @staticmethod
    def create_dir( path: str, conn: dropbox_connection.Connection, **kwargs ):
        conn.db.files_create_folder( path )

    @staticmethod
    def exists_dir( path: str, conn: dropbox_connection.Connection, **kwargs ):
        if path == '': #metadata for root folder isn't supported, just return True
            return 

        conn.db.files_get_metadata( path )
    
    @staticmethod
    def get_size_dir( path: str, conn: dropbox_connection.Connection, **kwargs ):
        
        self = DBDir( path = path, conn = conn )
        Paths_inst = self.list_contents_Paths( block_dirs=True, block_paths=False )

        bytes = 0
        for Path_inst in Paths_inst:
            Path_inst.get_size( **kwargs )
            bytes += Path_inst.size 
        
        return bytes

    @staticmethod
    def remove_dir( path: str, conn: dropbox_connection.Connection, **kwargs ):
        conn.db.files_delete( path )

    @staticmethod
    def copy_dir( path: str, conn: dropbox_connection.Connection, *args, 
                    destination: str = '', **kwargs ):

        remote_Dir = DBDir( path = path, conn = conn )
        remote_Paths = remote_Dir.walk_contents_Paths( block_dirs=True )
        
        valid = True
        for remote_Path in remote_Paths:
            rel_Path = remote_Path.get_rel( remote_Dir )
            destination_path = do.join( destination, rel_Path.path )
            if not remote_Path.copy( *args, destination = destination_path, **kwargs ):
                valid = False
            
        assert valid

    @staticmethod
    def upload_dir( path: str, conn: dropbox_connection.Connection, *args,
                        destination: str = '', **kwargs ):

        local_Dir = do.Dir( destination )
        local_Paths = local_Dir.walk_contents_Paths( block_dirs=True )

        valid = True
        for local_Path in local_Paths:
            rel_Path = local_Path.get_rel( local_Dir )
            remote_Path = DBPath( path = do.join( path, rel_Path.path ), conn = conn )
            if not remote_Path.upload( *args, Destination = local_Path, **kwargs ):
                valid = False

        assert valid

    @staticmethod
    def download_dir( path: str, conn: dropbox_connection.Connection, *args,
                        destination: str = '', **kwargs ):

        remote_Dir = DBDir( path = path, conn = conn )
        remote_Paths = remote_Dir.walk_contents_Paths( block_dirs=True )
        local_Dir = do.Dir( destination )
        
        valid = True
        for remote_Path in remote_Paths:
            rel_Path = remote_Path.get_rel( remote_Dir )
            local_Path = do.Path( local_Dir.join( rel_Path.path ) )
            if not remote_Path.download( *args, Destination = local_Path, **kwargs ):
                valid = False

        assert valid

    @staticmethod
    def list_files_dir( path: str, conn: dropbox_connection.Connection,
                            print_off: bool = False, **kwargs ):

        result = conn.db.files_list_folder( path ).entries

        filenames = []
        for file in result:
            if isinstance( file, dropbox.files.FileMetadata ):
                filenames.append( file.name )

        if print_off:
            ps.print_for_loop( filenames )

        return filenames

    @staticmethod
    def list_subfolders_dir( path: str, conn: dropbox_connection.Connection,
                            print_off: bool = False, **kwargs ):

        result = conn.db.files_list_folder( path ).entries

        subfolders = []
        for folder in result:
            if isinstance( folder, dropbox.files.FolderMetadata ):
                subfolders.append( folder.name )

        if print_off:
            ps.print_for_loop( subfolders )

        return subfolders



class DBPath( DBDir, do.RemotePath ):

    STATIC_METHOD_SUFFIX = '_path'
    INSTANCE_METHOD_ATTS = ['path','conn']

    def __init__( self, *args, **kwargs ):

        DBDir.__init__( self, *args, **kwargs )
        do.RemotePath.__init__( self, self.path )
        self.DIR_CLASS = DBDir
        self.PATH_CLASS = DBPath
        self.DIRS_CLASS = DBDirs
        self.PATHS_CLASS = DBPaths

    @staticmethod
    def exists_path( path: str, conn: dropbox_connection.Connection, **kwargs ):
        if path == '': #metadata for root folder isn't supported, just return True
            return 

        conn.db.files_get_metadata( path )

    @staticmethod
    def upload_path( path: str, conn: dropbox_connection.Connection, *args,
                        destination: str = '', **kwargs ):

        conn.db.files_upload( ps.read_text_file( destination, mode = 'rb' ), path )

    @staticmethod
    def download_path( path: str, conn: dropbox_connection.Connection, *args,
                        destination: str = '', **kwargs ):

        conn.db.files_download_to_file( destination, path )

    @staticmethod
    def remove_path( path: str, conn: dropbox_connection.Connection, **kwargs ):
        conn.db.files_delete( path )

    @staticmethod
    def get_size_path( path: str, conn: dropbox_connection.Connection, **kwargs ):

        result = conn.db.files_get_metadata( path )
        return result.size

    @staticmethod
    def write_path( path: str, conn: dropbox_connection.Connection, mode = 'w', **kwargs ):

        self = DBPath( path = path, conn = conn )
        temp_Path = do.Path( 'TEMP' )

        if not temp_Path.write( mode = mode, **kwargs ):
            assert False
        
        if not self.upload( Destination = temp_Path, **kwargs ):
            assert False

        if not temp_Path.remove( **kwargs ):
            assert False

    @staticmethod
    def create_path( path: str, conn: dropbox_connection.Connection, *args, string: str = '', mode = 'w', **kwargs ):

        self = DBPath( path = path, conn = conn )
        if not self.write( string = string, mode = mode, **kwargs ):
            assert False

    @staticmethod
    def read_path( path: str, conn: dropbox_connection.Connection, *args, **kwargs ):

        temp_Path = do.Path( 'TEMP' )

        self = DBPath( path = path, conn = conn )
        self.download( Destination = temp_Path, **kwargs )
            
        contents = temp_Path.read( **kwargs )
        temp_Path.remove( override = True, **kwargs )
                
        return contents

    @staticmethod
    def copy_path( path: str, conn: dropbox_connection.Connection, *args,
                    destination: str = '', **kwargs ):

        conn.db.files_copy( path, destination )

    @staticmethod
    def rename_path( path: str, conn: dropbox_connection.Connection, *args,
                    destination: str = '', destination_bucket = None, **kwargs ):

        conn.db.files_move( path, destination )


class DBDirs( do.RemoteDirs ):

    def __init__( self, *args, **kwargs ):

        do.RemoteDirs.__init__( self, *args, **kwargs )
        self.DIR_CLASS = DBDir
        self.PATH_CLASS = DBPath
        self.DIRS_CLASS = DBDirs
        self.PATHS_CLASS = DBPaths

class DBPaths( DBDirs, do.RemotePaths ):

    def __init__( self, *args, **kwargs ):

        DBDirs.__init__( self )
        do.RemotePaths.__init__( self, *args, **kwargs )
        self.DIR_CLASS = DBDir
        self.PATH_CLASS = DBPath
        self.DIRS_CLASS = DBDirs
        self.PATHS_CLASS = DBPaths




