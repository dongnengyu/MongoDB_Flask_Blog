import markdown2
import codecs


def main():
    md_name = "/Users/xiaomu/Documents/MyBlog/source/_posts/MWeb/Markdown 语法和 MWeb 写作使用说明.md"

    with codecs.open(md_name, mode='r', encoding='utf-8') as mdfile:
        with codecs.open("/Users/xiaomu/PycharmProjects/MongoDB/friendly.css", mode='r', encoding='utf-8') as cssfile:
            md_text = mdfile.read()
            css_text = cssfile.read()

            extras = ['code-friendly', 'fenced-code-blocks', 'footnotes']
            html_text = markdown2.markdown(md_text, extras=extras)

            html_name = '%s.html' % (md_name[:-3])
            with codecs.open(html_name, 'w', encoding='utf-8', errors='xmlcharrefreplace') as output_file:


                with codecs.open("/Users/xiaomu/PycharmProjects/MongoDB/end.css", mode='r',
                                 encoding='utf-8') as cssfile:
                    end_text = cssfile.read()

                output_file.write(css_text + html_text +end_text)
                print(css_text + html_text +end_text)


if __name__ == '__main__':
    main()
