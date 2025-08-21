from django.db import models
import uuid , json
from django.utils import timezone

class LoggedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    change_log = models.JSONField('变更日志', default=list)
    
    class Meta:
        abstract = True

#####################################################################
class DryFilmProduct(LoggedModel):
    class Meta:
        verbose_name = '干膜产品'
        verbose_name_plural = '干膜产品'
        db_table = 'dry_film_products'  # 自定义表名
       
    BATCH_TYPE_CHOICES = [
        ('single', '单批样'),
        ('continuous', '装车样'),
        ('special', '特殊样'),
    ]
    
    # 产品信息
    batch_number = models.CharField('批号', max_length=80, unique=False, null=False)
    product_id = models.CharField('产品牌号', max_length=80, null=False)
    production_line = models.CharField('产线', max_length=80, null=False)
    inspector = models.CharField('检测人', max_length=80, null=False)
    test_date = models.DateField('测试日期', null=False)
    sample_type = models.CharField(
        '样品类别', 
        max_length=30, 
        choices=BATCH_TYPE_CHOICES, 
        default='single',
        null=False
    )
    remarks = models.TextField('备注', blank=True, null=True)
    
    # 判定结果组 (只定义一次)
    JUDGMENT_CHOICES = [
        ('qualified', '合格'),
        ('unqualified', '不合格'),
        ('pending', '待判定'),
        ('no_standard', '无标准'),
    ]
    
    factory_judgment = models.CharField(
        '出厂判定', 
        max_length=50, 
        choices=JUDGMENT_CHOICES,
        default='pending', 
        null=True
    )
    
    internal_judgment = models.CharField(
        '内控判定', 
        max_length=50, 
        choices=JUDGMENT_CHOICES,
        default='pending', 
        null=True
    )
    
    # 产品数据
    appearance = models.CharField('外观', null=True, blank=True, default='合格', max_length=20)
    solid_content = models.FloatField('固含', null=True, blank=True)
    viscosity = models.IntegerField('粘度', null=True, blank=True)
    acid_value = models.FloatField('酸值', null=True, blank=True)
    moisture = models.FloatField('水分', null=True, blank=True)
    residue = models.FloatField('残单', null=True, blank=True)
    molecular_weight = models.IntegerField('重均分子量', null=True, blank=True)
    pdi = models.FloatField('PDI', null=True, blank=True)
    color = models.FloatField('色度', null=True, blank=True)
    inhibitor = models.FloatField('阻聚剂', null=True, blank=True)
    conversion_rate = models.FloatField('转化率', null=True, blank=True)
    loading_temp = models.FloatField('装车温度', null=True, blank=True)
    
    def __str__(self):
        return f"{self.product_id} - {self.batch_number}"


class DryFilmStandard(LoggedModel):
    product_name = models.CharField(max_length=100, verbose_name="产品名称", null=True, unique=True)
    producer = models.CharField(max_length=50, verbose_name="编制人", null=True)
    config_json = models.JSONField(verbose_name="产品标准", null=True)

    def __str__(self):
        return f"{self.product_name} ({self.production_date})"
    
    def get_config_display(self):
        """用于模板中格式化显示JSON配置"""
        return json.dumps(self.config_json, indent=2, ensure_ascii=False)



#####################################################################
class AdhesiveProduct(LoggedModel):
    BATCH_TYPE_CHOICES = [
        ('single', '单批样'),
        ('continuous', '装车样'),
        ('special', '特殊样'),
    ]
    # 产品信息
    batch_number = models.CharField('批号', max_length=80, unique=True, null=False)
    product_id = models.CharField('产品牌号', max_length=80, null=False)
    production_line = models.CharField('产线', max_length=80, null=False)
    inspector = models.CharField('检测人', max_length=80, null=False)
    test_date = models.DateField('测试日期', default=timezone.now, null=False)
    sample_type = models.CharField('样品类别', max_length=80, choices=BATCH_TYPE_CHOICES, default='single', null=False)
    remarks = models.TextField('备注', blank=True, null=True)
    
    # 判定结果
    JUDGMENT_CHOICES = [
        ('qualified', '合格'),
        ('unqualified', '不合格'),
        ('pending', '待判定'),
    ]

    physical_judgment = models.CharField('理化性能判定', max_length=80, choices=JUDGMENT_CHOICES, default='pending')
    tape_judgment = models.CharField('胶带性能判定', max_length=80, choices=JUDGMENT_CHOICES, default='pending')
    finally_judgment = models.CharField('最终判定', max_length=80, choices=JUDGMENT_CHOICES, default='pending')
    
    # 产品数据
    appearance = models.CharField('外观', null=True, blank=True, default='合格', max_length=20)
    solid_content = models.FloatField('固含', null=True, blank=True)
    viscosity = models.FloatField('粘度', null=True, blank=True)
    acid_value = models.FloatField('酸值', null=True, blank=True)
    moisture = models.FloatField('水分', null=True, blank=True)
    residue = models.FloatField('残单', null=True, blank=True)
    molecular_weight = models.FloatField('重均分子量', null=True, blank=True)
    pdi = models.FloatField('PDI', null=True, blank=True)
    color = models.FloatField('色度', null=True, blank=True)
    initial_stick = models.FloatField('初粘', null=True, blank=True)
    peel = models.FloatField('剥离', null=True, blank=True)
    high_temp_hold = models.FloatField('高温持粘', null=True, blank=True)
    normal_temp_hold = models.FloatField('常温持粘', null=True, blank=True)
    peel_under_load = models.FloatField('定荷重剥离', null=True, blank=True)
    
    class Meta:
        verbose_name = '胶粘剂产品'
        verbose_name_plural = '胶粘剂产品'
        db_table = 'adhesive_products'
    
    def __str__(self):
        return f"{self.product_id} - {self.batch_number}"




#####################################################################
class RawMaterial(LoggedModel):
    class Meta:
        verbose_name = '原料'
        verbose_name_plural = '原料'
        db_table = 'raw_material'  # 自定义表名

    MATERIAL_TYPES = [
        ('resin', '树脂'),
        ('solvent', '溶剂'),
        ('additive', '添加剂'),
        ('monomer', '单体'),
        ('other', '其他'),
    ]
    
    # 判定结果组 (只定义一次)
    JUDGMENT_CHOICES = [
        ('qualified', '合格'),
        ('unqualified', '不合格'),
        ('pending', '待判定'),
    ]

    batch_number = models.CharField('原料批号', max_length=20, unique=True, null=False)
    material_name = models.CharField('原料名称', max_length=20, null=False)
    material_type = models.CharField('原料类型', max_length=20, choices=MATERIAL_TYPES, default='other', null=False)
    supplier = models.CharField('供应商', max_length=100, default='defalt')
    received_date = models.DateField('入库日期', default=timezone.now, null=False)
    expiry_date = models.DateField('有效期至', null=False)
    inspector = models.CharField('检验人', max_length=50, null=False)

    appearance = models.CharField('外观', max_length=100, null=True, default='合格')
    purity = models.FloatField('纯度(%)', null=True, blank=True)
    moisture = models.FloatField('水分含量(%)', null=True, blank=True)
    inhibitor = models.FloatField('阻聚剂含量(%)', null=True, blank=True)   #修改
    test_result = models.CharField('检验结果', max_length=20, choices=JUDGMENT_CHOICES, default='pending')
    peak_position = models.FloatField('出峰位置', null=True, blank=True)   #修改
    ethanol_content = models.FloatField('乙醇含量', null=True, blank=True)   #修改
    acidity = models.FloatField('酸度', null=True, blank=True)   #修改
    remarks = models.CharField('备注', max_length=100, null=True)


    def __str__(self):
        return f"{self.material_name} - {self.batch_number}"
   



#####################################################################
class TrialProduct(LoggedModel):
    class Meta:
        verbose_name = '小试产品'
        verbose_name_plural = '小试产品'
        db_table = 'trial_product'  # 自定义表名

    PRODUCT_TYPES = [
        ('dryfilm', '干膜'),
        ('adhesive', '胶粘剂'),
        ('coating', '涂料'),
        ('ink', '油墨'),
        ('other', '其他'),
    ]
    
    trial_number = models.CharField('小试编号', max_length=20, null=False)
    product_id = models.CharField('产品牌号', max_length=20, unique=True, null=False)
    test_date = models.DateField('测试日期', default=timezone.now, null=False)
    responsible = models.CharField('负责人', max_length=20, null=False)
    product_type = models.CharField('产品类型', max_length=20, choices=PRODUCT_TYPES, null=False)
    inspector = models.CharField('检验人', max_length=50, null=False)

    appearance = models.CharField('外观', null=True, blank=True, default='合格', max_length=20)
    solid_content = models.FloatField('固含', null=True, blank=True)
    viscosity = models.IntegerField('粘度', null=True, blank=True)
    acid_value = models.FloatField('酸值', null=True, blank=True)
    moisture = models.FloatField('水分', null=True, blank=True)
    residue = models.FloatField('残单', null=True, blank=True)
    molecular_weight = models.IntegerField('重均分子量', null=True, blank=True)
    pdi = models.FloatField('PDI', null=True, blank=True)
    color = models.FloatField('色度', null=True, blank=True)
    initial_stick = models.FloatField('初粘', null=True, blank=True)
    peel = models.FloatField('剥离', null=True, blank=True)
    high_temp_hold = models.FloatField('高温持粘', null=True, blank=True)
    normal_temp_hold = models.FloatField('常温持粘', null=True, blank=True)
    peel_under_load = models.FloatField('定荷重剥离', null=True, blank=True)
    remarks = models.TextField('备注', blank=True)

    
    def __str__(self):
        return f"{self.product_id} - {self.trial_number}"



#####################################################################
class ReportCenter(LoggedModel):
    class Meta:
        verbose_name = '报告中心'
        verbose_name_plural = '报告中心'
        db_table = 'report_center'  # 自定义表名

    REPORT_TYPES = [
        ('daily', '日常报告'),
        ('monthly', '月度报告'),
        ('quarterly', '季度报告'),
        ('yearly', '年度报告'),
        ('special', '专项报告'),
    ]
    
    REPORT_STATUS = [
        ('draft', '草稿'),
        ('review', '审核中'),
        ('approved', '已批准'),
        ('released', '已发布'),
    ]
    
    report_number = models.CharField('报告编号', max_length=50, unique=True)
    report_type = models.CharField('报告类型', max_length=20, choices=REPORT_TYPES)
    title = models.CharField('报告标题', max_length=200)
    period_start = models.DateField('报告起始日期')
    period_end = models.DateField('报告结束日期')
    generated_by = models.CharField('生成人', max_length=50)
    generated_date = models.DateTimeField('生成日期', default=timezone.now)
    reviewer = models.CharField('审核人', max_length=50, blank=True)
    status = models.CharField('状态', max_length=20, choices=REPORT_STATUS, default='draft')
    report_file = models.FileField('报告文件', upload_to='reports/')
    
    def __str__(self):
        return f"{self.report_number} - {self.title}"




class AnalysisCenter(LoggedModel):
    class Meta:
        verbose_name = '分析中心'
        verbose_name_plural = '分析中心'
        db_table = 'analysis_center'  # 自定义表名

    ANALYSIS_TYPES = [
        ('quality', '质量分析'),
        ('process', '过程分析'),
        ('trend', '趋势分析'),
        ('comparative', '对比分析'),
        ('root_cause', '根本原因分析'),
    ]
    
    analysis_id = models.CharField('分析编号', max_length=50, unique=True)
    analysis_type = models.CharField('分析类型', max_length=20, choices=ANALYSIS_TYPES)
    title = models.CharField('分析标题', max_length=200)
    start_date = models.DateField('起始日期')
    end_date = models.DateField('结束日期')
    performed_by = models.CharField('分析人', max_length=50)
    performed_date = models.DateTimeField('分析日期', default=timezone.now)
    data_source = models.CharField('数据源', max_length=100)
    findings = models.TextField('分析发现', blank=True)
    recommendations = models.TextField('改进建议', blank=True)
    visualization = models.FileField('可视化文件', upload_to='analytics/', blank=True)
    
    def __str__(self):
        return f"{self.analysis_id} - {self.title}"
    

