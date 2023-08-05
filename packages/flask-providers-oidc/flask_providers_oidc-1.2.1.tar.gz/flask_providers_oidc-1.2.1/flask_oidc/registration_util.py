# Copyright (c) 2022 -, VestiaireCollective
# Copyright (c) 2014-2015, Erica Ehrhardt
# Copyright (c) 2016, Patrick Uiterwijk <patrick@puiterwijk.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# standard library
import argparse
import json
import logging
import os.path
import sys

# flask providers - flask oidc
from flask_oidc import discovery, registration

logging.basicConfig()
logger = logging.getLogger("oidc-register")


def _parse_args():
    parser = argparse.ArgumentParser(description="Help register an OpenID " "Client")
    parser.add_argument("provider_url", help="Base URL to the provider to register at")
    parser.add_argument("application_url", help="Base URL to the application")
    parser.add_argument("--token-introspection-uri", help="Token introspection URI")
    parser.add_argument("--output-file", default="client_secrets.json", help="File to write client info to")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main():
    args = _parse_args()
    if os.path.exists(args.output_file):
        logger.exception("Output file exists. Please provide other filename")
        return 1

    if args.debug:
        logger.setLevel(logging.DEBUG)

    redirect_uris = [f"{args.application_url}/oidc_callback"]
    registration.check_redirect_uris(redirect_uris)
    try:
        OP = discovery.discover_OP_information(args.provider_url)
    except Exception as ex:
        logger.exception("Error discovering OP information")
        logger.exception(f"Error caught when discovering OP information: {ex}")
        return 1
    if args.debug:
        print(f"Provider info: {OP}")
    try:
        reg_info = registration.register_client(OP, redirect_uris)
    except Exception as ex:
        logger.exception("Error registering client")
        logger.exception(f"Error caught when registering the client: {ex}")
        return 1

    logger.debug(f"Registration info: {reg_info}" % reg_info)

    if args.token_introspection_uri:
        reg_info["web"]["token_introspection_uri"] = args.token_introspection_uri

    with open(args.output_file, "w") as outfile:
        outfile.write(json.dumps(reg_info))
        logger.info("Client information file written")


if __name__ == "__main__":
    retval = main()
    if retval:
        sys.exit(retval)
