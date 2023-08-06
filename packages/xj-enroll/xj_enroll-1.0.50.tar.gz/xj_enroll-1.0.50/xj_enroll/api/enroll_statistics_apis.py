# encoding: utf-8
"""
@project: djangoModel->enroll_statistics
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 统计接口
@created_time: 2022/10/31 11:07
"""
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from ..service.enroll_statistics_service import EnrollStatisticsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class EnrollStatisticsAPI(APIView):
    @require_http_methods(['GET'])
    @request_params_wrapper
    def statistics(self, *args, request_params=None, **kwargs):
        data, err = EnrollStatisticsService.statistics_by_day()
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
