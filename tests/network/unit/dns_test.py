# SPDX-FileCopyrightText: Red Hat, Inc.
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import division

import io

from unittest import mock

from vdsm.network import dns


class TestNetworkDnsUnit(object):
    @mock.patch.object(dns, 'open', create=True)
    def test_get_host_nameservers(self, mock_open):
        RESOLV_CONF = (
            '# Generated by NetworkManager\n'
            'search example.com company.net\n'
            'domain example.com\n'
            'nameserver 192.168.0.100\n'
            'nameserver 8.8.8.8\n'
            'nameserver 8.8.4.4\n'
        )
        expected_nameservers = ['192.168.0.100', '8.8.8.8', '8.8.4.4']
        resolv_conf_stream = io.StringIO(RESOLV_CONF)
        mock_open.return_value.__enter__.return_value = resolv_conf_stream

        resulted_nameservers = dns.get_host_nameservers()
        assert expected_nameservers == resulted_nameservers

    @mock.patch.object(dns, 'open', create=True)
    def test_get_host_nameservers_no_resolvconf(self, mock_open):
        mock_open.return_value.__enter__.side_effect = IOError()

        nameservers = dns.get_host_nameservers()
        assert nameservers == []
