import markdown
from glob import glob



def get_posts():
    posts_path = 'posts/{}.md'
    posts = glob(posts_path.format('*'))
    blog_posts = []
    for i in range(len(posts)):
        post = {}
        file = open(posts_path.format(i), 'r')
        post["title"] = file.readline().strip()
        post["date"] = file.readline().strip()
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
    with open("posts_template.html", "r") as template:
        output = template.read().replace('<!-- POSTS -->', blog_posts)
        o = open("../posts.html", "w")
        o.write(output)
        o.close()
def html_format(blog_posts):
    html = '''<div class="flex light">'''
    for i in range(len(blog_posts)-1 , -1, -1):
        post = blog_posts[i]
        html += f'<div class="post" id="{post["link"]}"> {post["content"]} </div>'

    html += '\n</div>'
    
    return html
def recent_posts_html(blog_posts):
    html = "<ul>"
    posts_found = 0
    while(len(blog_posts) > 0 and posts_found < 5):
        post = blog_posts.pop()
        html += f'<li><a href="posts.html#{post["link"]}">{post["title"]}</a></li>'
        posts_found += 1
    html += "</ul>"
    return html

if __name__ == "__main__":
    blog_posts = get_posts()
    blog_posts_html = html_format(blog_posts)
    write_blog(blog_posts_html)
    recent_posts = recent_posts_html(blog_posts)
    write_index(recent_posts)

