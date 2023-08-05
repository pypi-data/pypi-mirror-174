# coding: utf-8
#
# This code is part of pyrekordbox.
#
# Copyright (c) 2022, Dylan Jones

import os
import re
import base64
import blowfish
import logging
from typing import Optional
from sqlalchemy import create_engine, or_, event
from sqlalchemy.orm import sessionmaker, Session
from ..config import get_config
from ..utils import read_rekordbox6_asar
from ..anlz import get_anlz_paths, read_anlz_files
from .tables import DjmdContent
from . import tables

try:
    from pysqlcipher3 import dbapi2 as sqlite3  # noqa
except ImportError:
    import sqlite3

logger = logging.getLogger(__name__)

rb6_config = get_config("rekordbox6")


def _get_masterdb_key():  # pragma: no cover
    # See https://www.reddit.com/r/Rekordbox/comments/qou6nm/key_to_open_masterdb_file/

    # Read password key from app.asar file
    asar_data = read_rekordbox6_asar(rb6_config["install_dir"])
    match = re.search('pass: ".(.*?)"', asar_data).group(0)
    password = match.replace("pass: ", "").strip('"')

    # Decode database key data
    encoded_key_data = rb6_config["dp"]  # from 'options.json'
    decoded_key_data = base64.standard_b64decode(encoded_key_data)

    # Decrypt database key
    cipher = blowfish.Cipher(password.encode())
    decrypted_bytes = b"".join(cipher.decrypt_ecb(decoded_key_data))
    database_key = decrypted_bytes.decode()

    return database_key


def open_rekordbox_database(path="", unlock=True, sql_driver=None):
    """Opens a connection to the Rekordbox v6 master.db SQLite3 database.

    Parameters
    ----------
    path : str, optional
        The path of the database file. Uses the main Rekordbox v6 master.db database
        by default.
    unlock : bool, optional
        Flag if the database is encrypted and needs to be unlocked.
    sql_driver : Callable, optional
        The SQLite driver to used for opening the database. The standard ``sqlite3``
        package is used as default driver.

    Returns
    -------
    con : sql_driver.Connection
        The opened Rekordbox v6 database connection.

    Examples
    --------
    Open the Rekordbox v6 master.db database:

    >>> db = open_rekordbox_database()

    Open a copy of the database:

    >>> db = open_rekordbox_database("path/to/master_copy.db")

    Open a decrypted copy of the database:

    >>> db = open_rekordbox_database("path/to/master_unlocked.db", unlock=False)

    To use the ``pysqlcipher3`` package as SQLite driver, either import it as

    >>> from pysqlcipher3 import dbapi2 as sqlite3  # noqa
    >>> db = open_rekordbox_database("path/to/master_copy.db")

    or supply the package as driver:

    >>> from pysqlcipher3 import dbapi2
    >>> db = open_rekordbox_database("path/to/master_copy.db", sql_driver=dbapi2)
    """
    if not path:
        path = rb6_config["db_path"]

    if not os.path.exists(path):
        raise FileNotFoundError(f"File '{path}' does not exist!")
    logger.info("Opening %s", path)

    # Open database
    if sql_driver is None:
        # Use default sqlite3 package
        # This requires that the 'sqlite3.dll' was replaced by
        # the 'sqlcipher.dll' (renamed to 'sqlite3.dll')
        sql_driver = sqlite3
    con = sql_driver.connect(path)

    if unlock:
        # Read and decode master.db key
        key = _get_masterdb_key()
        logger.info("Key: %s", key)
        # Unlock database
        con.execute(f"PRAGMA key='{key}'")

    # Check connection
    try:
        con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    except sqlite3.DatabaseError as e:
        msg = f"Opening database failed: '{e}'. Check if the database key is correct!"
        raise sqlite3.DatabaseError(msg)
    else:
        logger.info("Database unlocked!")

    return con


def create_rekordbox_engine(path="", unlock=True, sql_driver=None, echo=None):
    """Opens the Rekordbox v6 master.db SQLite3 database for the use with SQLAlchemy.

    Parameters
    ----------
    path : str, optional
        The path of the database file. Uses the main Rekordbox v6 master.db database
        by default.
    unlock : bool, optional
        Flag if the database is encrypted and needs to be unlocked.
    sql_driver : Callable, optional
        The SQLite driver to used for opening the database. The standard ``sqlite3``
        package is used as default driver.
    echo : bool, optional
        Prints all executed SQL statements to the console if true.

    Returns
    -------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine instance for the Rekordbox v6 database.
    """
    if not path:
        path = rb6_config["db_path"]

    if not os.path.exists(path):
        raise FileNotFoundError(f"File '{path}' does not exist!")
    logger.info("Opening %s", path)

    # Open database
    if unlock:
        key = _get_masterdb_key()
        logger.info("Key: %s", key)
        if sql_driver is None:
            # Use default sqlite3 package
            # This requires that the 'sqlite3.dll' was replaced by
            # the 'sqlcipher.dll' (renamed to 'sqlite3.dll')
            sql_driver = sqlite3
        url = f"sqlite+pysqlcipher://:{key}@/{path}?"
        engine = create_engine(url, module=sql_driver, echo=echo)
    else:
        engine = create_engine(f"sqlite:///{path}", echo=echo)

    return engine


def _parse_query_result(query, kwargs):
    if "ID" in kwargs:
        query = query.one()
    return query


class UpdateTracker:
    def __init__(self, session=None):
        self.session: Optional[Session] = None
        self._count = 0
        self._sequence = list()
        self.history = list()
        if session:
            self.connect(session)

    def connect(self, session):
        self.session = session
        event.listen(self.session, "before_flush", self.before_flush)
        event.listen(self.session, "after_commit", self.clear)
        event.listen(self.session, "after_rollback", self.clear)

    def disconnect(self):
        event.remove(self.session, "before_flush", self.before_flush)
        event.remove(self.session, "after_commit", self.clear)
        event.remove(self.session, "after_rollback", self.clear)
        self.session = None

    def _get_unflushed(self):
        seq = list()
        i = 0
        for x in self.session.new:
            i += 1
            seq.append((self._count + i, x, "create"))
        for x in self.session.dirty:
            i += 1
            seq.append((self._count + i, x, "update"))
        for x in self.session.deleted:
            i += 1
            seq.append((self._count + i, x, "delete"))
        return i, seq

    def before_flush(self, *_):
        count, seq = self._get_unflushed()
        self._count += count
        self._sequence.extend(seq)

    def clear(self, *_):
        # Reset number of rows changed on commit/rollback
        self.history.extend(self._sequence)
        self._count = 0
        self._sequence.clear()
        tables.reset_update_counts()

    def get_updates(self):
        seq = self._sequence.copy()
        _, new = self._get_unflushed()
        seq.extend(new)
        seq.sort(key=lambda _x: int(_x[0]))
        # seq.reverse()
        return seq

    def get_update_dict(self):
        d = {"created": list(), "updated": list(), "deleted": list()}
        for i, instance, op in self.get_updates():
            d[op].append((i, instance))
        return d


class Rekordbox6Database:
    """Rekordbox v6 master.db database handler.

    Parameters
    ----------
    path : str, optional
        The path of the Rekordbox v6 database file. By default, pyrekordbox
        automatically finds the Rekordbox v6 master.db database file.
        This parameter is only required for opening other databases or if the
        configuration fails.
    unlock: bool, optional
        Flag if the database needs to be decrypted. Set to False if you are opening
        an unencrypted test database.

    Attributes
    ----------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine instance for the Rekordbox v6 database.
    session : sqlalchemy.orm.Session
        The SQLAlchemy session instance bound to the engine.

    See Also
    --------
    pyrekordbox.db6.tables: Rekordbox v6 database table definitions
    create_rekordbox_engine: Creates the SQLAlchemy engine for the Rekordbox v6 database

    Examples
    --------
    Pyrekordbox automatically finds the Rekordbox v6 master.db database file and
    opens it when initializing the object:

    >>> db = Rekordbox6Database()

    Use the included getters for querying the database:

    >>> db.get_content()[0]
    <DjmdContent(40110712   Title=NOISE)>
    """

    def __init__(self, path="", unlock=True):
        self.engine = create_rekordbox_engine(path, unlock=unlock)
        self._Session = sessionmaker(bind=self.engine)
        self.session: Optional[Session] = None

        self._events = dict()
        self.tracker = UpdateTracker()

        self._db_dir = os.path.normpath(rb6_config["db_dir"])
        self._anlz_root = os.path.join(self._db_dir, "share")

        self.open()

    def open(self):
        """Open the database by instantiating a new session using the SQLAchemy engine.

        A new session instance is only created if the session was closed previously.

        Examples
        --------
        >>> db = Rekordbox6Database()
        >>> db.close()
        >>> db.open()
        """
        if self.session is None:
            self.session = self._Session()
            self.tracker.connect(self.session)

    def close(self):
        """Close the currently active session."""
        for key in self._events:
            self.unregister_event(key)
        self.tracker.disconnect()
        self.session.close()
        self.session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def register_event(self, identifier, fn):
        """Registers a session event callback.

        Parameters
        ----------
        identifier : str
            The identifier of the event, for example 'before_flush', 'after_commit', ...
            See the SQLAlchemy documentation for a list of valid event identifiers.
        fn : callable
            The event callback method.
        """
        event.listen(self.session, identifier, fn)
        self._events[identifier] = fn

    def unregister_event(self, identifier):
        """Removes an existing session event callback.

        Parameters
        ----------
        identifier : str
            The identifier of the event
        """
        fn = self._events[identifier]
        event.remove(self.session, identifier, fn)

    # -- Table queries -----------------------------------------------------------------

    def query(self, *entities, **kwargs):
        """Creates a new SQL query for the given entities.

        Parameters
        ----------
        *entities : Base
            The table objects for which the query is created.
        **kwargs
            Arbitrary keyword arguments used for creating the query.

        Returns
        -------
        query : sqlalchemy.orm.query.Query
            The SQLAlchemy ``Query`` object.

        Examples
        --------
        Query the ``DjmdContent`` table

        >>> db = Rekordbox6Database()
        >>> query = db.query(DjmdContent)

        Query the `Title` attribute of the ``DjmdContent`` table

        >>> db = Rekordbox6Database()
        >>> query = db.query(DjmdContent.Title)
        """
        return self.session.query(*entities, **kwargs)

    def get_active_censor(self, **kwargs):
        """Creates a filtered query for the ``DjmdActiveCensor`` table."""
        query = self.query(tables.DjmdActiveCensor).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_album(self, **kwargs):
        """Creates a filtered query for the ``DjmdAlbum`` table."""
        query = self.query(tables.DjmdAlbum).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_artist(self, **kwargs):
        """Creates a filtered query for the ``DjmdArtist`` table."""
        query = self.query(tables.DjmdArtist).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_category(self, **kwargs):
        """Creates a filtered query for the ``DjmdCategory`` table."""
        query = self.query(tables.DjmdCategory).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_color(self, **kwargs):
        """Creates a filtered query for the ``DjmdColor`` table."""
        query = self.query(tables.DjmdColor).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_content(self, **kwargs):
        """Creates a filtered query for the ``DjmdContent`` table."""
        query = self.query(tables.DjmdContent).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    # noinspection PyUnresolvedReferences
    def search_content(self, text):
        """Searches the contents of the ``DjmdContent`` table.

        The search is case-insensitive and includes the following collumns of the
        ``DjmdContent`` table:

        - `Album`
        - `Artist`
        - `Commnt`
        - `Composer`
        - `Genre`
        - `Key`
        - `OrgArtist`
        - `Remixer`

        Parameters
        ----------
        text : str
            The search text.

        Returns
        -------
        results : list[DjmdContent]
            The resulting content elements.
        """
        # Search standard columns
        query = self.query(tables.DjmdContent).filter(
            or_(
                DjmdContent.Title.contains(text),
                DjmdContent.Commnt.contains(text),
                DjmdContent.SearchStr.contains(text),
            )
        )
        results = set(query.all())

        # Search artist (Artist, OrgArtist, Composer and Remixer)
        artist_attrs = ["Artist", "OrgArtist", "Composer", "Remixer"]
        for attr in artist_attrs:
            query = self.query(DjmdContent).join(getattr(DjmdContent, attr))
            results.update(query.filter(tables.DjmdArtist.Name.contains(text)).all())

        # Search album
        query = self.query(DjmdContent).join(DjmdContent.Album)
        results.update(query.filter(tables.DjmdAlbum.Name.contains(text)).all())

        # Search Genre
        query = self.query(DjmdContent).join(DjmdContent.Genre)
        results.update(query.filter(tables.DjmdGenre.Name.contains(text)).all())

        # Search Key
        query = self.query(DjmdContent).join(DjmdContent.Key)
        results.update(query.filter(tables.DjmdKey.ScaleName.contains(text)).all())

        results = list(results)
        results.sort(key=lambda x: x.ID)
        return results

    def get_cue(self, **kwargs):
        """Creates a filtered query for the ``DjmdCue`` table."""
        query = self.query(tables.DjmdCue).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_device(self, **kwargs):
        """Creates a filtered query for the ``DjmdDevice`` table."""
        query = self.query(tables.DjmdDevice).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_genre(self, **kwargs):
        """Creates a filtered query for the ``DjmdGenre`` table."""
        query = self.query(tables.DjmdGenre).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_history(self, **kwargs):
        """Creates a filtered query for the ``DjmdHistory`` table."""
        query = self.query(tables.DjmdHistory).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_history_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongHistory`` table."""
        query = self.query(tables.DjmdSongHistory).filter_by(HistoryID=id_)
        return query

    def get_hot_cue_banklist(self, **kwargs):
        """Creates a filtered query for the ``DjmdHotCueBanklist`` table."""
        query = self.query(tables.DjmdHotCueBanklist).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_hot_cue_banklist_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongHotCueBanklist`` table."""
        query = self.query(tables.DjmdSongHotCueBanklist).filter_by(
            HotCueBanklistID=id_
        )
        return query

    def get_key(self, **kwargs):
        """Creates a filtered query for the ``DjmdKey`` table."""
        query = self.query(tables.DjmdKey).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_label(self, **kwargs):
        """Creates a filtered query for the ``DjmdLabel`` table."""
        query = self.query(tables.DjmdLabel).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_menu_items(self, **kwargs):
        """Creates a filtered query for the ``DjmdMenuItems`` table."""
        query = self.query(tables.DjmdMenuItems).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_mixer_param(self, **kwargs):
        """Creates a filtered query for the ``DjmdMixerParam`` table."""
        query = self.query(tables.DjmdMixerParam).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_my_tag(self, **kwargs):
        """Creates a filtered query for the ``DjmdMyTag`` table."""
        query = self.query(tables.DjmdMyTag).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_my_tag_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongMyTag`` table."""
        query = self.query(tables.DjmdSongMyTag).filter_by(MyTagID=id_)
        return query

    def get_playlist(self, **kwargs):
        """Creates a filtered query for the ``DjmdPlaylist`` table."""
        query = self.query(tables.DjmdPlaylist).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_playlist_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongPlaylist`` table."""
        query = self.query(tables.DjmdSongPlaylist).filter_by(PlaylistID=id_)
        return query

    def get_property(self, **kwargs):
        """Creates a filtered query for the ``DjmdProperty`` table."""
        query = self.query(tables.DjmdProperty).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_related_tracks(self, **kwargs):
        """Creates a filtered query for the ``DjmdRelatedTracks`` table."""
        query = self.query(tables.DjmdRelatedTracks).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_related_tracks_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongRelatedTracks`` table."""
        query = self.query(tables.DjmdSongRelatedTracks).filter_by(RelatedTracksID=id_)
        return query

    def get_sampler(self, **kwargs):
        """Creates a filtered query for the ``DjmdSampler`` table."""
        query = self.query(tables.DjmdSampler).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_sampler_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongSampler`` table."""
        query = self.query(tables.DjmdSongSampler).filter_by(SamplerID=id_)
        return query

    def get_tag_list_songs(self, id_):
        """Creates a filtered query for the ``DjmdSongTagList`` table."""
        query = self.query(tables.DjmdSongTagList).filter_by(ID=id_)
        return query

    def get_sort(self, **kwargs):
        """Creates a filtered query for the ``DjmdSort`` table."""
        query = self.query(tables.DjmdSort).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_agent_registry(self, **kwargs):
        """Creates a filtered query for the ``AgentRegistry`` table."""
        query = self.query(tables.AgentRegistry).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_cloud_agent_registry(self, **kwargs):
        """Creates a filtered query for the ``CloudAgentRegistry`` table."""
        query = self.query(tables.CloudAgentRegistry).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_content_active_censor(self, **kwargs):
        """Creates a filtered query for the ``ContentActiveCensor`` table."""
        query = self.query(tables.ContentActiveCensor).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_content_cue(self, **kwargs):
        """Creates a filtered query for the ``ContentCue`` table."""
        query = self.query(tables.ContentCue).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_content_file(self, **kwargs):
        """Creates a filtered query for the ``ContentFile`` table."""
        query = self.query(tables.ContentFile).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_hot_cue_banklist_cue(self, **kwargs):
        """Creates a filtered query for the ``HotCueBanklistCue`` table."""
        query = self.query(tables.HotCueBanklistCue).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_image_file(self, **kwargs):
        """Creates a filtered query for the ``ImageFile`` table."""
        query = self.query(tables.ImageFile).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_setting_file(self, **kwargs):
        """Creates a filtered query for the ``SettingFile`` table."""
        query = self.query(tables.SettingFile).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    def get_uuid_map(self, **kwargs):
        """Creates a filtered query for the ``UuidIDMap`` table."""
        query = self.query(tables.UuidIDMap).filter_by(**kwargs)
        return _parse_query_result(query, kwargs)

    # -- Database updates --------------------------------------------------------------

    def delete(self, instance):
        """Delete an element from the Rekordbox database.

        Parameters
        ----------
        instance : tables.Base
            The table entry to delte.
        """
        self.session.delete(instance)

    def get_local_usn(self):
        """Returns the local sequence number (update count) of Rekordbox.

        Any changes made to the `Djmd...` tables increments the local update count of
        Rekordbox. The ``usn`` entry of the changed row is set to the corresponding
        update count.

        Returns
        -------
        usn : int
            The value of the local update count.
        """
        reg = self.get_agent_registry(registry_id="localUpdateCount").one()
        return reg.int_1

    def set_local_usn(self, usn):
        """Sets the local sequence number (update count) of Rekordbox.

        Parameters
        ----------
        usn : int or str
            The new update sequence number.
        """
        item = self.get_agent_registry(registry_id="localUpdateCount").one()
        item.int_1 = usn

    def increment_local_usn(self, num=1):
        """Increments the local update sequence number (update count) of Rekordbox.

        Parameters
        ----------
        num : int, optional
            The number of times to increment the update counter. By default, the counter
            is incremented by 1.

        Returns
        -------
        usn : int
            The value of the incremented local update count.

        Examples
        --------
        >>> db = Rekordbox6Database()
        >>> db.get_local_usn()
        70500

        >>> db.increment_local_usn()
        70501

        >>> db.get_local_usn()
        70501
        """
        if not isinstance(num, int) or num < 1:
            raise ValueError("The USN can only be increment by a positive integer!")

        new = self.get_local_usn() + num
        self.set_local_usn(new)
        return new

    def autoincrement_usn(self, set_row_usn=True):
        """Auto-increments the local USN for all uncommited changes.

        Parameters
        ----------
        set_row_usn : bool, optional
            If True, set the ``rb_local_usn`` value of updated or added rows according
            to the uncommited update sequence.

        Examples
        --------
        >>> db = Rekordbox6Database()
        >>> db.get_local_usn()
        70500

        >>> content = db.get_content().first()
        >>> playlist = db.get_playlist().first()
        >>> content.Title = "New Title"
        >>> playlist.Name = "New Name"
        >>> db.autoincrement_usn(set_row_usn=True)
        >>> db.get_local_usn()
        70502

        >>> content.rb_local_usn
        70501

        >>> playlist.rb_local_usn
        70502
        """
        for i, instance, op in self.tracker.get_updates():
            if op == "create":
                last_usn = self.increment_local_usn()
                if set_row_usn and hasattr(instance, "rb_local_usn"):
                    instance.rb_local_usn = last_usn
            elif op == "update":
                num = tables.get_update_count(instance)
                last_usn = self.increment_local_usn(num)
                if set_row_usn and hasattr(instance, "rb_local_usn"):
                    instance.rb_local_usn = last_usn
            elif op == "delete":
                self.increment_local_usn()

    def commit(self, autoinc=True):
        """Commit the changes made to the database.

        Parameters
        ----------
        autoinc : bool, optional
            If True, auto-increment the local and row USN's before commiting the
            changes made to the database.

        See Also
        --------
        autoincrement_usn: Auto-increments the local Rekordbox USN's.
        """
        if autoinc:
            self.autoincrement_usn()

        self.session.commit()
        self.tracker.clear()

    def rollback(self):
        """Rolls back the uncommited changes to the database."""
        self.session.rollback()
        self.tracker.clear()

    # ----------------------------------------------------------------------------------

    def get_mysetting_paths(self):
        """Returns the file paths of the local Rekordbox MySetting files.

        Returns
        -------
        paths : list[str]
            the file paths of the local MySetting files.
        """
        paths = list()
        for item in self.get_setting_file():
            paths.append(os.path.join(self._db_dir, item.Path.lstrip("/\\")))
        return paths

    def get_anlz_dir(self, content):
        """Returns the directory path containing the ANLZ analysis files of a track.

        Parameters
        ----------
        content : DjmdContent or int or str
            The content corresponding to a track in the Rekordbox v6 database.
            If an integer is passed the database is queried for the ``DjmdContent``
            entry.

        Returns
        -------
        anlz_dir : str
            The path of the directory containing the analysis files for the content.
        """
        if isinstance(content, (int, str)):
            content = self.get_content(ID=content)

        dat_path = os.path.normpath(content.AnalysisDataPath).strip("\\/")
        path = os.path.join(self._anlz_root, os.path.dirname(dat_path))
        assert os.path.exists(path)
        return path

    def get_anlz_paths(self, content):
        """Returns all existing ANLZ analysis file paths of a track.

        Parameters
        ----------
        content : DjmdContent or int or str
            The content corresponding to a track in the Rekordbox v6 database.
            If an integer is passed the database is queried for the ``DjmdContent``
            entry.

        Returns
        -------
        anlz_paths : dict[str, str]
            The analysis file paths for the content as dictionary. The keys of the
            dictionary are the file types ("DAT", "EXT" or "EX2").
        """
        root = self.get_anlz_dir(content)
        return get_anlz_paths(root)

    def read_anlz_files(self, content):
        """Reads all existing ANLZ analysis files of a track.

        Parameters
        ----------
        content : DjmdContent or int or str
            The content corresponding to a track in the Rekordbox v6 database.
            If an integer is passed the database is queried for the ``DjmdContent``
            entry.

        Returns
        -------
        anlz_files : dict[str, AnlzFile]
            The analysis files for the content as dictionary. The keys of the
            dictionary are the file paths.
        """
        root = self.get_anlz_dir(content)
        return read_anlz_files(root)

    def update_content_path(self, content, path, save=True, check_path=True):
        """Update the file path of a track in the Rekordbox v6 database.

        This changes the `FolderPath` entry in the ``DjmdContent`` table and the
        path tag (PPTH) of the corresponding ANLZ analysis files.

        Parameters
        ----------
        content : DjmdContent or int or str
            The ``DjmdContent`` element to change. If an integer is passed the database
            is queried for the content.
        path : str
            The new file path of the database entry.
        save : bool, optional
            If True, the changes made are written to disc.
        check_path : bool, optional
            If True, raise an assertion error if the given file path does not exist.

        Examples
        --------
        If, for example, the file `NOISE.wav` was moved up a few directories
        (from `.../Sampler/OSC_SAMPLER/PRESET ONESHOT/` to `.../Sampler/`) the file
        could no longer be opened in Rekordbox, since the database still contains the
        old file path:

        >>> db = Rekordbox6Database()
        >>> cont = db.get_content()[0]
        >>> cont.FolderPath
        C:/Music/PioneerDJ/Sampler/OSC_SAMPLER/PRESET ONESHOT/NOISE.wav

        Updating the path changes the database entry

        >>> new_path = "C:/Music/PioneerDJ/Sampler/PRESET ONESHOT/NOISE.wav"
        >>> db.update_content_path(cont, new_path)
        >>> cont.FolderPath
        C:/Music/PioneerDJ/Sampler/PRESET ONESHOT/NOISE.wav

        and updates the file path in the corresponding ANLZ analysis files:

        >>> files = self.read_anlz_files(cont.ID)
        >>> file = list(files.values())[0]
        >>> file.get("path")
        C:/Music/PioneerDJ/Sampler/PRESET ONESHOT/NOISE.wav

        """
        if isinstance(content, (int, str)):
            content = self.get_content(ID=content)
        cid = content.ID

        # Check and format path (the database and ANLZ files use "/" as path delimiter)
        if check_path:
            assert os.path.exists(path)
        path = path.replace("\\", "/")
        old_path = content.FolderPath
        logger.info("Replacing '%s' with '%s' of content [%s]", old_path, path, cid)

        # Update path in ANLZ files
        anlz_files = self.read_anlz_files(cid)
        for anlz_path, anlz in anlz_files.items():
            logger.debug("Updating path of %s: %s", anlz_path, path)
            anlz.set_path(path)

        # Update path in database (DjmdContent)
        logger.debug("Updating database file path: %s", path)
        content.FolderPath = path

        if save:
            logger.debug("Saving changes")
            # Save ANLZ files
            for anlz_path, anlz in anlz_files.items():
                anlz.save(anlz_path)
            # Commit database changes
            self.commit()

    def update_content_filename(self, content, name, save=True, check_path=True):
        """Update the file name of a track in the Rekordbox v6 database.

        This changes the `FolderPath` entry in the ``DjmdContent`` table and the
        path tag (PPTH) of the corresponding ANLZ analysis files.

        Parameters
        ----------
        content : DjmdContent or int or str
            The ``DjmdContent`` element to change. If an integer is passed the database
            is queried for the content.
        name : str
            The new file name of the database entry.
        save : bool, optional
            If True, the changes made are written to disc.
        check_path : bool, optional
            If True, raise an assertion error if the new file path does not exist.

        See Also
        --------
        update_content_path: Update the file path of a track in the Rekordbox database.

        Examples
        --------
        Updating the file name changes the database entry

        >>> db = Rekordbox6Database()
        >>> cont = db.get_content()[0]
        >>> cont.FolderPath
        C:/Music/PioneerDJ/Sampler/OSC_SAMPLER/PRESET ONESHOT/NOISE.wav

        >>> new_name = "noise"
        >>> db.update_content_filename(cont, new_name)
        >>> cont.FolderPath
        C:/Music/PioneerDJ/Sampler/PRESET ONESHOT/noise.wav

        and updates the file path in the corresponding ANLZ analysis files:

        >>> files = self.read_anlz_files(cont.ID)
        >>> file = list(files.values())[0]
        >>> file.get("path")
        C:/Music/PioneerDJ/Sampler/PRESET ONESHOT/noise.wav

        """
        if isinstance(content, (int, str)):
            content = self.get_content(ID=content)

        old_path = os.path.normpath(content.FolderPath)
        name = os.path.splitext(name)[0]
        ext = os.path.splitext(old_path)[1]
        new_path = os.path.join(os.path.dirname(old_path), name + ext)

        self.update_content_path(content, new_path, save, check_path)
