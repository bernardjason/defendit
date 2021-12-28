import game

try:

    import simpleaudio as sa

    phaser_fire_sound = sa.WaveObject.from_wave_file(game.RESOURCES + 'phaser.wav')
    rescued_sound = sa.WaveObject.from_wave_file(game.RESOURCES + 'pickup.wav')
    explosion_sound = sa.WaveObject.from_wave_file(game.RESOURCES + 'explosion.wav')
    hit_alient_sound = sa.WaveObject.from_wave_file(game.RESOURCES + 'hitalien.wav')


    def phaser_fire():
        phaser_fire_sound.play()


    def rescued():
        rescued_sound.play()


    def explosion():
        explosion_sound.play()


    def hit_alien():
        hit_alient_sound.play()


except ImportError as e:
    print(e)


    def phaser_fire():
        return


    def rescued():
        return


    def explosion():
        return


    def hit_alien():
        return
