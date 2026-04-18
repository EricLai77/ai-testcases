from django.db import models

# Create your models here.
class projectconfig(models.Model):
    '''
    项目配置表
    '''
    id = models.AutoField(primary_key=True)#AutoField表示自增；primary_key表示唯一
    key =  models.CharField(max_length=64, db_column='key')#db_column表示数据库列名
    value = models.CharField(max_length=255, db_column='value', default='')#字符，默认为空
    #DateField表示为Y-M-D；DateTimeField表示为Y-M-D H:M:S,auto_now为自动获取当前时间
    create_time = models.DateTimeField(auto_now=True)
    #备注字段
    memo = models.TextField()

    def __unicode__(self):
        '''
        配置默认返回值
        '''
        return self.id