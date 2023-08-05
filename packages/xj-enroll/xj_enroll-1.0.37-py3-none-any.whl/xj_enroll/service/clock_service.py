# encoding: utf-8
"""
@project: djangoModel->clock_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名计时服务
@created_time: 2022/10/28 13:37
"""
from django.db.models import F
from django_redis import get_redis_connection

from ..models import EnrollRecord, Enroll, EnrollSubitem, EnrollSubitemRecord

ENROLL_CLOCK = "enroll-clock-ttl-{}"  # 倒计时
ENROLLED_HSET_LIST = "enroll-hset-list"


class ClockService:
    def __init__(self):
        self.conn = get_redis_connection()

    def add_clock(self, enroll_id=None, user_id=None):
        if not enroll_id or not user_id:
            return None, "enroll_id 和 user_id 必传"

        # 报名状态进入356 (已接单待上传)
        clock_key = ENROLL_CLOCK.format(enroll_id)
        has_clock = self.conn.get(clock_key)
        # print("has_clock:", has_clock)
        if not has_clock:
            self.conn.set(clock_key, user_id)
            self.conn.expire(clock_key, 600)

        # 记录报名用户
        enroll_users = self.conn.hget(ENROLLED_HSET_LIST, enroll_id)
        # print("enroll_users:", enroll_users)
        users_list = enroll_users.decode().split(";") if enroll_users else []
        users_list.append(str(user_id))
        users_list = list(set(users_list))

        users_list_str = ""
        for i in users_list:
            users_list_str = users_list_str + (";" if users_list_str else "") + i

        self.conn.hset(ENROLLED_HSET_LIST, enroll_id, users_list_str)
        self.conn.expire(ENROLLED_HSET_LIST, 660)

    # 闹钟是否停止
    def check_clock(self, enroll_id=None):
        if not enroll_id:
            return None, "enroll_i 必传且不能为空"
        clock_key = ENROLL_CLOCK.format(enroll_id)
        clock_ttl = self.conn.ttl(clock_key)
        return {"clock_ttl": clock_ttl}, None

    def check_end_clock(self):
        """定时脚本执行方法"""
        enroll_ids = self.conn.hkeys(ENROLLED_HSET_LIST)
        # print("enroll_ids:", enroll_ids)
        for enroll_id in enroll_ids:
            # 时候报名结束
            is_active_clock = self.conn.get(ENROLL_CLOCK.format(enroll_id.decode()))
            # print("enroll_id:", enroll_id, "是否定时:", is_active_clock)
            if is_active_clock:
                continue

            # 计时结束则进行如下操作
            enroll_obj = Enroll.objects.filter(id=enroll_id)
            eroll_count = enroll_obj.first().to_json().get("count", 0) if enroll_obj else 0  # 需求份数
            if eroll_count == 0:
                continue

            enroll_record_obj = EnrollRecord.objects.filter(enroll_id=enroll_id)
            if not enroll_record_obj:
                # print("实际报名人数为0")
                self.conn.hdel(ENROLLED_HSET_LIST, enroll_id)
                continue
            enroll_people_count = enroll_record_obj.count()  # 实际报名人数
            # print("实际报名人数:", enroll_people_count, "需求份数:", eroll_count)

            # 根据报名定时截至的时候报名人数处理报名
            if enroll_people_count == 0:  # 有人取消报名，什么都不做，报名人数为0。
                continue

            if enroll_people_count == 1:  # 一个人报名，生成多条记录
                enroll_record_obj.update(count=eroll_count)
                overplus = eroll_count - enroll_people_count
                if overplus <= 0:
                    continue

                # 把剩余的名额全部全部给这个人报名 TODO
                enroll_record_obj.update(count=eroll_count)
                subtems_obj = EnrollSubitem.objects.annotate(enroll_subitem_id=F("id")).annotate(subitem_amount=F("amount")).filter(enroll_id=enroll_id)
                if not subtems_obj:
                    continue
                values = list(subtems_obj.values("price", "count", "enroll_subitem_id", "subitem_amount"))
                enroll_record = enroll_record_obj.first()
                sub_record_obj = EnrollSubitemRecord.objects.filter(enroll_record_id=enroll_record.id)
                sub_record_obj.delete()

                for i in values:
                    params = i
                    params["enroll_record_id"] = enroll_record_obj.first().id
                    EnrollSubitemRecord.objects.create(**params)

            # 当超过一个人的时候，则仅仅改动报名住哪个太由后台人员指定报名
            enroll_obj.update(enroll_status_code=356)
            self.conn.hdel(ENROLLED_HSET_LIST, enroll_id)
