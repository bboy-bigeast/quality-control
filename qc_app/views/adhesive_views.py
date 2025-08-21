import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import AdhesiveForm
from ..models import AdhesiveProduct

logger = logging.getLogger(__name__)

def adhesive_list(request):
    """胶粘剂产品列表视图"""
    products = AdhesiveProduct.objects.all()
    logger.info(f"查询到 {len(products)} 条胶粘剂产品记录")

    # 分页处理
    product_list = AdhesiveProduct.objects.all().order_by('-test_date')
    paginator = Paginator(product_list, 10)
    
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return render(request, 'qc_app/adhesive_list.html', {
        'products': products, 
        'objects': objects
    })

def adhesive_create(request):
    """创建胶粘剂产品视图"""
    if request.method == 'POST':
        form = AdhesiveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '胶粘剂产品创建成功')
            return redirect('adhesive_list')
    else:
        form = AdhesiveForm()
    
    return render(request, 'qc_app/adhesive_form.html', {'form': form})

def adhesive_edit(request, pk):
    """编辑胶粘剂产品视图"""
    product = get_object_or_404(AdhesiveProduct, pk=pk)
    
    if request.method == 'POST':
        form = AdhesiveForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '胶粘剂产品更新成功')
            return redirect('adhesive_list')
    else:
        form = AdhesiveForm(instance=product)
    
    return render(request, 'qc_app/adhesive_form.html', {
        'form': form, 
        'product': product
    })

@require_POST
def adhesive_delete(request):
    """删除胶粘剂产品视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(AdhesiveProduct, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.product_id}-{record.batch_number} 已成功删除")
        return redirect('adhesive_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)
