from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import NFCTag
from .utils import scan_nfc_tag


def index(request):
    mirrored_values = request.GET.get('m', None)

    if mirrored_values:
        nfc_tag = scan_nfc_tag(mirrored_values, request.user if request.user.is_authenticated else None)

        if nfc_tag:
            return detail(request, nfc_tag.id)
        else:
            return JsonResponse({"error": "Unable to link NFC tag. Please try again later."}, status=400)

    if request.user.is_authenticated:
        nfc_tags = NFCTag.objects.filter(user=request.user).order_by('-created_at')
    else:
        nfc_tags = NFCTag.objects.none()

    return JsonResponse(nfc_tags.values('id', 'uid', 'content', 'created_at', 'updated_at'), safe=False)


def detail(request, nfc_tag_id):
    nfc_tag = get_object_or_404(NFCTag, id=nfc_tag_id, user__isnull=False)
    return JsonResponse({"nfc_tag": nfc_tag.metadata})


def link(request):
    mirrored_values = request.GET.get('m', None)

    if mirrored_values:
        nfc_tag = scan_nfc_tag(mirrored_values, request.user if request.user.is_authenticated else None)

        if nfc_tag:
            return JsonResponse({"redirect_url": reverse('ntags:detail', kwargs={'nfc_tag_id': nfc_tag.id})})
        else:
            return JsonResponse({"error": "Unable to link NFC tag. Please try again later."}, status=400)

    return JsonResponse({"redirect_url": "/"})
