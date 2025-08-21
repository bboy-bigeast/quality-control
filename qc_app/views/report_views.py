import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import ReportCenter

logger = logging.getLogger(__name__)

def report_list(request):
    """报告列表视图"""
    reports = ReportCenter.objects.all()
    logger.info(f"查询到 {len(reports)} 条报告记录")

    # 分页处理
    report_list = ReportCenter.objects.all().order_by('-created_at')
    paginator = Paginator(report_list, 10)
    
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return render(request, 'qc_app/report_list.html', {
        'reports': reports, 
        'objects': objects
    })

def report_create(request):
    """创建报告视图"""
    # 由于没有ReportForm，暂时重定向到列表页面
    messages.info(request, '报告创建功能暂未实现')
    return redirect('report_list')

def report_edit(request, pk):
    """编辑报告视图"""
    # 由于没有ReportForm，暂时重定向到列表页面
    messages.info(request, '报告编辑功能暂未实现')
    return redirect('report_list')

@require_POST
def report_delete(request):
    """删除报告视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(ReportCenter, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.title} 已成功删除")
        return redirect('report_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)
