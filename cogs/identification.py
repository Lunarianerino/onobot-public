
import discord
#from discord import client
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
from discord_components import *
import io
import discord_components
import requests
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageFont
import unicodedata
import sqlite3
from discord import Embed

#MAKE A 9x9 COMMAND JUST CUS

class IDCard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.antialias = 30
        
        self.profile_pic_w, self.profile_pic_h = 100,100
        self.width, self.height = 500,300 #creates the id template

        self.frame_w, self.frame_h = (self.profile_pic_w + 15), (self.profile_pic_h + 15)

        self.username_w, self.username_h = (500 - self.frame_w - 20), (self.frame_h - 30)
        self.background_color = (44,47,51) #for testing
        #self.background_color = (255,255,255)
        self.heading1_font_color = (255,255,255)

        self.subhead2 = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size =10)
        self.heading1 = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size = 40)
        self.subhead1 = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size = 20)

        self.custom_id = [1,2,3,4]
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('IDCard is working :)')
    
    @commands.command()
    async def pfp(self, ctx, user:discord.Member=None):
        usermentions = ctx.message.mentions
        if len(usermentions) == 0 :
            user = ctx.author
        else:
            user = usermentions[0]
        await ctx.send(user.avatar_url)

    @commands.command()
    async def id(self, ctx, user: discord.Member=None):
        """Prints your ID"""
        user = ctx.author

        

        #image = Image.open('./cogs/images/white2.png').convert('RGB') #convert to Image.new soon lol
        image = Image.new('RGB', (self.width,self.height), color = self.background_color)
        mask = Image.open('./cogs/images/circlemask.png').convert('L')

        mask = mask.resize((self.profile_pic_w,self.profile_pic_h))
        
        #Profile Picture of User
        profile_pic = Image.open(requests.get(user.avatar_url, stream=True).raw).convert('RGBA') #puts the profile picture of user to template
        profile_pic_size = (self.profile_pic_w, self.profile_pic_h)
        profile_pic = profile_pic.resize(profile_pic_size, Image.LANCZOS)
        profile_pic= crop_circle(profile_pic)

        #Frame for Profile Picture
        frame = Image.new('RGBA', ((self.frame_w)*self.antialias, (self.frame_h*self.antialias)), color = self.background_color) #padding purposes
        d_frame = ImageDraw.Draw(frame)
        d_frame.ellipse((0,0,self.frame_w*self.antialias, self.frame_h*self.antialias),fill = 'white', outline = 'white', width = 20)
        frame = frame.resize((self.frame_w , self.frame_h),Image.LANCZOS)
        #frame.show()

        #Display Username
        pname = ''
        name_str = str(user)
        print(name_str)
        name_list = name_str.split('#')

        for name in name_list:
            if name != name_list[-1]:
                pname = pname + name
        
        profilename = unicode_characters(pname)
        profile_tag = '#' + name_list[-1]
        #print(profilename)
        
        if len(profilename) < 15:
            self.heading1.size = 40
        else:
            self.heading1 = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size = 30)
        
        username = Image.new('RGBA', (self.username_w,self.username_h), color = self.background_color)
        d_username = ImageDraw.Draw(username)

        #self.username_font = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size = font_size)
        d_username.text((0,15), profilename, fill = self.heading1_font_color,font = self.heading1,  align = 'center')        
        d_username.text((0, self.heading1.size + 20), profile_tag, fill = 'white', font = self.subhead1, align = 'center' )

        username = remove_background(username, self.background_color)

        pfp_offset = center_offset(self.frame_w,self.frame_h,self.profile_pic_w,self.profile_pic_h)
        frame = remove_background(frame, self.background_color)
        frame.paste(profile_pic, pfp_offset, profile_pic.convert('RGBA'))
        
        frame = frame.resize((self.frame_w - 20,self.frame_h - 20), Image.LANCZOS)

        #Favorite Anime Section
        anime_border = create_rect(300, 175, 'Favorite _____')
        #anime_border = remove_background(anime_border, 'black')
        

        image.paste(frame, (10,10), frame.convert('RGBA'))
        image.paste(username, (self.frame_w + 10 , 10), username.convert('RGBA'))
        image.paste(anime_border,(10, self.frame_h + 5), anime_border.convert('RGBA'))

        with io.BytesIO() as image_binary: #so i dont have to save the dumb thing as a seperate image
                    image.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
    
    @commands.command()
    async def edit(self, ctx, user: discord.Member = None):
        pass
    
    @commands.command()
    async def setup(self, ctx):
        """Use this first in order to use xid"""
        user = ctx.message.author
        #options = drop_menu()
        labellst = list()
        await user.send('Choose what you want to display:',
            components = [
            Select(placeholder = "Favorite #1", options = drop_menu(1)),
            Select(placeholder = "Favorite #2", options = drop_menu(2)),
            Select(placeholder = "Favorite #3", options = drop_menu(3)),
            Select(placeholder = "Favorite #4", options = drop_menu(4)),
        ]
        )
        while True:
            event = await self.client.wait_for('select_option',check=None)
            label = str(event.values[0]).split()
            try:
                labellst[int(label[-1])-1] = label[0]
            except:
                labellst.append(label[0])
            
            #add submit button which sends to sql and deletes items in list
            if len(labellst) == 4:
                await event.send(content = f"You chose: {', '.join(labellst)}") #replace with the submit button
            else:
                await event.respond(type = 6)


        
def setup(client): #allows the cog to communicate with the bot
    client.add_cog(IDCard(client))

def remove_background(img,color):
    datas = img.getdata()
    newData = []

    for item in datas:
        if item[:3] == color:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img

def crop_circle(img):

    width, height = img.size
    mask = Image.new('L', (width*30, height*30))
    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse((0, 0, width*30, height*30), fill=255)
    #mask.show()
    mask = mask.filter(ImageFilter.UnsharpMask)
    mask = mask.resize(img.size, Image.LANCZOS)

    #modifies only the copied image cus fuck putalpha making background black
    img2 = img.copy()
    img2.putalpha(mask)
    img.paste(img2, img)

    #add mask as alpha channel
    #img = img.putalpha(mask)
    return img
def create_rect(width, height, text):
    image = Image.new("RGBA", (width*5, height*5), (0,0,0))
    draw = ImageDraw.Draw(image)
    # Draw a rounded rectangle

    subhead2 = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size =50)
    draw.rounded_rectangle((0, 0, width * 5, height*5), fill = (0,0,0), outline="white",
                           width=7, radius=15)
    
    draw.text((15,0), text = text, font = subhead2, fill = 'white')
    
   
    
    image = remove_background(image, (0,0,0))
    image = image.resize((width, height))
    return image
def center_offset(destination_w, destination_h, image_w, image_h):
    centered_offset = ((destination_w - image_w) // 2, (destination_h - image_h) // 2) #so its centered
    return centered_offset

def unicode_characters(text):
    profile_name = ''
    for letter in text:
        if letter.isalpha() == True:
            name = unicodedata.name(letter)
            #print(name)
            name_lst = name.split(' ')
            #print(name_lst)
            for item in name_lst:
                if len(item) == 1:
                    if 'CAPITAL' in name_lst:
                        item = item.capitalize()
                    elif 'SMALL':
                        item = item.lower()
                    else:
                        item = item.lower()
                    profile_name = profile_name + item
                    break
        else:
            profile_name = profile_name + letter
            
    return profile_name

def drop_menu(number):
    number = str(number)
    options = [
            SelectOption(
                label = 'Anime',
                value = 'Anime ' + number,        
                description = 'Displays your favorite anime',
                emoji = PartialEmoji(id = '881813985094152192', name = "anime")
            ),
            SelectOption(
                label = 'Movie',
                value = 'Movie ' + number,        
                description = 'Displays your favorite movie',
                emoji = PartialEmoji(id = '881814309427109908', name = "pepestar")
            ),
            SelectOption(
                label = 'Novel',
                value = 'Novel ' + number,        
                description = 'Displays your favorite novel',
                emoji = PartialEmoji(id = '881810698185895946', name = "read")
            ),
            SelectOption(
                label = 'Music',
                value = 'Music ' + number,        
                description = 'Displays your favorite music',
                emoji = PartialEmoji(id = '881814177486864434', name = "kirbyvibe")
            ),
            SelectOption(
                label = 'Games',
                value = 'Games ' + number,        
                description = 'Displays your favorite game',
                emoji = PartialEmoji(id = '881816031474118686', name = "doggoshoot")
            ),
            SelectOption(
                label = 'Manga',
                value = 'Manga ' + number,        
                description = 'Displays your favorite manga',
                emoji = PartialEmoji(id = '881817241878921226', name = "manga")
            ),
            SelectOption(
                label = 'Show',
                value = 'Show ' + number,        
                description = 'Displays your favorite show',
                emoji = PartialEmoji(id = '881815997542203432', name = "netflix")
            ),
            SelectOption(
                label = 'Youtuber',
                value = 'Youtuber ' + number,        
                description = 'Displays your favorite Youtube content creator',
                emoji = PartialEmoji(id = '881800923331059712', name = "hype")
            ),
            SelectOption(
                label = 'Streamer',
                value = 'Streamer ' + number,        
                description = 'Displays your favorite Twitch streamer',
                emoji = PartialEmoji(id = '881820402542845972', name = "pepesaber")
            ),
        ]
    return options