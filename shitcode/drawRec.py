# coding: utf-8

import os
from PIL import Image

default_skin = 'New!+game!'

class DrawRec():
    def __init__(self, skin=None):
        self.width = 1366
        self.height = 768
        self.skin = skin if skin else default_skin
        self.RecImg = Image.new('RGBA', (self.width, self.height), 0) 

    def get_img(self, iname):
        return Image.open('%s/%s' % (self.skin, iname))

    def add_items(self, fname, x, y, **kwargs):
        itemImg = self.get_img(fname)
        if kwargs.get('isresize', False):
            itemImg = itemImg.resize((kwargs.get('width', self.width), kwargs.get('height', self.height)))
        if kwargs.get('ismask', 1):
            mask = itemImg
        else:
            mask = None 
        self.RecImg.paste(itemImg, (x, y), mask=mask)

    def save(self):
        self.RecImg.save('rec.png')


bg = 'fail-background.png'

rank_lev_x = 985
rank_lev_y = 80
rank_lev_type = 'ranking-S.png'

mod_x = 1260
mod_y = 380
mod = 'selection-mod-hardrock.png'

mod2_x = 1230
mod2_y = 380
mod2 = 'selection-mod-doubletime.png'

back_icon = 'menu-back-0.png'
back_icon_x = 20
back_icon_y = 600

ranking_icon = 'ranking-title.png'
ranking_icon_x = 1150
ranking_icon_y = 10

if __name__ == '__main__':
    d = DrawRec()
    d.add_items(bg, 0, 0, isresize=True, ismask=False)
    d.add_items(rank_lev_type, rank_lev_x, rank_lev_y)
    d.add_items(mod, mod_x, mod_y)
    d.add_items(mod2, mod2_x, mod2_y)
    d.add_items(back_icon, back_icon_x, back_icon_y)
    d.add_items(ranking_icon, ranking_icon_x, ranking_icon_y)
    d.save()