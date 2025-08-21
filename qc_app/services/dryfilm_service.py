import logging
from django.forms import model_to_dict
from django.http import JsonResponse
from ..models import DryFilmProduct, DryFilmStandard

logger = logging.getLogger(__name__)

class DryFilmService:
    """干膜产品业务逻辑服务"""
    
    # 判定结果选项
    JUDGMENT_CHOICES = {
        'qualified': '合格',
        'unqualified': '不合格', 
        'pending': '待判定',
        'no_standard': '无标准'
    }
    
    @staticmethod
    def judge_product_quality(instance, target_index):
        """
        判断产品质量
        
        Args:
            instance: DryFilmProduct实例
            target_index: 产品牌号
            
        Returns:
            tuple: (factory_judgment, internal_judgment, error_message)
        """
        try:
            # 获取标准配置
            standard = DryFilmStandard.objects.get(product_name=target_index).config_json
            
            # 获取需要判断的字段数据
            instance_dict = model_to_dict(
                instance,
                fields=[field.name for field in instance._meta.fields],
                exclude=[
                    'id', 'created_at', 'updated_at', 'batch_number', 
                    'product_id', 'production_line', 'appearance', 
                    'inspector', 'test_date', 'sample_type', 'remarks',
                    'factory_judgment', 'internal_judgment', 'inhibitor',
                    'conversion_rate', 'loading_temp', 'change_log'
                ]
            )
            
            # 初始化计数器
            factory_ok, factory_ng, factory_pending = 0, 0, 0
            internal_ok, internal_ng, internal_pending = 0, 0, 0
            
            # 遍历所有需要判断的字段
            for field_name in instance_dict:
                value = instance_dict[field_name]
                
                # 判断外控标准
                factory_result = DryFilmService._judge_single_field(
                    value, standard, field_name, is_internal=False
                )
                if factory_result == 'ok':
                    factory_ok += 1
                elif factory_result == 'ng':
                    factory_ng += 1
                else:
                    factory_pending += 1
                
                # 判断内控标准
                internal_result = DryFilmService._judge_single_field(
                    value, standard, field_name, is_internal=True
                )
                if internal_result == 'ok':
                    internal_ok += 1
                elif internal_result == 'ng':
                    internal_ng += 1
                else:
                    internal_pending += 1
            
            # 最终判定逻辑
            factory_judgment = DryFilmService._final_judgment(
                factory_ok, factory_ng, factory_pending
            )
            internal_judgment = DryFilmService._final_judgment(
                internal_ok, internal_ng, internal_pending
            )
            
            return factory_judgment, internal_judgment, None
            
        except DryFilmStandard.DoesNotExist:
            logger.warning(f"产品 {target_index} 的标准配置不存在")
            return 'no_standard', 'no_standard', "未建立标准"
        except Exception as e:
            logger.error(f"产品质量判断失败: {str(e)}")
            return 'pending', 'pending', str(e)
    
    @staticmethod
    def _judge_single_field(value, standard, field_name, is_internal=False):
        """
        判断单个字段是否符合标准
        
        Args:
            value: 字段值
            standard: 标准配置字典
            field_name: 字段名称
            is_internal: 是否为内控标准
            
        Returns:
            str: 'ok', 'ng', 或 'pending'
        """
        prefix = 'in_' if is_internal else ''
        max_key = f"{prefix}{field_name}_max"
        min_key = f"{prefix}{field_name}_min"
        
        # 检查标准是否存在
        if max_key not in standard and min_key not in standard:
            return 'pending'
        
        # 检查值是否为数字
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return 'pending'
        
        # 判断范围
        max_val = standard.get(max_key)
        min_val = standard.get(min_key)
        
        if max_val is not None and min_val is not None:
            # 范围判断
            if min_val <= value <= max_val:
                return 'ok'
            else:
                return 'ng'
        elif min_val is not None and max_val is None:
            # 最小值判断
            if value >= min_val:
                return 'ok'
            else:
                return 'ng'
        elif max_val is not None and min_val is None:
            # 最大值判断
            if value <= max_val:
                return 'ok'
            else:
                return 'ng'
        else:
            return 'pending'
    
    @staticmethod
    def _final_judgment(ok_count, ng_count, pending_count):
        """
        最终判定逻辑
        
        Args:
            ok_count: 合格数量
            ng_count: 不合格数量
            pending_count: 待判定数量
            
        Returns:
            str: 判定结果
        """
        if ng_count > 0:
            return 'unqualified'
        elif pending_count > 0:
            return 'pending'
        elif ok_count > 0:
            return 'qualified'
        else:
            return 'pending'
