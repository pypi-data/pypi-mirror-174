# from yourtools.WeChat import WeChat
from yourtools import WeChat
from yourtools import MySQL
from yourtools import Hive


def test_wechat():
    # 仲达（测试）
    zd_test = WeChat("ww06fa03084e27ff22", "uwYEfV7eyDL1y3IzkD_RvksxiA5UBvmJzWNP4ze8vjU", 1000116)
    data = {
        "touser": "1331811502877461564",
        "toparty": "",
        "totag": "",
        "msgtype": "text",
        "agentid": 1000116,
        "text": {
            "content": "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    send_statu = zd_test.send_text(data)
    print(send_statu)


def test_mysql():
    dbconfg = {
        'host': '172.28.28.99',
        'port': 3308,
        'username': 'root',
        'password': 'Data@2022!',
        'db': 'test',
        'charset': 'utf8'
    }
    mysql = MySQL(dbconfg)
    # result = mysql.execute("insert into users_cdc(name,birthday,ts) values('灭霸2','2022-11-01 16:00:00','2022-11-01 16:00:00') ")
    result = mysql.query("select * from users_cdc")
    print(result)


def test_hive():
    hive_connection = {
        'host': 'emr-header-2',
        'port': 10000,
        'db': 'ods',
        'username': '',
        'auth': 'NOSASL'
    }
    hive = Hive(hive_connection)
    hive_sql="""
        select shr_staff_no
      from dwd.dwd_other_billing_power_list t
      join (-- 近1个月有医疗收入开单的医生
    select nvl(sf.ehr_user_name,t.ehr_user_name) as shr_code
      from ads.ads_zm_doctor_comy_anay t
      left join dim.dim_staff sf on t.create_userid = sf.user_id
     where t.dtype = 'day'
       and t.dt >= date_sub(current_date(),30) -- 近1个月
       and t.medical_amt > 0  -- 有医疗收入
         group by nvl(sf.ehr_user_name,t.ehr_user_name)
      ) dc on t.shr_staff_no = dc.shr_code
     where t.role_name = '开单权限'
       and t.vet_id_number is not null   -- 有执兽证
       and t.is_beian = '否'             -- 未进行执业兽医备案
     group by shr_staff_no
    """
    rows = hive.query(hive_sql)
    print(rows)


def main():
    test_hive()


if __name__ == '__main__':
    main()
