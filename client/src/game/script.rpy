# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
init python:
    import sys
    config.keymap['toggle_skip'] = []
    config.keymap['skip'] = []
    config.keymap['fast_skip'] = []
    config.keymap['game_menu'] = []

label start:
    image topimage:
        "Title.jpg"
    
    show topimage:
       xanchor 0 yanchor 0 xpos 0 ypos 0
       zoom 1.0
    
    image backimage:
        "black.jpg"
       
    python:
        soundfile = "click.mp3"
        intext = renpy.input('Please enter your user name. Press \"Enter\" to confirm.', length=40)
        intext = intext.strip()
        
        result = senduserid(intext)
    
label loginloop:
    if result == 'failure':
        python:
            intext = renpy.input('The user name you entered, \"'+intext+'\", does not exist. Please re-enter your user name. Press \"Enter\" to confirm.', length=40)
            intext = intext.strip()
            
            result = senduserid(intext)
        jump loginloop
    elif result == 'tomorrow':
        "You have already played a session today. Please wait until tomorrow for the next session."
        jump endcomic
    else:
        show backimage:
            xanchor 0 yanchor 0 xpos 0 ypos 0
            zoom 1.0
        $ sendlog('game start')
        $ filecode = firstfile()
        $ renpy.block_rollback()

# The game starts here.
label realstart:
    
    if filecode != 'end' and filecode != ' ' and filecode != '':
        $ filename = sys.path[0] + "/game/" + filecode + ".txt"
    else:
        jump endcomic
    python:
        gameend = False
        with open(filename):
            file = open(filename)
            line = file.readline().strip()
            top = line.split('\t')
            pos = file.tell()
            file.close()
    
label mainloop:
    
    if gameend == True:
        jump endcomic
    
    image img3:
        top[0]
        
    show img3:
       xanchor int(top[1]) yanchor int(top[2]) xpos int(top[3]) ypos int(top[4])
       zoom float(top[5])
       
    $ sendlog('enter file: '+filecode)

label outloop:
    
    python:
        file = open(filename)
        file.seek(pos)
        inline = file.readline().strip()
        inline = edittext(inline)
        data = inline.split('\t')
        pos = file.tell()
        file.close()
        
    if inline == 'END':
        $ filecode = nextfile()
        $ renpy.block_rollback()
        jump realstart
    if inline == 'GAMEOVER':
        jump endcomic

    if len(data) > 1:
        if data[0] == 'MENU':
            $ sendlog('enter menu')
            jump menuloop
        elif data[0] == 'INPUT':
            $ sendlog('enter input')
            jump inputloop
        elif data[0] == 'FRAME':
            $ sendlog('enter new frame')
            jump frameswitch
        elif data[0] == 'SET':
            $ sendlog('set variable: '+data[1]+' : '+data[2])
            $ updatevars(data[1],data[2])
            jump outloop
        elif data[0] == 'SETSOUND':
            $ sendlog('set sound: '+data[1])
            $ soundfile = data[1]
            jump outloop
        elif data[0] == 'PLAYMUSIC':
            python:
                if data[1] == 'REGULAR':
                    musicname = 'It hit the fan.mp3'
                elif data[1] == 'BATTLE':
                    musicname = 'Ruskies and Outer Space Charlies.mp3'
                else:
                    musicname = None
            if renpy.music.get_playing() != musicname:
                stop music fadeout 1.5
                if musicname != None:
                    queue music musicname
                $ sendlog('play music: '+data[1])
            jump outloop
        elif data[0] == 'FUNC':
            $ sendlog('call function: '+data[1])
            $ perform(data[1])
            jump outloop
        elif data[0] == 'GAMEOVER':
            jump endcomic
        else:
            show expression Text(_(data[0]), size=16, area=(int(data[1]),int(data[2]),int(data[3]),int(data[4])), color="#000", font="comic.ttf") as text1
            " "
            play sound soundfile
            $ soundfile = "click.mp3"
            $ prevdata = data
            $ sendlog('click bubble: '+data[0])
            hide expression text1
            jump outloop
    elif len(data) == 1:
        "%(inline)s"
        play sound soundfile
        $ soundfile = "click.mp3"
        $ sendlog('click narration: '+inline)
        jump outloop
    else:
        jump endcomic
    
label endloop:
    
    if inline == '\n':
        jump outloop
        
    python:
        file = open(filename)
        file.seek(pos)
        inline = file.readline()
        data = inline.split('\t')
        pos = file.tell()
        file.close()
    
    if inline == '':
        jump realstart
    if inline == 'END':
        $ filecode = nextfile()
        $ renpy.block_rollback()
        jump realstart
    if inline == 'GAMEOVER':
        jump endcomic
    
    if data[0] == 'MENU':
        $ sendlog('enter menu')
        jump menuloop
    elif data[0] == 'INPUT':
        $ sendlog('enter input')
        jump inputloop
    elif data[0] == 'FRAME':
        $ sendlog('enter new frame')
        jump frameswitch
    elif data[0] == 'SET':
        $ sendlog('set variable: '+data[1]+' : '+data[2])
        $ updatevars(data[1],data[2])
        jump outloop
    elif data[0] == 'SETSOUND':
        $ sendlog('set sound: '+data[1])
        $ soundfile = data[1]
        jump outloop
    elif data[0] == 'FUNC':
        $ sendlog('call function: '+data[1])
        $ exec(data[1])
        jump outloop
    
    show img3:
        parallel:
            linear 0.5 xpos int(data[0]) ypos int(data[1]) 
        parallel:
            linear 0.5 zoom float(data[2])
            
    $ renpy.pause(0.5)
    jump outloop
    
label frameswitch:
    
    show img3:
        parallel:
            linear 0.5 xpos int(data[1]) ypos int(data[2]) 
        parallel:
            linear 0.5 zoom float(data[3])
            
    $ renpy.pause(0.5)
    jump outloop
    
label menuloop:
    
    show expression Text(_(prevdata[0]), size=16, area=(int(prevdata[1]),int(prevdata[2]),int(prevdata[3]),int(prevdata[4])), color="#000", font="comic.ttf") as text1
    
    python:
        
        test = [(data[1], None, None, None),]
        file = open(filename)
        file.seek(pos)
        for x in range (0, int(data[2])):
            menuline = file.readline().strip()
            data = menuline.split('\t')
            if len(data) == 2:
                test.append( (data[0],data[1],None,None) )
            elif len(data) == 4:
                test.append( (data[0],data[1],data[2],data[3]) )
        pos = file.tell()
        file.close()
        menuitem = test[0][0]
        choice1 = test[1][0]
        res1 = test[1][1]
        key1 = test[1][2]
        val1 = test[1][3]
        if x >= 1:
            choice2 = test[2][0]
            res2 = test[2][1]
            key2 = test[2][2]
            val2 = test[2][3]
        if x >= 2:
            choice3 = test[3][0]
            res3 = test[3][1]
            key3 = test[3][2]
            val3 = test[3][3]
        if x >= 3:
            choice4 = test[4][0]
            res4 = test[4][1]
            key4 = test[4][2]
            val4 = test[4][3]
        if x >= 4:
            choice5 = test[5][0]
            res5 = test[5][1]
            key5 = test[5][2]
            val5 = test[5][3]
        
    menu:
        "%(menuitem)s"
        
        "%(choice1)s":
            $ sendlog('choose option: '+choice1)
            $ result = res1
            $ newkey = key1
            $ newval = val1
            
        "%(choice2)s" if x >= 1:
            $ sendlog('choose option: '+choice2)
            $ result = res2
            $ newkey = key2
            $ newval = val2
        
        "%(choice3)s" if x >= 2:
            $ sendlog('choose option: '+choice3)
            $ result = res3
            $ newkey = key3
            $ newval = val3
        
        "%(choice4)s" if x >= 3:
            $ sendlog('choose option: '+choice4)
            $ result = res4
            $ newkey = key4
            $ newval = val4
        
        "%(choice5)s" if x >= 4:
            $ sendlog('choose option: '+choice5)
            $ result = res5
            $ newkey = key5
            $ newval = val5
            
    "%(result)s"
    if (newkey):
        $ sendlog('set variable: '+newkey+' : '+newval)
        $ updatevars(newkey, newval)
        $ updatestory()
        $ checked = 1
    hide expression text1
        
    jump outloop
    
label inputloop:
    
    python:
        intext = renpy.input(data[1], length=400)
        intext = intext.strip()
        sendlog('user input: '+intext)
        if len(data)>2:
            sendlog('set variable: '+data[2]+' : '+intext)
            updatevars(data[2], intext)
    
    jump outloop

label endcomic:    
    $ sendlog('game end')
    $ endgame()
    $ renpy.quit()
    return
