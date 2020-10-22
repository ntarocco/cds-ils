# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# cds-migrator-kit is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CDS-ILS ldap users CLI."""

import click
from flask import current_app
from flask.cli import with_appcontext

from .api import import_ldap_users, sync_users
from .models import LdapSynchronizationLog


@click.group()
def ldap_users():
    """Ldap users import CLI."""


@ldap_users.command(name="import")
@with_appcontext
def import_users():
    """Load users from ldap and import them in db."""
    import_ldap_users()


@ldap_users.command(name="sync")
@with_appcontext
def ldap_sync_users():
    """Add entry to database with info about this synchronization."""
    log = LdapSynchronizationLog.create_cli()
    try:
        result = sync_users()
        log.set_succeeded(*result)
    except Exception as e:
        current_app.logger.exception(e)
        log.set_failed(e)
