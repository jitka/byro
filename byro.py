#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Clever assistant for each bureaucrat.
"""

import os
import locale
from byro.bredmine import BRedmine
from byro.vycetka import (Cmd, DocX)
from byro.sign import PdfSign
from byro.convertor import Convertor
from byro.configargparse import ByroParse
from byro.mail import Mail


__author__ = ['Ondřej Profant', 'Jakub Michálek']
__dir__ = os.path.realpath(os.path.dirname(__file__))


class App:

    def __init__(self):
        self.arg_parser = None
        self.args = None

    def _parse_args(self):

        subcommands = ["pdf", "sign", "vycetka", "save", "mail", "ds", "ocr", "args"]

        p = ByroParse(
            subcommands,
            default_config_files=['files/config.ini', os.path.expanduser('~') + "/.byro.ini"],
            description=__doc__,
            epilog=str(__author__)
        )

        p.add('-c', '--config', is_config_file=True,  help='config file path')
        p.add('-g', '--gui', type=bool, help="")
        p.add('-l', '--locale',   help="")
        p.add('-o', '--out',      help="Output file name")

        vyc = p.add_argument_group('Vycetka', "Generates \"vycetka\" for Prague City Hall.")
        vyc.add(      '--url',      help="Target Redmine url.")
        vyc.add('-p', '--project',  help="Redmine project name.")
        vyc.add('-y', '--year',     help="Values: this, last, 2014, 2015, ...")
        vyc.add('-m', '--month',    help="Values: this, last, leden, únor, ..., prosinec, 1, ..., 12. Determinate by localization.")
        vyc.add('-u', '--user',     help="Redmine user nickname or id.")

        sign = p.add_argument_group('Sign', "Digital sign of pdf file.")
        sign.add('-k', '--sign-key', help="Path to the key.pfx")
        sign.add(	    '--sign-bin', help="Path to the jPdfSign" )
        sign.add('-V', '--sign-visible', type=bool, help="")
        sign.add(	    '--sign-reason', help="" )
        sign.add(	    '--sign-location', help="" )
        sign.add(	    '--sign-contact', help="" )

        pdf = p.add_argument_group('Pdf', "Convert markdown into pdf via Pandoc.")
        pdf.add(      '--pandoc-bin', help="Path to pandoc binary.")
        pdf.add(      '--tex-bin',  help="")
        pdf.add('-t', '--template', help="Path to XeLaTeX template.")

        mail = p.add_argument_group('Mail', "Send mass mails, body is markdown file, list of recipients is file")
        mail.add("-r", "--recipients", help="Email, or path to text file with recipients divided by newline.")
        mail.add("-f", "--frm",       help="Sender email address.")
        mail.add("--login", help="Email login")
        mail.add("--server", help="Email server")

        ds = p.add_argument_group('Ds')
        ds.add(      '--ds-id', help="")

        p.add_argument('inputs', metavar='input files', nargs='*', help='Input files')

        self.arg_parser = p
        self.args = p.parse_args()

    def _before_run(self):
        locale.setlocale(locale.LC_ALL, self.args.locale)

    def pdf(self):
        convertor = Convertor(self.args.pandoc_bin)
        #TODO: gives real filename
        convertor.convert(self.args.inputs)

    def vycetka(self):
        redmine = BRedmine(self.args.user, self.args.url, self.args.project, self.args.month)
        data = redmine.get_data()
        # data.export_to_bin_file("data-6-OP.p")
        docx = DocX(data, self.args.out)
        docx.show()

    def sign(self):
        sign = PdfSign(self.args.sign_bin, self.args.sign_key)
        sign.sign(self.args.inputs)

    def mail(self):

        mail = Mail(self.args.login, self.args.frm,
                    recipients=[self.args.recipients],
                    body=self.args.inputs,
                    server=self.args.server)
        mail.send()

    def ocr(self):
        from PIL import Image
        import pytesseract
        text = ""
        for file in self.args.inputs:
            try:
                img = Image.open(file)
            except OSError:
                print("Only image can be OCR. For pdf use:\npdftocairo -jpeg <file>.pdf")
                exit()
            text += pytesseract.image_to_string(img, lang="ces")

        if self.args.out:
            with open(self.args.out, "w") as f:
                f.write(text)
        else:
            print(text)

    def args_test(self):
        print(self.args)
        print(__dir__ + '/files/config.ini')

    def main(self):

        self._parse_args()

        self._before_run()

        c = self.args.command

        if c == 'args':
            self.args_test()
        elif c == "pdf":
            self.pdf()
        elif c == "ocr":
            self.ocr()
        elif c == "sign":
            self.sign()
        elif c == "mail":
            self.mail()
        elif c == "vycetka":
            self.vycetka()
        else:
            self.arg_parser.print_help()

if __name__ == "__main__":
    App().main()
