import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from ..forms import DryFilmConfigForm, DryFilmMainForm
from ..models import DryFilmStandard

logger = logging.getLogger(__name__)

def dryfilm_standard_list(request):
    """干膜标准列表视图"""
    dryfilmstandards = DryFilmStandard.objects.all().order_by('-product_name')
    logger.info(f"查询到 {len(dryfilmstandards)} 条干膜标准记录")
    return render(request, 'qc_app/dryfilm_standard/dryfilm_standard_list.html', {
        'dryfilmstandards': dryfilmstandards
    })

def create_dryfilm_standard(request):
    """创建干膜标准视图"""
    config_form = DryFilmConfigForm(request.POST or None)
    main_form = DryFilmMainForm(request.POST or None, config_json=None)
    
    if request.method == 'POST':
        # 处理AJAX请求（JSON配置预览）
        if 'generate-json' in request.POST:
            if config_form.is_valid():
                config_data = config_form.cleaned_data
                return JsonResponse({
                    'json_data': json.dumps(config_data, cls=DjangoJSONEncoder, indent=2),
                    'success': True
                })
            return JsonResponse({'success': False})
        
        # 处理主表单提交（保存到数据库）
        if main_form.is_valid():
            config_json = json.loads(request.POST.get('config_json', '{}'))
            
            instance = main_form.save(commit=False)
            instance.config_json = config_json
            instance.save()
            
            return redirect('dryfilm_success', pk=instance.id)
    
    return render(request, 'qc_app/dryfilm_standard/create.html', {
        'config_form': config_form,
        'main_form': main_form
    })

def success_view(request, pk):
    """成功页面视图"""
    record = DryFilmStandard.objects.get(pk=pk)
    return render(request, 'qc_app/dryfilm_standard/success.html', {'record': record})

def dryfilm_standard_edit(request, product_name):
    """编辑干膜标准视图"""
    dryfilm_standard = get_object_or_404(DryFilmStandard, product_name=product_name)
    config_form = DryFilmConfigForm(request.POST or None)
    main_form = DryFilmMainForm(request.POST or None, config_json=None)

    if request.method == 'POST':
        # 处理AJAX请求（JSON配置预览）
        if 'generate-json' in request.POST:
            if config_form.is_valid():
                config_data = config_form.cleaned_data
                return JsonResponse({
                    'json_data': json.dumps(config_data, cls=DjangoJSONEncoder, indent=2),
                    'success': True
                })
            return JsonResponse({'success': False})
        
        # 处理主表单提交（更新数据库）
        config_json = json.loads(request.POST.get('config_json', '{}'))
        
        # 更新记录
        update_fields = {
            'config_json': config_json,
            'producer': dryfilm_standard.producer
        }
        
        instance, created = DryFilmStandard.objects.update_or_create(
            product_name=product_name,
            defaults=update_fields
        )
            
        return redirect('dryfilm_success', pk=instance.id)
    
    else:
        main_form = DryFilmMainForm(instance=dryfilm_standard)
        config_form = DryFilmConfigForm(dryfilm_standard.config_json)

    return render(request, 'qc_app/dryfilm_standard/create.html', {
        'config_form': config_form,
        'main_form': main_form, 
        'mode': 'edit', 
        'dryfilm_standard': dryfilm_standard
    })

@require_POST
def dryfilm_standard_delete(request):
    """删除干膜标准视图"""
    record_id = request.POST.get('record_id')
    
    if not record_id:
        return JsonResponse({'success': False, 'message': '无效的请求参数'}, status=400)

    try:
        record = get_object_or_404(DryFilmStandard, pk=record_id)
        record.delete()
        
        messages.success(request, f"{record.product_name}-{record.created_at} 已成功删除")
        return redirect('dryfilm_standard_list')
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'删除失败: {str(e)}'
        }, status=500)
