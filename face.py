# -*- coding: utf-8 -*-
from jinja2 import Environment, BaseLoader
import os
import codecs

class MyLoader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with file(path) as f:
            source = f.read().decode('utf-8')
        return source, path, lambda: mtime == os.path.getmtime(path)

def render_stuff(template_path=None, output_path=None):
    if not template_path:
        template_path = os.getcwd() + '/templates'
    if not output_path:
        output_path = os.getcwd() + '/rendered_website'
    env = Environment(loader=MyLoader('templates'))
    all_the_things = os.walk(template_path)
    for root, dirs, files in all_the_things:
        for f in files:
            if f[-5:] == '.html' and f[:1] != '_':
                full_path = root + '/' + f
                relative_path = full_path[len(template_path) + 1:]
                print "Rendering " + relative_path
                template = env.get_template(relative_path)
                print template
                dirname = os.path.dirname(output_path + '/' + relative_path)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                with codecs.open(output_path + '/' + relative_path, 'w', 'utf-8') as render_file:
                    for line in template.render():
                        render_file.write(line)