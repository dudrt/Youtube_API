from flask import Flask, send_file, request
from pytube import YouTube
import requests
import json
import os
import shutil

developer_key = os.environ['developer_key']
DEVELOPER_KEY = developer_key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

app = Flask(__name__)
key = os.environ['key']


def delete_audio():
  if os.path.exists("audio"):
    shutil.rmtree('audio')
    print("Pasta Deletada.")
  else:
    print("Pasta não existente.")
    
delete_audio()


@app.route('/')
def index():
  return 'Olá, a API está funcionando!'


@app.route('/<parametros>')
def buscar_parametros(parametros):
  url = f'https://www.googleapis.com/youtube/v3/search?q={parametros}&part=snippet&key={key}&type=video&maxResults=10'

  # Fazer a solicitação GET
  a = requests.get(url)
  response = a.json()

  videos = []
  
  for i in range(10):
    # Extrair os campos desejados
    video_id = response["items"][i]["id"]["videoId"]
    channel_title = response["items"][i]["snippet"]["channelTitle"]
    thumbnail = response["items"][i]["snippet"]["thumbnails"]["medium"]["url"]
    title = response["items"][i]["snippet"]["title"]

    item ={"Thumbnail":thumbnail,
               "Canal":channel_title,
               "Titulo":title,
               "VideoId":video_id}

    videos.append(item)

  json_str = json.dumps({"videos":videos}, indent=2)
  return json_str

@app.route('/getids')
def getids():
  try:
    url_completa = request.url
    url_baixar = url_completa.split("?")
    yt = YouTube(f"{url_baixar[1]}")
    retornar = str(yt.streams.filter(only_audio=True))
    apoio = retornar.split(",")
    videos =[]
    for i in range(len(apoio) - 1):
      separar = apoio[i].split("Stream:")[1]
      id = separar.split("=")[1].split(" ")[0].split('"')[1]
      qualidade = separar.split("=")[3].split(" ")[0].split('"')[1]
      
      item ={"ID":id,
            "Qualidade":qualidade}
    
      videos.append(item)
  
    json_str = json.dumps({"IDs":videos}, indent=2)
  
    return json_str
  except Exception as e:
    print(e)
    return "Erro"


@app.route('/down/<id>')
def download(id):
  try:
    url_completa = request.url
    url_baixar = url_completa.split("?")[1]
    yt = YouTube(f"{url_baixar}")
    stream = yt.streams.get_by_itag(id)
    titulo = stream.title[:10] + ".mp3"
    print(titulo)
    stream.download(output_path='audio', filename=titulo)
    
    return send_file("audio/" + titulo, mimetype='audio/mp3')
  except Exception as e:
    print(e)
    return "Erro"
    
@app.route('/downalto')
def download_alto():
  try:
    url_completa = request.url
    url_baixar = url_completa.split("?")[1]
    print(url_completa)
    yt = YouTube(f"{url_baixar}")
    # Tenta baixar o audio na qualidade desejada.
    try:
      stream = yt.streams.get_by_itag(140)
    # Caso não exista a opção, baixa na menor qualidade.(100%)
    except:
      stream = yt.streams.get_by_itag(139)
  
    titulo = f"{stream.title}.mp3"
    titulo = stream.title[:10] + ".mp3"
    print(titulo)
  
    stream.download(output_path='audio', filename=titulo)
    
    return send_file("audio/" + titulo, mimetype='audio/mp3')
    
  except Exception as e:
    print(e)
    return "Erro"

@app.route('/downmedio')
def download_medio():
  try:
    url_completa = request.url
    url_baixar = url_completa.split("?")[1]
    print(url_completa)
    yt = YouTube(f"{url_baixar}")
    # Tenta baixar o audio na qualidade desejada.
    try:
      stream = yt.streams.get_by_itag(250)
    # Caso não exista a opção, baixa na menor qualidade.(100%)
    except:
      stream = yt.streams.get_by_itag(139)
    
    titulo = f"{stream.title}.mp3"
    titulo = stream.title[:10] + ".mp3"
    print(titulo)
  
    stream.download(output_path='audio', filename=titulo)
    
    return send_file("audio/" + titulo, mimetype='audio/mp3')
    
  except Exception as e:
    print(e)
    return "Erro"

@app.route('/downbaixo')
def download_baixo():
  try:  
    url_completa = request.url
    url_baixar = url_completa.split("?")[1]
    print(url_completa)
    yt = YouTube(f"{url_baixar}")
    stream = yt.streams.get_by_itag(139)
    titulo = f"{stream.title}.mp3"
    titulo = stream.title[:10] + ".mp3"
    print(titulo)

    stream.download(output_path='audio', filename=titulo)
  
    return send_file("audio/" + titulo, mimetype='audio/mp3')
  except Exception as e:
    print(e)
    return "Erro"


@app.route('/teste')
def teste():
  yt = YouTube("www.youtube.com/watch?v=69sw2G79Tb8")
  retornar = str(yt.streams.filter(progressive=True))

  return retornar


app.run(host='0.0.0.0', port=81)
