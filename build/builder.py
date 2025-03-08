import markdown
import requests
import re

from glob import glob
with open("secret.txt", "r") as f:
    api_key = f.read().rstrip()
api_url = "https://www.flickr.com/services/rest/?method=flickr.photosets.getPhotos&api_key="+api_key + \
    "&photoset_id=72177720317830969&user_id=49734374%40N07&extras=url_m,url_o&format=json&nojsoncallback=1"


def get_posts():
    posts_path = 'posts/{:02}.md'
    posts = glob(posts_path.format('**'))
    blog_posts = []
    for i in range(len(posts)):
        post = {}
        file = open(posts_path.format(i), 'r')
        post["title"] = file.readline().strip()
        post["date"] = file.readline().strip()
        post["thumb"] = file.readline().strip()
        post["tags"] = file.readline().strip().split(" ")
        post["content"] = markdown.markdown(file.read())
        post["link"] = post["title"].replace(" ", "_")
        blog_posts.append(post)
        file.close()
    return blog_posts


def write_index(new_posts):
    with open("index_template.html", "r") as template:
        output = template.read().replace('<!-- NEWPOSTS -->', new_posts)
        o = open("../index.html", "w")
        o.write(output)
        o.close()


def write_blog(blog_posts):
    with open("posts_list_template.html", "r") as template:
        output = template.read().replace('<!-- POSTS -->', blog_posts)
        o = open("../posts.html", "w")
        o.write(output)
        o.close()


def format_list(blog_posts):
    html = '''<div class="flex light"><ul>'''
    for post in blog_posts:
        html += f'<li class="blog-li"><a href="posts/{post["link"]}.html">{post["title"]} - {post["date"]}</a></li>\n'

    html += '</ul></div>'
    return html


def write_blogs(blog_posts):
    for i in range(len(blog_posts)):
        post = blog_posts[i]
        next_post = "../posts.html"
        prev_post = "../posts.html"
        if i > 0:
            prev_post = blog_posts[i-1]["link"]+'.html'
        if i < len(blog_posts) - 1:
            next_post = blog_posts[i+1]["link"]+'.html'

        with open("posts_template.html", "r") as template:
            output = template.read().replace('<!-- POSTS -->', html_format(post)).replace('<!-- NEXT -->', next_post).replace('<!-- PREV -->',
                                                                                                                              prev_post).replace('<!-- METATITLE -->', post["title"]).replace('<!-- METAIMG -->', post["thumb"])
            o = open(f'../posts/{post["title"].replace(" ","_")}.html', 'w')
            o.write(output)
            o.close()


def write_highlights(gallery):
    with open("highlights_template.html", "r") as template:
        output = template.read().replace('<!-- GALLERY -->', gallery)
        o = open("../highlights.html", "w")
        o.write(output)
        o.close()


def add_click_to_images(html_string):
    img_pattern = r'(<img[^>]+src=["\']([^"\']+)["\'][^>]*>)'

    def modify_img_tag(match):
        img_tag = match.group(1)
        src = match.group(2)

        modified_img_tag = img_tag.replace(
            f'src="{src}"', f'src="{src}" @click="openModal(\'{src}\')"')

        return modified_img_tag

    modified_html = re.sub(img_pattern, modify_img_tag, html_string)

    return modified_html


def html_format(post):
    html = '''<div class="flex light">'''
    html += f'<div class="post" id="{post["link"]}"> {post["content"]} </div>'
    html += '\n</div>'
    html = add_click_to_images(html)
    return html


def recent_posts_html(blog_posts):
    html = "<ul>"
    posts_found = 0
    while len(blog_posts) > 0 and posts_found < 5:
        post = blog_posts.pop()
        html += f'<li><a href="posts/{post["link"]}.html">{post["title"]}</a></li>'
        posts_found += 1
    html += "</ul>"
    return html


def make_gallery():
    photos = []
    response = requests.get(api_url).json()
    for photo in response["photoset"]["photo"]:
        new_photo = {
            "url":  "https://flickr.com/photos/49734374@N07/" + photo["id"],
            "thumb": photo["url_m"],
            "img": photo["url_o"]
        }
        photos.append(new_photo)
    html = "<ul class=\"image-gallery\">"
    for photo in photos:
        html += f'<li class="gallery-li"><img @click="openModal(\'{photo["img"]}\')" class="gallery-img" src="{photo["thumb"]}" /></a></li>'
    html += "</ul>"
    return html


# def make_3d_gallery():
# from os import listdir
#   from os.path import isfile, join
#   models = [f for f in listdir("../public/models/")
#             if isfile(join("../public/models/", f))]
#   for model in models:


if __name__ == "__main__":
    blog_posts = get_posts()
    write_blog(format_list(blog_posts))
    write_blogs(blog_posts)
    recent_posts = recent_posts_html(blog_posts)
    write_index(recent_posts)
    write_highlights(make_gallery())
