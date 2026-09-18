from zipfile import ZipFile

from hl import *
from ham import HAMPack, HAMZip, Game

def ask_for_changes():
    i = input("?: ") != 'Y'

    if i:
        print("Discarding changes; Have a good day!")

    return not i

def locate_game_ask(args):
    game = locate_game()
    while not game and args.game:
        game = input("HL directory not found. Please enter ABSOLUTE path (starting with /): ")
        if not (os.path.exists(game) and os.path.isdir(game)):
            game = None
    return args.game or game

def hamparser_init(args):
    game = locate_game_ask(args)
    
    pack = HAMPack(args.name)

def hamparser_addbg(args):
    game = locate_game_ask(args)

    pack = HAMPack(None, False)

    images = image_to_bg(args.name)

    if len(pack.conflicts_list([i["name"] for i in images])) > 0:
        print("Conflicts detected (most probably another BG is already present in the pack). If you would like to overwrite BG enter Y; Enter any other key to discard changes.")

        if not ask_for_changes():
            return

    if not os.path.exists(os.path.dirname(images[0]["name"])):
        os.makedirs(os.path.dirname(images[0]["name"]))

    for img in images:
        print(f"Adding {img['name']} to {pack.name} ...")
        pack.register(img["name"])

        img["img"].save(img['name'])

    print(f"\nSuccessfully added BG {args.name} to {pack.name}!")

def hamparser_addskybox(args):
    game = locate_game_ask(args)
    game = Game(game)

    pack = HAMPack(None, False)

    if args.skybox:
        images = image_to_skybox(args.name, args.skybox)
    else:
        img = image_to_skybox(args.name)

        images = [{"name": f"gfx/env/{f}", "img": img} for f in [os.path.basename(j) for j in os.listdir(f"{game.directory}/valve/gfx/env")]]

    if len(pack.conflicts_list([i["name"] for i in images])) > 0:
        print("Conflicts detected (most probably same skybox is already present in the pack). If you would like to overwrite it enter Y; Enter any other key to discard changes.")

        if not ask_for_changes():
            return

    if not os.path.exists(os.path.dirname(images[0]["name"])):
        os.makedirs(os.path.dirname(images[0]["name"]))

    for img in images:
        print(f"Adding {img['name']} to {pack.name} ...")
        pack.register(img["name"])

        img["img"].save(img["name"])

    print(f"\nSuccessfully added skybox {args.name} to {pack.name}!")

def hamparser_build(args):
    game = locate_game_ask(args)

    pack = HAMPack(None, False)

    if not os.path.exists("release/"):
        os.mkdir("release/")
    elif not os.path.isdir("release/"):
        raise Exception("'release' already exists and is not a directory.")

    pn = f"release/{pack.name}.ham"

    with ZipFile(pn, 'w') as zf:
        for fn in pack.files:
            with open(fn, 'rb') as of:
                with zf.open(fn, 'w') as f:
                    data = of.read()
                    f.write(data)
        with open("hampack.json", 'rb') as of:
            with zf.open("hampack.json", 'w') as f:
                f.write(of.read())

    print(f"Built {pn}")

def hamparser_install(args):
    game = locate_game_ask(args)

    destination = args.destination

    pack = HAMPack(None, False) if not args.hamfile else HAMZip(args.hamfile)

    game = Game(game)

    if game.current_pack:
        print(f"This action will DELETE current pack ({game.current_pack['name']}). Y to continue; any other key to abort.")
        if not ask_for_changes():
            return

    game.install(pack)

def hamparser_uninstall(args):
    game = locate_game_ask(args)

    game = Game(game)

    if game.current_pack:
        print(f"This action will DELETE current pack ({game.current_pack['name']}). Y to continue; any other key to abort.")
        if not ask_for_changes():
            return

    game.uninstall()

def hamparser_history(args):
    game = locate_game_ask(args)

    game = Game(game)

    history = list(reversed(game.history))

    if len(history) == 0:
        print("No HAM packs installed yet. Maybe try it with 'ham install'?")

    for i in range(min(args.limit if args.limit else len(history) - 1, len(history) - 1)):
        print(history[i]["name"], "INSTALLED AT", history[i]["install_dir"])
