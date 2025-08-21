import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..forms import DryFilmForm
from ..models import DryFilmProduct
from ..services.dryfilm_service import DryFilmService

logger = logging.getLogger(__name__)

def dryfilm_list(request):
    """干膜产品列表视图"""
    products = DryFilmProduct.objects.all()
    logger.info(f"查询到 {len(products)} 条干膜产品记录")

    # 分页处理
    product_list = DryFilmProduct.objects.all().order_by('-test_date')
    paginator = Paginator(product_list, 10)
    
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return render(request, 'qc_app/dryfilm_list.html', {
        'products': products, 
        'objects': objects
    })

def dryfilm_create(request):
    """创建干膜产品视图"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'judge':
            return _handle_judge_action(request, None)
        elif action == 'save':
            return redirect('dryfilm_list')
    
    form = DryFilmForm()
    
    context = {
        'form': form,
        'mode': 'create',
        'title': '添加干膜产品'
    }
    return render(request, 'qc_app/dryfilm_form.html', context)

def dryfilm_edit(request, pk):
    """编辑干膜产品视图"""
    product = get_object_or_404(DryFilmProduct, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'judge':
            return _handle_judge_action(request, product)
        elif action == 'save':
            return redirect('dryfilm_list')
    
    form = DryFilmForm(instance=product)
    return render(request, 'qc_app/dryfilm_form.html', {
        'form': form, 
        'mode': 'edit', 
        'product': product
    })

@require_POST
def dryfilm_delete(request):
    """删除干膜产品视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(DryFilmProduct, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.product_id}-{record.batch_number} 已成功删除")
        return redirect('dryfilm_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)

def _handle_judge_action(request, product_instance):
    """处理判定操作的通用逻辑"""
    form = DryFilmForm(request.POST, instance=product_instance)
    
    if form.is_valid():
        instance = form.save()
        target_index = instance.product_id
        
        # 使用服务层进行质量判定
        factory_judgment, internal_judgment, error_message = DryFilmService.judge_product_quality(
            instance, target_index
        )
        
        if error_message:
            # 处理错误情况
            instance.factory_judgment = 'no_standard'
            instance.save(update_fields=['factory_judgment'])
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'数据已经保存，{error_message}'
                }, status=500)
            else:
                messages.warning(request, f'数据已经保存，{error_message}')
                return render(request, 'qc_app/dryfilm_form.html', {
                    'form': form, 
                    'product': instance
                })
        
        # 更新判定结果
        instance.factory_judgment = factory_judgment
        instance.internal_judgment = internal_judgment
        instance.save(update_fields=['factory_judgment', 'internal_judgment'])
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'factory_judgment': factory_judgment,
                'internal_judgment': internal_judgment
            })
        else:
            messages.success(request, '质量判定完成')
            return render(request, 'qc_app/dryfilm_form.html', {
                'form': form, 
                'product': instance
            })
    
    # 表单验证失败
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': '表单数据验证失败',
            'errors': form.errors
        }, status=400)
    else:
        return render(request, 'qc_app/dryfilm_form.html', {
            'form': form,
            'product': product_instance
        })
