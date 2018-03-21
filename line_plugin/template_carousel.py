from linebot.models import CarouselColumn
from linebot.models import CarouselTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage
from linebot.models import URITemplateAction

carousels = [{
    "id" : "tampil_kelas",
    "payload" : TemplateSendMessage(
        alt_text='Tampil Kelas',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://image.winudf.com/v2/image/Y29tLnNvbGl0ZWtpZHMuY2VyZGFzY2VybWF0c2RfaWNvbl8xNTE0MDAyOTc4XzAwNw/icon.png?w=170&fakeurl=1&type=.png',
                    title='SD',
                    text='Sekolah Dasar',
                    actions=[
                        PostbackTemplateAction(
                            label='SD Kelas 1',
                            data='evt=pilih_kelas&kelas=SD%20Kelas%201'
                        ),
                        PostbackTemplateAction(
                            label='SD Kelas 2',
                            data='evt=pilih_kelas&kelas=SD%20Kelas%202'
                        ),
                        PostbackTemplateAction(
                            label='SD Kelas 3',
                            data='evt=pilih_kelas&kelas=SD%20Kelas%203'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://image.winudf.com/v2/image/Y29tLnNvbGl0ZWtpZHMuY2VyZGFzY2VybWF0c2RfaWNvbl8xNTE0MDAyOTc4XzAwNw/icon.png?w=170&fakeurl=1&type=.png',
                    title='SD',
                    text='Sekolah Dasar',
                    actions=[
                        PostbackTemplateAction(
                            label='SD Kelas 4',
                            data='evt=pilih_kelas&kelas=SD%20Kelas%204'
                        ),
                        PostbackTemplateAction(
                            label='SD Kelas 5',
                            data='evt=pilih_kelas&kelas=SD%20Kelas%205'
                        ),
                        PostbackTemplateAction(
                            label='SD Kelas 6',
                            data='evt=pilih_kelas&kelas=SD%20Kelas%206'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://image.winudf.com/v2/image/Y29tLnNvbGl0ZWtpZHMuY2VyZGFzY2VybWF0c21wX2ljb25fMTUxMzk5MTk2MF8wNDU/icon.png?w=170&fakeurl=1&type=.png',
                    title='SMP',
                    text='Sekolah Menengah Pertama',
                    actions=[
                        PostbackTemplateAction(
                            label='SMP Kelas VII',
                            data='evt=pilih_kelas&kelas=SMP%20Kelas%20VII'
                        ),
                        PostbackTemplateAction(
                            label='SMP Kelas VIII',
                            data='evt=pilih_kelas&kelas=SMP%20Kelas%20VIII'
                        ),
                        PostbackTemplateAction(
                            label='SMP Kelas IX',
                            data='evt=pilih_kelas&kelas=SMP%20Kelas%20IX'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://lh3.googleusercontent.com/OVNH8_WcT9ntciHgybzbv5gJa_6Ht01WzyErrrOWPua1o-ecV2Af5jH9yanVYX757snj=w168',
                    title='SMA',
                    text='Sekolah Menengah Atas',
                    actions=[
                        PostbackTemplateAction(
                            label='SMA Kelas X',
                            data='evt=pilih_kelas&kelas=SMA%20Kelas%20X'
                        ),
                        PostbackTemplateAction(
                            label='SMA Kelas XI',
                            data='evt=pilih_kelas&kelas=SMA%20Kelas%20XI'
                        ),
                        PostbackTemplateAction(
                            label='SMA Kelas XII',
                            data='evt=pilih_kelas&kelas=SMA%20Kelas%20XII'
                        )
                    ]
                )
            ]
        )
    )
},{
    "id" : "menu_rogu",
    "payload" : TemplateSendMessage(
        alt_text='Menu Belajar',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://cdn6.aptoide.com/imgs/7/b/5/7b5006b117500673beb188a6386de6fc_icon.png?w=240',
                    title='Ruang Guru',
                    text='Mau Pilih Mana Nih ?',
                    actions=[
                        PostbackTemplateAction(
                            label='Belajar Seru',
                            data='evt=pilih_menu&menu=belajar'
                        ),
                        PostbackTemplateAction(
                            label='Tryout Seru',
                            data='evt=pilih_menu&menu=tryout'
                        )
                    ]
                )
            ]
        )
    )
},{
    "id" : "menu_bljr_mapel",
    "payload" : TemplateSendMessage(
        alt_text='Menu Belajar Mapel',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://lh3.googleusercontent.com/Z8syQw3bCR1k26M7w1FSOxZDqPA-0cW5HdKQwpsGnpzihnQdVzG6lFIVtC6Gpd7c7-T1=w168',
                    title='Mata Pelajaran',
                    text='Mau Belajar Apa Nih ?',
                    actions=[
                        PostbackTemplateAction(
                            label='Matematika',
                            data='evt=pilih_bljr_mapel&mapel=matematika'
                        ),
                        PostbackTemplateAction(
                            label='Bahasa Indonesia',
                            data='evt=pilih_bljr_mapel&mapel=bahasa%20indonesia'
                        ),
                        PostbackTemplateAction(
                            label='Bahasa Inggris',
                            data='evt=pilih_bljr_mapel&mapel=bahasa%20inggris'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://lh3.googleusercontent.com/Z8syQw3bCR1k26M7w1FSOxZDqPA-0cW5HdKQwpsGnpzihnQdVzG6lFIVtC6Gpd7c7-T1=w168',
                    title='Mata Pelajaran',
                    text='Mau Belajar Apa Nih ?',
                    actions=[
                        PostbackTemplateAction(
                            label='Fisika',
                            data='evt=pilih_bljr_mapel&mapel=fisika'
                        ),
                        PostbackTemplateAction(
                            label='Kimia',
                            data='evt=pilih_bljr_mapel&mapel=kimia'
                        ),
                        PostbackTemplateAction(
                            label='Biologi',
                            data='evt=pilih_bljr_mapel&mapel=biologi'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://lh3.googleusercontent.com/Z8syQw3bCR1k26M7w1FSOxZDqPA-0cW5HdKQwpsGnpzihnQdVzG6lFIVtC6Gpd7c7-T1=w168',
                    title='Mata Pelajaran',
                    text='Mau Belajar Apa Nih ?',
                    actions=[
                        PostbackTemplateAction(
                            label='Sejarah',
                            data='evt=pilih_bljr_mapel&mapel=sejarah'
                        ),
                        PostbackTemplateAction(
                            label='Ekonomi',
                            data='evt=pilih_bljr_mapel&mapel=ekonomi'
                        ),
                        PostbackTemplateAction(
                            label='Others',
                            data='evt=pilih_bljr_mapel&mapel=others'
                        )
                    ]
                )
            ]
        )
    )
},{
    "id" : "topik_matematika",
    "payload" : TemplateSendMessage(
        alt_text='Matematika',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://icon-icons.com/icons2/1194/PNG/512/1490886309-15-formula_82482.png',
                    title='Pelajaran Matematika',
                    text='Mau Belajar Apa Nih ?',
                    actions=[
                        PostbackTemplateAction(
                            label='FPB dan KPK',
                            data='evt=pilih_topik_mapel&topik=fpb%20fpk'
                        ),
                        PostbackTemplateAction(
                            label='Aljabar',
                            data='evt=pilih_topik_mapel&topik=aljabar'
                        ),
                        PostbackTemplateAction(
                            label='Pecahan',
                            data='evt=pilih_topik_mapel&topik=pecahan'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://icon-icons.com/icons2/1194/PNG/512/1490886309-15-formula_82482.png',
                    title='Mata Pelajaran',
                    text='Mau Belajar Apa Nih ?',
                    actions=[
                        PostbackTemplateAction(
                            label='Bangun Datar',
                            data='evt=pilih_topik_mapel&topik=bangun%20datar'
                        ),
                        PostbackTemplateAction(
                            label='Bangun Ruang',
                            data='evt=pilih_topik_mapel&topik=bangun%20ruang'
                        ),
                        PostbackTemplateAction(
                            label='Phytagoras',
                            data='evt=pilih_topik_mapel&topik=phytagoras'
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