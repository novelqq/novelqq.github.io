from markdown import markdown
from glob import glob


blog_posts = []

def get_posts():
    posts_path = 'posts/{}.md'
    posts = glob(posts_path.format('*'))
    
    for i in range(len(posts)):
        file = open(posts_path.format(i), 'r')
        title = file.readline().strip()
        content = markdown(file.read().strip())
        blog_posts.append({"title": title, "content": content}) 
        file.close()
    return


def write_html():
    with open("template.html", "r") as template:
        output = template.read().replace('<!-- CONTENT -->', content)
         
