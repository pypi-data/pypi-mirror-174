# encoding: utf-8
"""
@project: djangoModel->enroll_record_serivce
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户报名记录
@created_time: 2022/9/17 15:45
"""
from django.core.paginator import Paginator

from ..models import EnrollRecord, Enroll
from ..utils.custom_tool import format_params_handle


class EnrollRecordServices:

    @staticmethod
    def record_add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll_id",
                "user_id",
                "enroll_auth_status_id",
                "enroll_pay_status_id",
                "enroll_status_code",
                "create_time",
                "price",
                "deposit",
                "count",
                "main_amount",
                "coupon_amount",
                "again_reduction",
                "subitems_amount",
                "deposit_amount",
                "amount",
                "paid_amount",
                "unpaid_amount",
                "fee",
                "photos",
                "files",
                "score",
                "reply",
                "remark",
            ],
        )
        try:
            instance, is_create = EnrollRecord.objects.get_or_create(user_id=params["user_id"], enroll_id=params["enroll_id"], defaults=params)
        except Exception as e:
            return None, str(e)
        return instance.to_json(), None

    @staticmethod
    def record_list(params):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id",
                "enroll_id",
                "user_id",
                "enroll_auth_status_id",
                "enroll_pay_status_id",
                "enroll_status_code",
                "create_time",
                "price",
                "deposit",
                "count",
                "main_amount",
                "coupon_amount",
                "again_reduction",
                "subitems_amount",
                "deposit_amount",
                "amount",
                "paid_amount",
                "unpaid_amount",
                "fee",
                "photos",
                "files",
                "score",
                "reply",
                "remark",
            ],
        )
        enroll_obj = EnrollRecord.objects.filter(**params).values()
        count = enroll_obj.count()
        paginator = Paginator(enroll_obj, size)
        enroll_obj = paginator.page(page)
        enroll_list = list(enroll_obj.object_list)
        data = {'total': count, "page": page, "size": size, 'list': enroll_list}
        return data, None

    @staticmethod
    def record_edit(params, pk):
        pk = params.pop("id", None) or pk
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "enroll", "user_id", "enroll_auth_status_id", "enroll_pay_status_id", "enroll_status_code", "create_time", "price", "deposit", "count", "main_amount", "coupon_amount",
                "again_reduction", "subitems_amount", "deposit_amount", "amount", "paid_amount", "unpaid_amount", "fee", "photos", "files", "score", "reply", "remark",
            ],
        )
        record_obj = EnrollRecord.objects.filter(id=pk)
        if not record_obj:
            return None, None
        try:
            record_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def record_del(pk, search_params=None):
        if pk:
            record_obj = EnrollRecord.objects.filter(id=pk)
        elif search_params and isinstance(search_params, dict):
            record_obj = EnrollRecord.objects.filter(**search_params)
        else:
            return None, "找不到要删除的数据"

        if not record_obj:
            return None, None
        try:
            record_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def check_can_add(enroll_id, user_id):
        enroll_obj = Enroll.objects.filter(id=enroll_id)
        if not enroll_obj:
            return False

        need_num = enroll_obj.first().to_json().get("count")
        enroll_record_obj = EnrollRecord.objects.filter(enroll_id=enroll_id, user_id=user_id, enroll_status_code__lt=356)
        if not enroll_record_obj:
            return True

        if need_num > enroll_record_obj.count():
            return True

        return False
