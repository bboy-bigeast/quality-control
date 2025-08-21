import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import RawMaterialForm
from ..models import RawMaterial

logger = logging.getLogger(__name__)

def rawmaterial_list(request):
    """原材料产品列表视图"""
    products = RawMaterial.objects.all()
    logger.info(f"查询到 {len(products)} 条原材料产品记录")

    # 分页处理
    product_list = RawMaterial.objects.all().order_by('-received_date')
    paginator = Paginator(product_list, 10)
    
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return render(request, 'qc_app/rawmaterial_list.html', {
        'products': products, 
        'objects': objects
    })

def rawmaterial_create(request):
    """创建原材料产品视图"""
    if request.method == 'POST':
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '原材料产品创建成功')
            return redirect('rawmaterial_list')
    else:
        form = RawMaterialForm()
    
    return render(request, 'qc_app/rawmaterial_form.html', {'form': form})

def rawmaterial_edit(request, pk):
    """编辑原材料产品视图"""
    product = get_object_or_404(RawMaterial, pk=pk)
    
    if request.method == 'POST':
        form = RawMaterialForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '原材料产品更新成功')
            return redirect('rawmaterial_list')
    else:
        form = RawMaterialForm(instance=product)
    
    return render(request, 'qc_app/rawmaterial_form.html', {
        'form': form, 
        'product': product
    })

@require_POST
def rawmaterial_delete(request):
    """删除原材料产品视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(RawMaterial, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.material_name}-{record.batch_number} 已成功删除")
        return redirect('rawmaterial_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)
