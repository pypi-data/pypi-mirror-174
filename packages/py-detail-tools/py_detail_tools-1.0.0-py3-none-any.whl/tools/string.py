'''处理字符串相关的方法集合'''
import re
import enchant


class String(str):
    @staticmethod
    def cleanemoji(content):
        '''过滤表情符号'''
        pattern = re.compile(u'['u'\U0001F300-\U0001F64F' u'\U0001F680-\U0001F6FF' u'\u2600-\u2B55 \U00010000-\U0010ffff]+')
        return  re.sub(pattern, '', content)



    def split(self,pattern):
        '''正则分割字符串'''
        return re.split(pattern,self)



    @staticmethod
    def is_en_word(word):
        '''判断是否是正确单词'''
        d = enchant.Dict("en_US")
        return d.check(word)







