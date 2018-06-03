from linebot.models import CarouselColumn
from linebot.models import CarouselTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage
from linebot.models import URITemplateAction

carousels = [{
    "id" : "menu_minsu",
    "payload" : TemplateSendMessage(
        alt_text='Menu Minsu',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/v2/carousel/zomato/indonesia.png',
                    title='MINSU',
                    text='Katalog Minsu',
                    actions=[
                        PostbackTemplateAction(
                            label='Pilih',
                            data='evt=katalog'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/v2/carousel/zomato/indonesia.png',
                    title='MINSU',
                    text='Order Minsu',
                    actions=[
                        PostbackTemplateAction(
                            label='Pilih',
                            data='evt=order'
                        )
                    ]
                )
            ]
        )
    )
}]

def composeCarousel(alt_text, columns):
    carousel_columns = []
    for column in columns:
        actions = []
        for action in column['actions']:
            if action['type'] == 'postback':
                actions.append(PostbackTemplateAction(label=action['label'], data=action['data']))
            elif action['type'] == 'message':
                actions.append(MessageTemplateAction(label=action['label'], text=action['text']))
            elif action['type'] == 'uri':
                actions.append(URITemplateAction(label=action['label'], uri=action['uri']))
        col = CarouselColumn(thumbnail_image_url=column['thumbnail_image_url'], title=column['title'], text=column['text'], actions=actions)
        carousel_columns.append(col)
    template = TemplateSendMessage(alt_text=alt_text, template=CarouselTemplate(columns=carousel_columns))
    return template