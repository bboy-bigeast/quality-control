import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import AnalysisCenter

logger = logging.getLogger(__name__)

def analysis_list(request):
    """分析列表视图"""
    analyses = AnalysisCenter.objects.all()
    logger.info(f"查询到 {len(analyses)} 条分析记录")

    # 分页处理
    analysis_list = AnalysisCenter.objects.all().order_by('-created_at')
    paginator = Paginator(analysis_list, 10)
    
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return render(request, 'qc_app/analysis_list.html', {
        'analyses': analyses, 
        'objects': objects
    })

def analysis_create(request):
    """创建分析视图"""
    # 由于没有AnalysisForm，暂时重定向到列表页面
    messages.info(request, '分析创建功能暂未实现')
    return redirect('analysis_list')

def analysis_edit(request, pk):
    """编辑分析视图"""
    # 由于没有AnalysisForm，暂时重定向到列表页面
    messages.info(request, '分析编辑功能暂未实现')
    return redirect('analysis_list')

@require_POST
def analysis_delete(request):
    """删除分析视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(AnalysisCenter, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.title} 已成功删除")
        return redirect('analysis_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)
