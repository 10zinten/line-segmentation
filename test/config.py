from pathlib import Path


class config:
    # ocr_output paths
    ocr_path = Path('/home/tenzin/ML/project/Esukhia/Google-OCR/archive')
    # peydurma tengyur
#     images_path = ocr_path/'images'/'W1PD95844'
#     res_path = ocr_path/'output'/'W1PD95844'

    # peydurma kangyur
    images_path = ocr_path/'images'/'W1PD96682'
    res_path = ocr_path/'output'/'W1PD96682'

    # peydurma path
    peydurma_path = Path('data/peydurma')
    template_path = peydurma_path/'templates'
    peydurma_meta_fn = peydurma_path/'tengyur-peydurma-bdrc.xml'

    # dergey opf path
    op_path = Path('/home/tenzin/ML/project/Esukhia/openpecha-user/.openpecha/data/')
    tengyur_opf = op_path/'P000002/P000002.opf'
    kangyur_opf = op_path/'P000001/P000001.opf'

    # output_path
    output_path = peydurma_path/'output'
    output_path.mkdir(exist_ok=True)
    output_tmp_path = output_path/'tmp'
    output_tmp_path.mkdir(exist_ok=True)

    # annotation
    double_tsek_sym = '$'
    tsek = '་'
    shed = '།'

    # image
    img_size = (3969, 2641)

    # dev
    debug = False
