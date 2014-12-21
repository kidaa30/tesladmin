import os, subprocess, re, textwrap, datetime
from django.core.exceptions import ValidationError
from django.contrib import admin, messages
from django.conf import settings
from .models import Post
import os

regex = re.compile(r'\.\. slug: (.*)\n\.\. date: (.*)')
getn = re.compile(r"Your post's text is at: (.+)")

def reformat_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S %Z')\
                            .strftime('%Y-%m-%d %H:%M:%S%z')

class Runner():
    def __init__(self, request):
        if settings.DEBUG:
            self.workdir = os.path.join(os.getcwd(), 'static')
        else:
            self.workdir = settings.STATIC_ROOT
        self.request = request

    def run(self, cmd):
        try:
            res = subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                               cwd=self.workdir)
            if 'ERROR' in res:
                messages.error(self.request,
                               'error while running nikola: %s' % res)
            return
        except subprocess.CalledProcessError as ex:
            messages.error(self.request,
                           'error while running nikola: %s' % ex.output)
            return

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('path', 'date', 'slug')

    def save_model(self, request, obj, form, change):
        r = Runner(request)
        if obj.path == '':
            out = r.run(['nikola', 'new_post', '-t', obj.title])
            if out is None: return
            obj.path = os.path.join(r.workdir, getn.search(out).group(1))
            with open(obj.path, 'r') as f:
                data = f.read()
                m = regex.search(data)
                assert m
                obj.slug = m.group(1)
                obj.date = reformat_date(m.group(2))
        text = textwrap.dedent('''
        .. title: %s
        .. slug: %s
        .. date: %s
        .. tags: %s
        .. type: text

        %s
        '''.lstrip('\n') % (obj.title, obj.slug, obj.date, obj.tags, obj.text))
        with open(obj.path, 'w') as f:
            f.write(text)
        if r.run(['nikola', 'build']) is None: return
        obj.save()

    def delete_model(self, request, obj):
        r = Runner(request)
        os.remove(obj.path)
        assert r.run(['nikola', 'build'])
        obj.delete()

admin.site.register(Post, PostAdmin)
