from django.contrib import admin
from .models import DryFilmProduct
from .forms import DryFilmForm
from .models import AdhesiveProduct
from .forms import AdhesiveForm

class DryFilmProductAdmin(admin.ModelAdmin):
    form = DryFilmForm
    list_display = ('batch_number', 
                    'product_id', 
                    'test_date', 
                    'inspector', 
                    'display_factory_judgment',  # 使用自定义方法
                    'display_internal_judgment')   # 使用自定义方法
    list_filter = ('test_date', 'production_line', 'sample_type')
    search_fields = ('batch_number', 'product_id')
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'batch_number', 'product_id', 'production_line', 
                'inspector', 'test_date', 'sample_type', 'remarks'
            )
        }),
        ('判定结果', {
            'fields': ('factory_judgment', 'internal_judgment')
        }),
        ('物理数据', {
            'fields': (
                'appearance', 'solid_content', 'viscosity', 'acid_value', 
                'moisture', 'residue', 'molecular_weight', 'pdi',
                'color', 'inhibitor', 'conversion_rate', 'loading_temp'
            )
        }),
        ('报告设置', {
            'fields': ('report_template',)
        })
    )
        # 自定义方法显示出厂判定
    def display_factory_judgment(self, obj):
        return obj.get_factory_judgment_display()
    display_factory_judgment.short_description = '出厂判定'
    
    # 自定义方法显示内控判定
    def display_internal_judgment(self, obj):
        return obj.get_internal_judgment_display()
    display_internal_judgment.short_description = '内控判定'

admin.site.register(DryFilmProduct, DryFilmProductAdmin)

class AdhesiveProductAdmin(admin.ModelAdmin):
    form = AdhesiveForm
    list_display = ('batch_number', 
                    'product_id', 
                    'test_date', 
                    'inspector', 
                    'display_physical_judgment',  # 使用自定义方法
                    'display_tape_judgment',      # 使用自定义方法
                    'display_finally_judgment'    # 使用自定义方法
                    )
    list_filter = ('test_date', 'production_line', 'sample_type')
    search_fields = ('batch_number', 'product_id')
    
    fieldsets = (
        ('基本信息', {
            'fields': (
                'batch_number', 'product_id', 'production_line', 
                'inspector', 'test_date', 'sample_type', 'remarks'
            )
        }),
        ('判定结果', {
            'fields': ('physical_judgment', 'tape_judgment', 'finally_judgment')
        }),
        ('理化数据', {
            'fields': (
            'appearance', 
            'solid_content',
            'viscosity', 
            'acid_value',
            'moisture', 
            'residue', 
            'molecular_weight', 
            'pdi',
            'color'
            )
        }),
        ('胶带数据', {
            'fields': (
            'initial_stick', 
            'peel', 
            'high_temp_hold',
            'normal_temp_hold', 
            'peel_under_load'
            )
        }),
        ('报告设置', {
            'fields': ('report_template',)
        })
    )
    # 自定义方法显示物理性能判定
    def display_physical_judgment(self, obj):
        return obj.get_physical_judgment_display()
    display_physical_judgment.short_description = '物理性能判定'
    
    # 自定义方法显示胶带性能判定
    def display_tape_judgment(self, obj):
        return obj.get_tape_judgment_display()
    display_tape_judgment.short_description = '胶带性能判定'
    
    # 自定义方法显示最终判定
    def display_finally_judgment(self, obj):
        return obj.get_finally_judgment_display()
    display_finally_judgment.short_description = '最终判定'

admin.site.register(AdhesiveProduct, AdhesiveProductAdmin)