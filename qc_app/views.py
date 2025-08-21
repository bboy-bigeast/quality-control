"""
主视图文件 - 导入所有模块化视图
此文件作为视图入口点，导入所有模块化的视图函数
"""

# 导入所有模块化视图
from .views.base_views import *
from .views.dryfilm_views import *
from .views.standard_views import *
from .views.adhesive_views import *
from .views.rawmaterial_views import *
from .views.trialproduct_views import *
from .views.report_views import *
from .views.analysis_views import *

# 导入其他必要的模块
import logging
from django.http import HttpResponse  
from openpyxl import Workbook
from django.db.models import Q
from .models import ReportCenter, AnalysisCenter

logger = logging.getLogger(__name__)

##################################################################################################################
# 报告中心首页
def reports_home(request):
    return render(request, 'qc_app/reports_home.html')

# Excel报告生成
def generate_excel_report(request, product_type, batch_number):
    """生成Excel报告视图"""
    # 获取产品数据
    product = get_object_or_404(DryFilmProduct, batch_number=batch_number)
    
    # 创建Excel工作簿
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{batch_number}_report.xlsx"'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "质检报告"
    
    # 添加报告头
    headers = ["质检报告", f"产品牌号: {product.product_id}", f"批号: {batch_number}"]
    for i, header in enumerate(headers, 1):
        ws.cell(row=i, column=1, value=header)
    
    # 添加数据表格
    data_rows = [
        ["检测项目", "标准要求", "实测值", "判定"],
        ["外观", "-", product.appearance, ""],
        # 其他数据行...
    ]
    
    for row_idx, row_data in enumerate(data_rows, 4):
        for col_idx, value in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    wb.save(response)
    return response

########################################################################################################
def report_list_legacy(request):
    """旧版报告列表视图（兼容性）"""
    reports = ReportCenter.objects.filter(
        Q(generated_by=request.user.username) | 
        Q(status__in=['approved', 'released'])
    ).order_by('-generated_date')
    
    return render(request, 'qc_app/report_list.html', {'reports': reports})

########################################################################################################
def analysis_list_legacy(request):
    """旧版分析列表视图（兼容性）"""
    analyses = AnalysisCenter.objects.all().order_by('-performed_date')
    return render(request, 'qc_app/analysis_list.html', {'analyses': analyses})

########################################################################################################
def test_permission(request):
    """测试权限页面"""
    return render(request, 'qc_app/test_permission.html', {
        'user_role': request.user_role,
        'client_ip': request.META.get('REMOTE_ADDR')
    })

def test_view(request):
    """测试视图"""
    print(f"用户角色: {request.user_role}")
    print(f"客户端IP: {request.META.get('REMOTE_ADDR')}")
    # ...
