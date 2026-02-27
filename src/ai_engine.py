import random

def generate_script(niche):
    templates = {
        'motivasi': {
            'title': 'JANGAN PERNAH MENYERAH! 🔥',
            'text': 'Hari ini mungkin berat, tapi percayalah, setiap kesulitan akan membuatmu lebih kuat. Jangan pernah menyerah pada impianmu! Allah tidak memberikan beban melebihi kemampuan hamba-Nya.',
            'hashtags': ['#motivasi', '#inspirasi', '#janganmenyerah', '#islam']
        },
        'inspirasi': {
            'title': 'KISAH NYATA YANG MENGUBAH HIDUPMU ✨',
            'text': 'Dari nol hingga sukses, perjalanan ini membuktikan bahwa kerja keras tidak akan mengkhianati hasil. Mulailah dari langkah kecil hari ini dan percayalah pada proses!',
            'hashtags': ['#inspirasi', '#sukses', '#kerjakeras', '#viral']
        }
    }
    return templates.get(niche, templates['motivasi'])
