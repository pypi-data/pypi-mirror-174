# Copyright (c) 2022 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import textwrap

import qumulo.lib.opts
import qumulo.rest.saml as saml

from qumulo.rest_client import RestClient


class GetSettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 'saml_get_settings'
    SYNOPSIS = 'Get cluster SAML configuration'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(rest_client.saml.get_settings().data.to_json())


class ModifySettingsCommand(qumulo.lib.opts.Subcommand):
    NAME = 'saml_modify_settings'
    SYNOPSIS = 'Modify cluster SAML configuration'

    DESCRIPTION = SYNOPSIS + textwrap.dedent(
        """

        To enable SAML single sign-on (SSO) for your cluster, contact your SSO administrator.
        Provide your administrator with the Service Provider endpoint, including the fully qualified
        domain name (FQDN) for your cluster (for example, https://mycluster.example.com/saml).
        Your administrator creates the SAML integration for your Qumulo cluster and provides you
        with the configuration parameters for this command, which lets you complete the integration
        on your cluster.

        Note: For SSO to work, your cluster must be joined to an Active Directory domain that is
        connected to your SAML Identity Provider.
        """
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        enable_group = parser.add_mutually_exclusive_group()
        enable_group.add_argument(
            '--disable',
            '-d',
            dest='enabled',
            help='Disable authentication via SAML',
            action='store_false',
            default=None,
        )
        enable_group.add_argument(
            '--enable',
            '-e',
            dest='enabled',
            help='Enable authentication via SAML',
            action='store_true',
            default=None,
        )
        parser.add_argument('--idp-sso-url', help="Sets the cluster's configured IDP SSO URL.")

        certificate_group = parser.add_mutually_exclusive_group()
        certificate_group.add_argument(
            '--idp-certificate',
            help="Sets the cluster's configured IDP public key with the given value in PEM format.",
            default=None,
        )
        certificate_group.add_argument(
            '--idp-certificate-file',
            help="Sets the cluster's configured IDP public key from a PEM file.",
            default=None,
        )

        parser.add_argument(
            '--idp-entity-id',
            help='Sets the URI for the IDP this cluster trusts to authenticate users via SAML.',
        )
        parser.add_argument(
            '--cluster-dns-name', help="Sets the cluster's configured DNS name (must be FQDN)."
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        config = saml.ConfigV1Patch()

        if (
            args.enabled is None
            and args.idp_sso_url is None
            and args.idp_certificate is None
            and args.idp_certificate_file is None
            and args.idp_entity_id is None
            and args.cluster_dns_name is None
        ):
            err_msg = (
                'At least one of the following arguments is required: [--disable, --enable,'
                ' --idp-sso-url, --idp-certificate, --idp-certificate-file, --idp-entity-id,'
                ' --cluster-dns-name]'
            )
            raise ValueError(err_msg)

        if args.enabled is not None:
            config.enabled = args.enabled

        if args.idp_sso_url is not None:
            config.idp_sso_url = args.idp_sso_url

        if args.idp_certificate is not None:
            config.idp_certificate = args.idp_certificate
        elif args.idp_certificate_file is not None:
            with open(args.idp_certificate_file) as f:
                config.idp_certificate = f.read()

        if args.idp_entity_id is not None:
            config.idp_entity_id = args.idp_entity_id

        if args.cluster_dns_name is not None:
            config.cluster_dns_name = args.cluster_dns_name

        print(rest_client.saml.modify_settings(config).to_json())
