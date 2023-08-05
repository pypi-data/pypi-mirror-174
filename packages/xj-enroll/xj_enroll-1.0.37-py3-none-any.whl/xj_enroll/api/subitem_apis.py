from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from xj_user.utils.user_wrapper import user_authentication_wrapper
from ..service.subitem_service import SubitemService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data


class SubitemApis(APIView):

    @require_http_methods(['GET'])
    @user_authentication_wrapper
    def list(self, *args, **kwargs, ):
        request_params = parse_data(self)
        data, err = SubitemService.list(params=request_params)

        if err:
            return util_response(err=1000, msg=data)
        return util_response(data=data)

    @require_http_methods(['POST'])
    def add(self, *args, **kwargs, ):
        params = parse_data(self)
        data, err = SubitemService.add(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit(self, *args, **kwargs, ):
        params = parse_data(self)
        subitem_id = params.pop("id", None) or kwargs.pop("pk", None)
        data, err = SubitemService.edit(params, subitem_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit_by_enroll_id(self, *args, **kwargs, ):
        params = parse_data(self)
        enroll_id = params.pop("id", None) or kwargs.pop("enroll_id", None)
        data, err = SubitemService.batch_edit(params, enroll_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # @require_http_methods(['DELETE'])
    # def delete(self, *args, **kwargs, ):
    #     params = parse_data(self)
    #     subitem_id = params.pop("id", None) or kwargs.pop("pk", None)
    #     data, err = SubitemService.delete(params, subitem_id)
    #     if err:
    #         return util_response(err=1000, msg=err)
    #     return util_response(data=data)

    @require_http_methods(['GET'])
    def extend_field(self, *args, **kwargs, ):
        request_params = parse_data(self)
        is_pagination = request_params.pop("is_pagination", 1)
        is_pagination = int(is_pagination)
        data, err = SubitemService.extend_field(params=request_params, is_pagination=is_pagination)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
