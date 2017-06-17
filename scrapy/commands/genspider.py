#-*- coding:utf-8 –*-
from __future__ import print_function
import os
import shutil
import string

from importlib import import_module
from os.path import join, dirname, abspath, exists, splitext

import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.utils.template import render_templatefile, string_camelcase
from scrapy.exceptions import UsageError

# 自动重命名模块名
def sanitize_module_name(module_name):
    """Sanitize the given module name, by replacing dashes and points
    with underscores and prefixing it with a letter if it doesn't start
    with one
    """
    module_name = module_name.replace('-', '_').replace('.', '_')
    if module_name[0] not in string.ascii_letters:
        module_name = "a" + module_name
    return module_name

# 构建爬虫spider文件的
class Command(ScrapyCommand):

    requires_project = False
    default_settings = {'LOG_ENABLED': False}

    def syntax(self):
        return "[options] <name> <domain>"

    def short_desc(self):
        return "Generate new spider using pre-defined templates"

	  # 执行scrapy genspider可以查看该命令
    # --list表示显示所有可用的模板
    # --template表示使用指定模板，默认是basic类型的模板
    # --force表示覆盖掉以前的spider
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-l", "--list", dest="list", action="store_true",
            help="List available templates")
        parser.add_option("-e", "--edit", dest="edit", action="store_true",
            help="Edit spider after creating it")
        parser.add_option("-d", "--dump", dest="dump", metavar="TEMPLATE",
            help="Dump template to standard output")
        parser.add_option("-t", "--template", dest="template", default="basic",
            help="Uses a custom template.")
        parser.add_option("--force", dest="force", action="store_true",
            help="If the spider already exists, overwrite it with the template")

    def run(self, args, opts):
        if opts.list:
            self._list_templates()
            return
        if opts.dump:
            template_file = self._find_template(opts.dump)
            if template_file:
                with open(template_file, "r") as f:
                    print(f.read())
            return
        if len(args) != 2:
            raise UsageError()

        name, domain = args[0:2]
        module = sanitize_module_name(name)
        
        # 爬虫名字不能与项目名字相同
        if self.settings.get('BOT_NAME') == module:
            print("Cannot create a spider with the same name as your project")
            return

        try:
            spidercls = self.crawler_process.spider_loader.load(name)
        except KeyError:
            pass
        else:
            # if spider already exists and not --force then halt
            if not opts.force:
                print("Spider %r already exists in module:" % name)
                print("  %s" % spidercls.__module__)
                return
        template_file = self._find_template(opts.template)
        if template_file:
            self._genspider(module, name, domain, opts.template, template_file)
            if opts.edit:
                self.exitcode = os.system('scrapy edit "%s"' % name)
    
    # 根据给定的模板信息生成spider爬虫文件
    def _genspider(self, module, name, domain, template_name, template_file):
        """Generate the spider module, based on the given template"""
        tvars = {
            'project_name': self.settings.get('BOT_NAME'),
            'ProjectName': string_camelcase(self.settings.get('BOT_NAME')),
            'module': module,
            'name': name,
            'domain': domain,
            'classname': '%sSpider' % ''.join(s.capitalize() \
                for s in module.split('_'))
        }
        if self.settings.get('NEWSPIDER_MODULE'):
            spiders_module = import_module(self.settings['NEWSPIDER_MODULE'])
            spiders_dir = abspath(dirname(spiders_module.__file__))
        else:
            spiders_module = None
            spiders_dir = "."
        spider_file = "%s.py" % join(spiders_dir, module)
        # 从元template_file复制到spider_file文件去
        shutil.copyfile(template_file, spider_file)
        render_templatefile(spider_file, **tvars)
        print("Created spider %r using template %r " % (name, \
            template_name), end=('' if spiders_module else '\n'))
        if spiders_module:
            print("in module:\n  %s.%s" % (spiders_module.__name__, module))

    # 在指定位置查找相应模板
    def _find_template(self, template):
        template_file = join(self.templates_dir, '%s.tmpl' % template)
        if exists(template_file):
            return template_file
        print("Unable to find template: %s\n" % template)
        print('Use "scrapy genspider --list" to see all available templates.')

    # 显示所有可用的spider模板，模板存放在templates\spiders路径下，以.tmpl结尾
    def _list_templates(self):
        print("Available templates:")
        for filename in sorted(os.listdir(self.templates_dir)):
            if filename.endswith('.tmpl'):
                print("  %s" % splitext(filename)[0])

    # 如果TEMPLATES_DIR的值为空，那么_templates_base_dir就是scrapy的path与templates拼接成的路径。
    @property
    def templates_dir(self):
        _templates_base_dir = self.settings['TEMPLATES_DIR'] or \
            join(scrapy.__path__[0], 'templates')
        return join(_templates_base_dir, 'spiders')
