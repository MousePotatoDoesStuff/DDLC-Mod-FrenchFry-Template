init python:
    menu_trans_time = 1
    splash_message_default = '\"If I have seen further (than others),\nit is by standing on the shoulders of giants.\"\n\n- Isaac Newton'''
    splash_messages = ["insert funni message here"]

label splashscreen:

    python:
        process_list = []
        currentuser = ""
        if renpy.windows:
            try:
                process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
            except:
                pass
            try:
                for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                    user = os.environ.get(name)
                    if user:
                        currentuser = user
            except:
                pass
        firstrun = ""
        try:
            firstrun = renpy.file("firstrun").read(1)
        except:
            with open(config.basedir + "/game/firstrun", "wb") as f:
                pass
    if not firstrun:
        if persistent.first_run and (config.version == persistent.oldversion or persistent.autoload == "postcredits_loop"):
            $ quick_menu = False
            scene black
            menu:
                "A previous save file has been found. Would you like to delete your save data and start over?"
                "Yes, delete my existing data.":
                    "Deleting save data...{nw}"
                    python:
                        delete_all_saves()
                        renpy.loadsave.location.unlink_persistent()
                        renpy.persistent.should_save_persistent = False
                        renpy.utter_restart()
                "No, continue where I left off.":
                    $ restore_relevant_characters()
        python:
            if not firstrun:
                try:
                    with open(config.basedir + "/game/firstrun", "w") as f:
                        f.write("1")
                except:
                    renpy.jump("readonly")

    if config.version != persistent.oldversion:
        $ restore_relevant_characters()
        $ persistent.oldversion = config.version
        $ renpy.save_persistent()

    if not persistent.first_run:
        python:
            restore_all_characters()
        $ quick_menu = False
        scene white
        pause 0.5
        scene tos
        with Dissolve(1.0)
        pause 1.0
        # ==================================================================================================================================================
        # CHANGE THIS TO YOUR OWN TERMS OF SERVICE
        # ==================================================================================================================================================
        "[config.name] is a fan-made production and is not in any way affiliated with Team Salvato or Serenty Forge."
        "Users of this template are highly encouraged to both complete the original game and understand the IP guidelines set in place for this product."
        "This template is not intended to be used for commercial purposes, and is only meant to be used as a base for fan works."
        "Please support the official release on ddlc.moe."
        menu:
            "By using this template, you agree to the IP guidelines set forth by Team Salvato, and you have completed DDLC previously."
            "I agree.":
                pass
            "I do not agree.":
                "Then I cannot allow you to use this template."
                $ renpy.quit()
        $ persistent.first_run = True
        scene tos2
        with Dissolve(1.5)
        pause 1.0
        scene white

    python:
        restore_relevant_characters()

    $ basedir = config.basedir.replace('\\', '/')

    if persistent.autoload:
        jump autoload

    show white
    python:
        config.allow_skipping = False
        persistent.ghost_menu = False
        splash_message = splash_message_default
        renpy.music.play(config.main_menu_music)
        starttime = datetime.datetime.now()
    show intro with Dissolve(0.5, alpha=True)
    $ pause(3.0 - (datetime.datetime.now() - starttime).total_seconds())
    hide intro with Dissolve(max(0, 3.5 - (datetime.datetime.now() - starttime).total_seconds()), alpha=True)

    if renpy.random.randint(0, 3) == 0:
        $ splash_message = renpy.random.choice(splash_messages)
    show splash_warning "[splash_message]" with Dissolve(max(0, 4.0 - (datetime.datetime.now() - starttime).total_seconds()), alpha=True)
    $ pause(6.0 - (datetime.datetime.now() - starttime).total_seconds())
    hide splash_warning with Dissolve(max(0, 6.5 - (datetime.datetime.now() - starttime).total_seconds()), alpha=True)
    $ pause(6.5 - (datetime.datetime.now() - starttime).total_seconds())
    $ config.allow_skipping = True
    return

label after_load:
    if persistent.playthrough == 0:
        $ restore_all_characters()
    $ config.allow_skipping = allow_skipping
    $ _dismiss_pause = config.developer
    $ persistent.ghost_menu = False
    $ style.say_dialogue = style.normal

    if anticheat != persistent.anticheat:
        stop music
        scene black
        "The save file could not be loaded."
        "Are you trying to cheat?"
        $ m_name = "Monika"
        show monika 1 at t11
        if persistent.playername == "":
            m "You're so funny."
        else:
            m "You're so funny, [persistent.playername]."
        $ renpy.utter_restart()
        return
    
    if persistent.playthrough == 0 and not persistent.first_load and not config.developer:
        $ persistent.first_load = True
        call screen dialog("Hint: You can use the \"Skip\" button to\nfast-forward through text you've already read.", ok_action=Return())
    return

label autoload:
    python:
        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen
        if "_old_history" in globals():
            _history = _old_history
            del _old_history
        renpy.block_rollback()
        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None
        if renpy.get_return_stack():
            renpy.pop_call()
    jump expression persistent.autoload

label before_main_menu:
    return
label quit:
    return

label readonly:
    scene black
    "The game cannot be run because you are trying to run it from a read-only location."
    "Please copy the DDLC application to your desktop or other accessible location and try again."
    $ renpy.quit()
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
