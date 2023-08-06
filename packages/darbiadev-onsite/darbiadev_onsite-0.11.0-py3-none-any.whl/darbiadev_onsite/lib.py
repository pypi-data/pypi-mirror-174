"""Wrapping an ODBC connection to OnSite"""

from __future__ import annotations

from importlib.resources import files

import jaydebeapi


class OnSiteServices:  # pylint: disable=too-few-public-methods
    """A class wrapping an ODBC connection to OnSite.

    This class wraps an ODBC connection to OnSite.
    """

    def __init__(
        self,
        connection_url: str,
        username: str,
        password: str
    ):
        self._connection_url: str = connection_url
        self.__username: str = username
        self.__password: str = password

    def _connect(
        self,
    ):
        return jaydebeapi.connect(
            "com.filemaker.jdbc.Driver",
            self._connection_url,
            [self.__username, self.__password],
            str(files("darbiadev_onsite").joinpath("vendor/fmjdbc.jar")),
        )

    def _make_query(
        self,
        sql: str,
    ) -> list[dict[str, str | int | float]]:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
