import markdown
from glob import glob



def get_posts():
    posts_path = 'posts/{}.md'
    posts = glob(posts_path.format('*'))
    blog_posts = []
    for i in range(len(posts)):
        file = open(posts_path.format(i), 'r')
        data = file.read().strip()
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(data)
        print(md.Meta)
        blog_posts += f"<li><a href=\"posts/{i}\">{title}</li>\n"
        print(blog_posts)
        file.close()
    return blog_posts


def write_html(blog_posts_html):
    with open("template.html", "r") as template:
        output = template.read().replace('<!-- CONTENT -->', blog_posts_html )
        o = open("../index.html", "w")
        o.write(output)
        o.close()
        return

def create_index():
    pass

def create_post_pages():
    pass

def 
if __name__ == "__main__":
    blog_posts_html = get_posts()
    write_html(blog_posts_html)
