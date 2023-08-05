#!/usr/bin/env python

import argparse
import configparser
import json
import os
import shutil
import subprocess
import sys


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        help=(
            "profile to use if ARM_PROFILE not set. if ARM_PROFILE is set, this "
            "will override it."
        ),
    )
    parser.add_argument(
        "--ignore-missing",
        action="store_true",
        help=(
            "if no matching config section is found, continue processing anyway "
            "without setting environment variables."
        ),
    )

    subparsers = parser.add_subparsers(dest="command")

    exec_parser = subparsers.add_parser("exec")
    exec_parser.add_argument("command", nargs=argparse.REMAINDER)
    exec_parser.set_defaults(which="exec")

    env_parser = subparsers.add_parser("env")
    env_parser.set_defaults(which="env")

    eval_parser = subparsers.add_parser("eval")
    eval_parser.set_defaults(which="eval")

    refresh_parser = subparsers.add_parser("refresh")
    refresh_parser.set_defaults(which="refresh")

    args = parser.parse_args()

    credentials_dir = os.path.expanduser("~/.azure/")
    credentials_path = os.path.join(credentials_dir, "credentials")

    if not os.path.exists(credentials_dir):
        if not args.ignore_missing:
            sys.stderr.write("no credentials dir\n")
            sys.stderr.flush()
            sys.exit(1)

    if not os.path.exists(credentials_path):
        if not args.ignore_missing:
            sys.stderr.write("no credentials path\n")
            sys.stderr.flush()
            sys.exit(1)

    if os.path.exists(credentials_path):
        file_stat = os.stat(credentials_path)
        file_mask = oct(file_stat.st_mode)[-3:]
        if file_mask != "600":
            sys.stderr.write(
                "permissions {} on {} are too broad, must be exactly 600\n"
                .format(
                    file_mask,
                    credentials_path,
                )
            )
            sys.stderr.flush()
            sys.exit(1)

    if os.path.exists(credentials_path):
        config = configparser.ConfigParser()
        config.read(credentials_path)
    else:
        config = {}

    profile = os.environ.get("ARM_PROFILE")
    if args.profile:
        profile = args.profile

    if profile not in config:
        if not args.ignore_missing:
            sys.stderr.write("no config for env {}\n".format(profile))
            sys.stderr.flush()
            sys.exit(1)

    azure_vars = {}
    if profile in config:
        for key, value in config[profile].items():
            azure_vars[key.upper()] = value

    new_environ = os.environ.copy()
    new_environ.update(azure_vars)
    new_environ["ERUZA"] = "1"
    new_environ["ERUZA_PROFILE"] = profile

    do_refresh = False
    if args.which == "refresh":
        do_refresh = True
    else:
        access_tokens_path = os.path.expanduser("~/.azure/accessTokens.json")
        if os.path.exists(access_tokens_path):

            found_token = False

            with open(access_tokens_path, "rt") as access_tokens_fp:
                access_tokens = json.load(access_tokens_fp)

                for access_token in access_tokens:
                    if "ARM_CLIENT_ID" in new_environ:
                        if access_token["servicePrincipalId"] == new_environ["ARM_CLIENT_ID"]:
                            found_token = True
                            break

            if not found_token:
                do_refresh = True

    if do_refresh:

        has_vars = (
            "ARM_APPLICATION_ID" in new_environ
            and "ARM_CLIENT_SECRET" in new_environ
            and "ARM_TENANT_ID" in new_environ
        )

        if not has_vars:
            if args.ignore_missing:
                pass
            else:
                sys.stderr.write(
                    "missing ARM_APPLICATION_ID, ARM_CLIENT_SECRET, or "
                    "ARM_TENANT_ID\n"
                )
                sys.stderr.flush()
                sys.exit(1)
        else:
            az_login_args = [
                "az",
                "login",
                "--service-principal",
                "-u",
                new_environ["ARM_APPLICATION_ID"],
                "-p",
                new_environ["ARM_CLIENT_SECRET"],
                "--tenant",
                new_environ["ARM_TENANT_ID"],
            ]

            az_login_process = subprocess.Popen(
                az_login_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = az_login_process.communicate()

            if az_login_process.returncode:
                sys.stderr.write("refresh failed!\n")
                sys.stderr.buffer.write(stdout)
                sys.stderr.buffer.write(stderr)
                sys.stderr.flush()
                sys.exit(az_login_process.returncode)

    if args.which == "refresh":
        pass
    elif args.which == "env":
        for key, value in new_environ.items():
            print("{}={}".format(key, value))
    elif args.which == "eval":
        for key, value in new_environ.items():
            if key.startswith("ARM_") or key.startswith("ERUZA_"):
                print("export {}={}".format(key, value))

    elif args.which == "exec":
        if args.command:
            new_command = args.command
        else:
            new_command = [os.environ.get("SHELL", "/bin/sh")]

        exec_path = new_command[0]
        if not "/" in exec_path:
            maybe_exec_path = shutil.which(exec_path)
            if maybe_exec_path:
                exec_path = maybe_exec_path

        os.execve(exec_path, new_command, new_environ)
    else:
        raise Exception(
            "Implementation Error: unknown value for args.which {}"
            .format(args.which)
        )
