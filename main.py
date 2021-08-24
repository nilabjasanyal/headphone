
from flask import Flask, render_template, send_file, logging

from pytube import Channel,YouTube

app = Flask(__name__)



def details(url):
    yt = YouTube(url=url)
    min, sec = divmod(yt.length, 60)
    hour, min = divmod(min, 60)
    #       0(title)          1(runtime)                  2(image url)      3(description)
    return [yt.title, "%02d min %02d sec" % (min, sec), yt.thumbnail_url,  yt.description]

length = 0
dict_url={}
def get_dict(a):
    global length
    url_dict={}
    c = Channel('https://www.youtube.com/channel/UCS7S4NlE1SIjztaGzcHN0vQ')
    length = len(c.video_urls)
    print(length)
    for url in c.video_urls[:a]:
        info =  details(url)
        url_dict[url]=info

    return url_dict

# print(url_dict)

# yt = YouTube('https://www.youtube.com/watch?v=OfvpQRuizN4')
# video = yt.streams.filter(res="720p").first()
# video.download(r'~/Downloads')



@app.route('/')
def home():

    return render_template("index.html")
n=4
@app.route('/downloadpage')
def download_page():
    global dict_url
    global n
    n=4
    dict_url = get_dict(4)
    return render_template("table.html", url_dict=dict_url)

@app.route('/downloadpage_clip_increment')
def clip_increment():
    global dict_url
    global n
    n+=3
    if n > length:
        d= n-length
        n-=d
    dict_url = get_dict(n)
    return render_template("table.html", url_dict=dict_url)



@app.route('/about_us')
def about_us():
    return render_template("hero.html")

@app.route('/clips/<title>')
def clip_info(title):        #line 88 on table.html
    for link in dict_url:
        if dict_url[link][0]==title:
            image_url = dict_url[link][2]
            description = dict_url[link][3]

    return render_template("clips.html", title = title, description = description , image_url = image_url)
# DOWNLOADING THE VIDEO
@app.route('/download_video/<title>')
def download_video(title):
    for link in dict_url:
        if dict_url[link][0] == title:
            url = link
            download_path = YouTube(url=url).streams.filter(res="720p",file_extension="mp4").first()
            DOWNLOAD = download_path.download()
            fname = DOWNLOAD.split('//')[-1]

            return send_file(fname, as_attachment=True)
    # return render_template('index.html')


# @app.route('/<date>')
# def details(date):
#     # return date
#     return render_template("post.html",det=response.json()['articles'],d=date)

if __name__ == "__main__":
    app.run(debug=True)


