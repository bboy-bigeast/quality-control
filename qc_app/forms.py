# 在 qc_app 目录下创建 forms.py
from django import forms
from .models import DryFilmProduct, AdhesiveProduct, RawMaterial, TrialProduct, DryFilmStandard



class DryFilmForm(forms.ModelForm):
    class Meta:
        model = DryFilmProduct
        fields = [
            # 基本信息组
            'batch_number', 
            'product_id', 
            'production_line',
            'inspector', 
            'test_date', 
            'sample_type', 
            'remarks',
            
            # 判定结果组
            'factory_judgment', 
            'internal_judgment',
            
            # 产品数据组
            'appearance', 
            'solid_content', 
            'viscosity', 
            'acid_value', 
            'moisture', 
            'residue', 
            'molecular_weight', 
            'pdi', 
            'color', 
            'inhibitor', 
            'conversion_rate', 
            'loading_temp',
            
        ]
        
        widgets = {
            'test_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'yyyy-mm-dd'
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': '请输入备注信息...'
            }),
            'sample_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置表单验证不强制
        self.fields['factory_judgment'].required = False
        self.fields['internal_judgment'].required = False

class AdhesiveForm(forms.ModelForm):
    class Meta:
        model = AdhesiveProduct
        fields = [

            'batch_number', 
            'product_id', 
            'production_line',
            'inspector', 
            'test_date', 
            'sample_type', 
            'remarks',

            'physical_judgment', 
            'tape_judgment',
            'finally_judgment',
            
            'appearance', 
            'solid_content',
            'viscosity', 
            'acid_value',
            'moisture', 
            'residue', 
            'molecular_weight', 
            'pdi',
            'color', 
            'initial_stick', 
            'peel', 
            'high_temp_hold',
            'normal_temp_hold', 
            'peel_under_load'
        ]
        
        widgets = {
            'test_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': '输入备注信息...'
            }),
            'factory_judgment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'internal_judgment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'sample_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = [
            # 基本信息组
            'batch_number', 
            'material_name', 
            'material_type',
            'supplier', 
            'received_date', 
            'expiry_date', 
            'inspector',
            
            # 产品数据组
            'appearance', 
            'purity', 
            'moisture', 
            'inhibitor', 
            'peak_position',  
            'ethanol_content',  
            'acidity', 
            'remarks'
        ]
        
        widgets = {
            'received_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
            'expiry_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': '请输入备注信息...'
            }),
            'material_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        } 

class TrialProductForm(forms.ModelForm):
    class Meta:
        model = TrialProduct
        fields = [
            ##############
            'trial_number', 
            'product_id', 
            'inspector', 
            'responsible', 
            'test_date', 
            'product_type', 
            ##############
            'appearance', 
            'solid_content',
            'viscosity', 
            'acid_value',
            'moisture', 
            'residue', 
            'molecular_weight', 
            'pdi',
            'color', 
            'initial_stick', 
            'peel', 
            'high_temp_hold',
            'normal_temp_hold', 
            'peel_under_load',
            'remarks'
        ]
        
        widgets = {
            'test_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': '输入备注信息...'
            }),
            'product_type': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
##############################################################################################################################
class DryFilmConfigForm(forms.Form):
    APPEARANCES = [
        ('qualified', '合格'),
        ('unqualified', '不合格')
    ]
    appearance = forms.ChoiceField(
        label="外观",
        choices=APPEARANCES,
        required=False
    )
#######################################################################
#                        外部标准                                      #
#######################################################################
    solid_content_max= forms.DecimalField(
        label="固含标准上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    solid_content_min= forms.DecimalField(
        label="固含标准下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    viscosity_max= forms.IntegerField(
        label="粘度标准上限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    viscosity_min= forms.IntegerField(
        label="粘度标准下限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    acid_value_max= forms.DecimalField(
        label="酸值标准上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    acid_value_min= forms.DecimalField(
        label="酸值标准下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    moisture_max= forms.DecimalField(
        label="水分标准上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    moisture_min= forms.DecimalField(
        label="水分标准下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    residue_max= forms.DecimalField(
        label="残单标准上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    residue_min= forms.DecimalField(
        label="残单标准下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    molecular_weight_max= forms.IntegerField(
        label="分子量标准上限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    molecular_weight_min= forms.IntegerField(
        label="分子量标准下限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    pdi_max= forms.DecimalField(
        label="pdi标准上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    pdi_min= forms.DecimalField(
        label="pdi标准下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    color_max= forms.DecimalField(
        label="色度标准上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    color_min= forms.DecimalField(
        label="色度标准下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
#######################################################################
#                        内部标准                                      #
#######################################################################
    in_solid_content_max= forms.DecimalField(
        label="固含内控上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_solid_content_min= forms.DecimalField(
        label="固含内控下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_viscosity_max= forms.IntegerField(
        label="粘度内控上限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    in_viscosity_min= forms.IntegerField(
        label="粘度内控下限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    in_acid_value_max= forms.DecimalField(
        label="酸值内控上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_acid_value_min= forms.DecimalField(
        label="酸值内控下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_moisture_max= forms.DecimalField(
        label="水分内控上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_moisture_min= forms.DecimalField(
        label="水分内控下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_residue_max= forms.DecimalField(
        label="残单内控上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_residue_min= forms.DecimalField(
        label="残单内控下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_molecular_weight_max= forms.IntegerField(
        label="分子量内控上限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    in_molecular_weight_min= forms.IntegerField(
        label="分子量内控下限",
        widget=forms.NumberInput(attrs={'step': '1'}) ,
        required=False
    )
    in_pdi_max= forms.DecimalField(
        label="pdi内控上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_pdi_min= forms.DecimalField(
        label="pdi内控下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}),
        required=False 
    )
    in_color_max= forms.DecimalField(
        label="色度内控上限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )
    in_color_min= forms.DecimalField(
        label="色度内控下限",
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}) ,
        required=False
    )




class DryFilmMainForm(forms.ModelForm):
    class Meta:
        model = DryFilmStandard
        fields = ['product_name', 'producer']
        widgets = {
            'config_json': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        config_json = kwargs.pop('config_json', None)
        super().__init__(*args, **kwargs)
        
        if config_json:
            self.fields['config_json'].initial = config_json