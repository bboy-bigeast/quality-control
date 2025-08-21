import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import TrialProductForm
from ..models import TrialProduct

logger = logging.getLogger(__name__)

def trialproduct_list(request):
    """试用产品列表视图"""
    products = TrialProduct.objects.all()
    logger.info(f"查询到 {len(products)} 条试用产品记录")

    # 分页处理
    product_list = TrialProduct.objects.all().order_by('-test_date')
    paginator = Paginator(product_list, 10)
    
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return render(request, 'qc_app/trialproduct_list.html', {
        'products': products, 
        'objects': objects
    })

def trialproduct_create(request):
    """创建试用产品视图"""
    if request.method == 'POST':
        form = TrialProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '试用产品创建成功')
            return redirect('trialproduct_list')
    else:
        form = TrialProductForm()
    
    return render(request, 'qc_app/trialproduct_form.html', {'form': form})

def trialproduct_edit(request, pk):
    """编辑试用产品视图"""
    product = get_object_or_404(TrialProduct, pk=pk)
    
    if request.method == 'POST':
        form = TrialProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '试用产品更新成功')
            return redirect('trialproduct_list')
    else:
        form = TrialProductForm(instance=product)
    
    return render(request, 'qc_app/trialproduct_form.html', {
        'form': form, 
        'product': product
    })

@require_POST
def trialproduct_delete(request):
    """删除试用产品视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(TrialProduct, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.product_id}-{record.batch_number} 已成功删除")
        return redirect('trialproduct_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)
