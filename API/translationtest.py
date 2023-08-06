from translate import Translator
def translation(text,des):

    translator = Translator(to_lang=des)

    result = translator.translate(text)
    #(result)
    return result


