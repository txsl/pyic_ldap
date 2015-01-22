import logging

import ldap, ldap.filter


class ICAdsLdap(object):

    def __init__(self):
        self.conn = ldap.initialize('ldaps://icadsldap.ic.ac.uk')
        logging.warning('ICADS LDAP link not fully developed or tested yet. Use with caution!')

    def auth_bind(self, user, passw):

        if not user or not passw:
            print 'something empty'
            return False

        dn = "{}@ic.ac.uk".format(ldap.filter.escape_filter_chars(user, 1))
        
        try:
            self.conn.bind_s(dn, passw)
            return True
        except ldap.INVALID_CREDENTIALS:
            # Bad user/pass
            return False

        # Although we really shouldn't reach here
        return False


class ICUnixLdap(object):

    def __init__(self):
        self.conn = ldap.initialize('ldaps://unixldap.cc.ic.ac.uk')

    def bind(self):
        self.conn.simple_bind_s()

    def auth_bind(self, user, passw):

        if not user or not passw:
            print 'something empty'
            return False

        # Filter out any bad characters
        dn = 'uid=%s,ou=People,ou=everyone,dc=ic,dc=ac,dc=uk' % ldap.filter.escape_filter_chars(user, 1)

        try:
            # Bind OK
            self.conn.bind_s(dn, passw)
            return True
        except ldap.INVALID_CREDENTIALS:
            # Bad user/pass
            return False

        # Although we really shouldn't reach here
        logging.warning("ICUnixLdap auth_bind with username {0} failed to complete successfully, but was not caught as invalid credentials".format(user))
        return False

    def get_details(self, user, return_list=True):

        # If one username (and a string) is put in a list
        if isinstance(user, str):
            user = [user]

        basedn = "ou=People,ou=shibboleth,dc=ic,dc=ac,dc=uk"

        # Query for all users, one by one
        output = []
        for i in user:
            filt_uname = "uid={0}".format(ldap.filter.escape_filter_chars(str(i), 1))

            query_result = self.conn.search_s(basedn, ldap.SCOPE_SUBTREE, filt_uname)

            for dn, entry in query_result:

            # Filter to the values we want to keep
                entry = {key: entry[key] for key in
                                    ['uid', 'mail', 'sn', 'givenName', 'displayName']}

            # We want to return strings not a list of one item (results should be one item!)
                for key, item in entry.iteritems():
                    entry[key] = item[0]

            if not query_result:
                entry = None

            # If we are returning a list (default)
            if return_list:
                output.append(entry)
            else:  # This should only be called if ther is one result to return (and as a dict)
                return entry

        return output

    def close(self):
        self.conn.unbind()

    def __del__(self):
        self.close()
