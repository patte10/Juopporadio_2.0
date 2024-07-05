# bot.pys
##pip install -U discord.py
##pip install beautifulsoup4
##pip install urllib3
import discord
from discord import Interaction, app_commands
from discord.ext import tasks, commands
from bs4 import BeautifulSoup
import urllib.request
import json
import random
import time
import logging

sup_radio_nimi_lista = ["kantri-radio","helmi-radio","groove-fm","classic-hits","easy-hits","aito-iskelma","hitmix","loop","radiorock","suomipop"]
yle_radio_nimi_lista = ["yle-radio","ylex","yle-radio-suomi","yle-vega","yle-klassinen","yle-sami","yle-x3m"]
url_radio_nimi_lista = ["https://yleradiolive.akamaized.net/hls/live/2027672/in-YleRadio1/master.m3u8"
                        ,"https://yleradiolive.akamaized.net/hls/live/2027674/in-YleX/master.m3u8"
                        ,"https://yleradiolive.akamaized.net/hls/live/2027675/in-YleRS/master.m3u8"
                        ,"https://yleradiolive.akamaized.net/hls/live/2027679/in-YleVega/master.m3u8"
                        ,"https://yleradiolive.akamaized.net/hls/live/2027676/in-YleKlassinen/master.m3u8"
                        ,"https://yleradiolive.akamaized.net/hls/live/2027680/in-YleSami/master.m3u8"
                        ,"https://yleradiolive.akamaized.net/hls/live/2027678/in-YleX3M/master.m3u8"]


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = Interaction.guild

bot = commands.Bot(command_prefix='!', intents=intents)
class GatewayEventFilter(logging.Filter):
    def __init__(self) -> None:
        super().__init__('discord.gateway')

    def filter(self, record: logging.LogRecord) -> bool:
        if record.exc_info is not None and isinstance(record.exc_info[1], discord.ConnectionClosed):
            return False
        return True

@client.event
async def on_ready():
        print(f'Logged on as {client.user}!')
        await client.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='/info'))
        try:
               synced = await tree.sync()
               print(f"syced {len(synced)} commands")
        except Exception as e:
               print(e)

@tree.command(name="ulkamaiset_kanavat",description="Täältä löydät kaikki ulkomaalaiset tällä hetkellä saatavilla oletvat radio kanavat")
@app_commands.choices(maa=[
    app_commands.Choice(name="Iso-britannia", value="UK"),
    ])

async def ulkamaiset_kanavat(interaction: discord.Interaction, maa: app_commands.Choice[str]):
    if maa.value == 'UK':
        html_doc= "https://hellorayo.co.uk/absolute-radio/play/"
        print('paper')
    elif maa.value == 'PL':
        html_doc= "https://www.rmfon.pl/play,5#p"
        print('scissors')  
    html = urllib.request.urlopen(html_doc)
    radio_sivun_lahdekoodi1 = BeautifulSoup(html, 'html.parser')
    global radio_sivun_lahdekoodi
    radio_sivun_lahdekoodi = radio_sivun_lahdekoodi1.prettify()
    #valikoi pelkän json tekstin
    radio_sivun_lahdekoodi= radio_sivun_lahdekoodi.split('<script id="__NEXT_DATA__" type="application/json">')[1]
    radio_sivun_lahdekoodi= radio_sivun_lahdekoodi.split('</script>')[0]


    #valikoi radio kanavien nimet
    global Ulkomaiset_radiokanava_lista
    radiokanava_lista = radio_sivun_lahdekoodi.split('"items":["')[1]
    radiokanava_lista= radiokanava_lista.split('],')[0]
    radiokanava_lista =radiokanava_lista.replace('"', '')
 
    radiokanava_lista = radiokanava_lista.split(",") 

    print(radiokanava_lista)
    

    Ulkomaiset_radiokanava_lista=radiokanava_lista
    Ulkomaiset_radiokanava_lista.sort()
    s = '\n'.join(Ulkomaiset_radiokanava_lista[:100])
    s2 = '\n'.join(Ulkomaiset_radiokanava_lista[100:])
    embed=discord.Embed(
    #luo embedin jossa on kaikki radio kanavat
        title=f"Tässä {maa.name}:n radiokanavat",

        description= s

        #add_field(name = "  ", value= s2, inline = True)
    )
    embed2=discord.Embed(
    #luo embedin jossa on kaikki radio kanavat
        description= s2

        #add_field(name = "  ", value= s2, inline = True)
    )

    await interaction.response.send_message(embeds=[embed,embed2]) 





def ulkomaiset_radio_kuutelu_lista(Kanavan_nimi):
    global h
    y = json.loads(radio_sivun_lahdekoodi)
    y = y["props"]
    y = y["initialState"]
    y = y["stationList"]
    y = y["stationsById"]
    h = y[Kanavan_nimi]
    y = h["stationStreams"]

    
    ##y["stationName"]
    liiitymis_lista= []
    naa = 0
    s=0
    while naa == 0:
       #tämä hakee kuinka montako radio kuuntelu linkkiä on
        try:
            #print(y[s]["streamUrl"])
            liiitymis_lista.append(y[s]["streamUrl"])

        except:
            naa = 2
        else:
            s += 1
            #print(s)
      
    liiitymis_lista.sort(reverse = True)
    #print(liiitymis_lista) 
    premium = 0 
    premium_lista = []
    #tämä hakee  onko listassa premium kanavia ja asettaa "premium =1" 
    for i in liiitymis_lista:

        if i.__contains__("prem"):
            premium = 1
            premium_lista.append(i) 
    for i in liiitymis_lista:

        if i.__contains__("premium"):
            premium = 1
            premium_lista.append(i)

    global botissa_soitettava_url
    if premium == 1:
        botissa_soitettava_url = premium_lista[random.randrange(0,len(premium_lista))]
        #print(botissa_soitettava_url)

    if premium == 0:
        botissa_soitettava_url = liiitymis_lista[-1]
        #print(botissa_soitettava_url)

            











     
 



def radio_lista():
    #hakee radio kanavan sivun netistä
    html_doc= "https://radioplay.fi/kanavat/"
    html = urllib.request.urlopen(html_doc)
    radio_sivun_lahdekoodi1 = BeautifulSoup(html, 'html.parser')
    global radio_sivun_lahdekoodi
    radio_sivun_lahdekoodi = radio_sivun_lahdekoodi1.prettify()
    #valikoi pelkän json tekstin
    radio_sivun_lahdekoodi= radio_sivun_lahdekoodi.split('<script id="__NEXT_DATA__" type="application/json">')[1]
    radio_sivun_lahdekoodi= radio_sivun_lahdekoodi.split('</script>')[0]


    #valikoi radio kanavien nimet
    global radiokanava_lista
    radiokanava_lista = radio_sivun_lahdekoodi.split('"items":["')[1]
    radiokanava_lista= radiokanava_lista.split('],')[0]
    radiokanava_lista =radiokanava_lista.replace('"', '')
 
    radiokanava_lista = radiokanava_lista.split(",") 

    print(radiokanava_lista)
    

    radiokanava_lista=radiokanava_lista + sup_radio_nimi_lista + yle_radio_nimi_lista
    radiokanava_lista.sort()

radio_lista()




def radio_kuutelu_lista(Kanavan_nimi):
    global h
    y = json.loads(radio_sivun_lahdekoodi)
    y = y["props"]
    y = y["initialState"]
    y = y["stationList"]
    y = y["stationsById"]
    h = y[Kanavan_nimi]
    y = h["stationStreams"]

    
    ##y["stationName"]
    liiitymis_lista= []
    naa = 0
    s=0
    while naa == 0:
       #tämä hakee kuinka montako radio kuuntelu linkkiä on
        try:
            #print(y[s]["streamUrl"])
            liiitymis_lista.append(y[s]["streamUrl"])

        except:
            naa = 2
        else:
            s += 1
            #print(s)
      
    liiitymis_lista.sort(reverse = True)
    #print(liiitymis_lista) 
    premium = 0 
    premium_lista = []
    #tämä hakee  onko listassa premium kanavia ja asettaa "premium =1"  
    for i in liiitymis_lista:

        if i.__contains__("premium"):
            premium = 1
            premium_lista.append(i)

    global botissa_soitettava_url
    if premium == 1:
        botissa_soitettava_url = premium_lista[random.randrange(0,len(premium_lista))]
        #print(botissa_soitettava_url)

    if premium == 0:
        botissa_soitettava_url = liiitymis_lista[-1]
        #print(botissa_soitettava_url)

            

radio_kuutelu_lista("iskelma")



@tree.command(name="kanavat",description="Täältä löydät kaikki tällä hetkellä saatavilla oletvat radio kanavat")
async def kanavat(interaction: discord.Interaction):

    s = '\n'.join(radiokanava_lista[:30])
    s2 = '\n'.join(radiokanava_lista[30:])
    embed=discord.Embed() 
    #luo embedin jossa on kaikki radio kanavat
    embed.add_field(name = "RADIO KANAVAT", value= s, inline = True)
    embed.add_field(name = "  ", value= s2, inline = True)

    



    await interaction.response.send_message(embed=embed ) 
      



class MyView(discord.ui.View):
    @discord.ui.button(label="❚❚", style=discord.ButtonStyle.red)
    async def pysayta_soitto(self,interaction: discord.Interaction,button: discord.ui.button, ):
            channel2.stop()
            await interaction.response.send_message(f'pysäytetään soittoa...')


    @discord.ui.button(label="▶", style=discord.ButtonStyle.green) 
    async def jatka_soitoa(self, interaction: discord.Interaction,button: discord.ui.button, ):
            channel2.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=kanavaurl))
            await interaction.response.send_message(f'jatketaan soittoa...')

@tree.command() 
async def soita( interaction: discord.Interaction, kanavan_nimi: str):
    ff =0
    global channel2 
    
    kanavan_nimi = str(kanavan_nimi).lower()

    try:
        if kanavan_nimi in sup_radio_nimi_lista:
            ff += 1
        elif kanavan_nimi in yle_radio_nimi_lista:
            ff += 2
            numero_lista =yle_radio_nimi_lista.index(kanavan_nimi)
        #yrittää hakea radio kanavan nimen radio kanava listastata
        elif ff == 0:
            radio_kuutelu_lista(kanavan_nimi)
    except:
         await interaction.response.send_message(f'Kanavaa nimeltä " {kanavan_nimi} " ei löytynyt kanvaluotetelosta!')
         return None

    try:
        member = interaction.guild.get_member(interaction.user.id)
        
        channel = member.voice.channel
    except:
         await interaction.response.send_message(f'Et ole puhekanavalla ')


    global kanavaurl
    try:
        channel2 = await channel.connect()
    except:
        print("botti onjo puhekanavalla")
    #luo radio kanavan url jossa on todennus avain
    if kanavan_nimi in sup_radio_nimi_lista:
        kanavaurl = "https://ms-live-"+kanavan_nimi.replace("-","" )+".nm-elemental.nelonenmedia.fi/master-256000.m3u8"
    if kanavan_nimi in yle_radio_nimi_lista:
        kanavaurl = url_radio_nimi_lista[numero_lista]
    elif ff == 0:   
        kanavaurl = botissa_soitettava_url+ "&aw_0_1st.d_a=true&aw_0_1st.bauer_loggedin=true&aw_0_1st.skey="+ str(round(int(time.time() * 1000)/ 1000)) ##str(random.randrange(1, 1000)).zfill(3)
    print(kanavaurl)
    try:
        
            channel2.stop()
    except:
        print("kanava on tyhjä")
    channel2.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=kanavaurl))

    if kanavan_nimi in sup_radio_nimi_lista:
        await interaction.response.send_message(f'Nyt soi {(kanavan_nimi.replace("-"," " )).capitalize()}  ', view=MyView())
    if kanavan_nimi in yle_radio_nimi_lista:
        await interaction.response.send_message(f'Nyt soi {(kanavan_nimi.replace("-"," " )).capitalize()}  ', view=MyView())
    elif ff == 0:
        await interaction.response.send_message(f'Nyt soi {h["stationName"]}  ', view=MyView())
   

@tree.command(name="stop",description="Täällä komennolla pysäytät botin soiton ")
async def stop(interaction: discord.Interaction):

    
    channel2.disconnect()
    await interaction.response.send_message(client.user.name +" poistui puhekanavalta!")  

@tree.command(name="info",description="Täällä komennolla näet kaikki botin komennot ja miten niitä kääytetään ")
async def info(interaction: discord.Interaction):
    embed=discord.Embed(title="/info") 
    #luo embedin jossa on kaikki radio kanavat
    
    embed.add_field(name = "/kanavat", value= "Tällä komennolla näet kaikki suomalaiset kanavat jotka ovat käytettävissä tällä hetkellä", inline = False)
    embed.add_field(name = "/soita ```kanavan_nimi``` --> kirjoita tämän jälkeen haluamasi radiokanavan nimi", value= "Tällä komennolla saat soitettua kaikkia radio kanavia jotka ovat saata villa tällä hetkellä", inline = False)
    embed.add_field(name = "/stop", value= "Tällä komennolla saat botin pois puhekanavalta", inline = False)
    embed.add_field(name = "/ulkamaiset_kanavat ```maa``` --> valitse tämän jälkeen haluamasi maan listan jonka radiokanavat haluat nähdä", value= "Tällä komennolla näet kaikki ulkomaalaiset kanavat jotka ovat käytettävissä tällä hetkellä", inline = False)
    await interaction.response.send_message(embed=embed )


client.run("token")
