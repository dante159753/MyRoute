from flask import request


def check_form_para(para_list):
    for para_name in para_list:
        assert para_name in request.form
        assert len(request.form[para_name]) > 0
