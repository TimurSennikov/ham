import argparse

from functions import *

parser = argparse.ArgumentParser(prog="ham", description="HAM (HL Addon Manager) is used to easily manage Half-Life texture packs.")

parser.add_argument("-g", "--game", help="Specify game directory", type=str)

subparsers = parser.add_subparsers(required=True)

parser_init = subparsers.add_parser("init", help="Initialize HAM texturepack in current directory")
parser_init.add_argument("name", type=str)
parser_init.set_defaults(func=hamparser_init)

parser_bg = subparsers.add_parser("bg", help="Replace HAM texturepack background image")
parser_bg.add_argument("name", type=str)
parser_bg.set_defaults(func=hamparser_addbg)

parser_skybox = subparsers.add_parser("skybox", help="Replace HAM texturepack skybox image")
parser_skybox.add_argument("name", type=str, help="Input image")
parser_skybox.add_argument("--skybox", type=str, help="Skybox name. Could be different from the ones present in valve/ directory, be warned. Leave empty to replace all of the available skyboxes.", required=False, default=None)
parser_skybox.set_defaults(func=hamparser_addskybox)

parser_install = subparsers.add_parser("install", help="Install HAM texturepack to game.")
parser_install.add_argument("--hamfile", default=None, help="HAM file to install from. Defaults to installing from current directory tree if not specified.")
parser_install.add_argument("--destination", type=str, default="valve_addon", help="Install destination relative to HL directory. Defaults to 'valve_addon'.")
parser_install.set_defaults(func=hamparser_install)

parser_build = subparsers.add_parser("build", help="Build HAM texturepack to store it in single file.")
parser_build.set_defaults(func=hamparser_build)

parser_uninstall = subparsers.add_parser("uninstall", help="Uninstall active HAM texturepack from game.")
parser_uninstall.set_defaults(func=hamparser_uninstall)

parser_history = subparsers.add_parser("history", help="Install HAM texturepack to game.")
parser_history.add_argument("--limit", type=int, default=None, help="History entries limit.")
parser_history.set_defaults(func=hamparser_history)


